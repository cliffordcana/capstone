from rest_framework import viewsets, status, generics
from .models import Item, PendingOrder, Coupon, Transaction, ActivityLog
from .serializers import ItemSerializer, PendingOrderSerializer, \
    CouponSerializer, TransactionSerializer, ActivityLogSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import random, string
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class CouponDetail(generics.RetrieveAPIView):
    serializer_class = CouponSerializer
    lookup_field = 'code'

    def get_queryset(self):
        qs = Coupon.objects.filter(is_valid=True)
        return qs

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'stocks', 'price', 'category', 'code']
    lookup_field = 'code'

    def get_queryset(self):
        qs = Item.objects.filter(is_expired=False, stocks__gt=0).order_by('name')
        return qs

    @action(detail=False, methods=['GET'])
    def inventory(self, request, *args, **kwargs):
        item_qs = Item.objects.values(
            'name',
            'stocks',
            'price',
            'is_expired',
            'category',
            'timestamp'
        ).annotate(total=Sum('price') * Sum('stocks')).order_by('-is_expired', 'stocks')

        active_items = item_qs.filter(is_expired=False)
        expired_items = item_qs.filter(is_expired=True)

        active_items_total = sum([items['total'] for items in active_items])
        expired_items_total = sum([items['total'] for items in expired_items])

        active_expired_items_total = active_items_total + expired_items_total

        return Response(
            {   
                'item_qs': item_qs,
                'active_items_total': active_items_total,
                'expired_items_total': expired_items_total,
                'active_expired_items_total': active_expired_items_total
            }
        )
    
class PendingOrderView(APIView):
    serializer_class = PendingOrderSerializer

    def get(self, request, *args, **kwargs):
        qs = PendingOrder.objects.filter(ordered=False, pending_order__stocks__gt=0).order_by('-timestamp')
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=request.data['id'])

        pending_order = PendingOrder.objects.create(
            pending_order=item,
            ordered=False,
            timestamp=timezone.now()
        )
        pending_order.save()

        return Response(status=status.HTTP_201_CREATED)

class VoidPendingOrder(generics.DestroyAPIView):
    serializer_class = PendingOrderSerializer

    def get_queryset(self):
        return PendingOrder.objects.filter(ordered=False).order_by('-timestamp')

class TransactionView(APIView):
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        qs = Transaction.objects.all().order_by('-timestamp')
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        quantity = data['orderQuantity']
        pending_order_id = data['pendingOrderID']

        coupon_data = data['couponData']
        code = coupon_data.get('code')

        item = Item.objects.filter(pending_order_item__id=pending_order_id).first()

        if int(quantity) > item.stocks:
            return Response({'error': 'insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        item.stocks -= int(quantity)
        item.save()

        pending_order = PendingOrder.objects.get(id=pending_order_id)
        pending_order.ordered = True
        pending_order.quantity = quantity
        pending_order.save()

        confirmation_number = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

        if code is not None:
            coupon = Coupon.objects.get(code=code)
            coupon.is_valid = False
            coupon.save()

            transaction = Transaction.objects.create(
                transaction=pending_order,
                transaction_status='COMPLETED',
                timestamp=timezone.now(),
                confirmation_number=confirmation_number,
                coupon=coupon
            )
            transaction.save()
        
        else:
            transaction = Transaction.objects.create(
                transaction=pending_order,
                transaction_status='COMPLETED',
                timestamp=timezone.now(),
                confirmation_number=confirmation_number,
            )
            transaction.save()

        return Response(status=status.HTTP_201_CREATED)

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().order_by('-timestamp')

    def put(self, request, pk):
        data = request.data
        action = data['action']

        transaction = Transaction.objects.get(pk=pk)
        
        if action == 'RETURN':
            transaction.transaction_status = 'RETURNED'
        else:
            transaction.transaction_status = 'REFUNDED'

        transaction.save()
        return Response(status=status.HTTP_200_OK)

class SalesView(APIView):
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        from datetime import datetime
        
        transaction_qs = Transaction.objects.filter(
            transaction_status='COMPLETED', 
            transaction__ordered=True
        ).order_by('-timestamp')
        serializer = self.serializer_class(transaction_qs, many=True)
        
        today = date.today()
        monday = today + timedelta(days=-today.weekday())
        sunday = monday + timedelta(days=6)
        first_day_of_the_month = today.replace(day=1)
        last_day_of_the_month = first_day_of_the_month + relativedelta(days=30) 

        sales_today_qs = transaction_qs.filter(timestamp__date=today)
        sales_today_qs_serializer = self.serializer_class(sales_today_qs, many=True)
        sales_today = sum([total['transaction_total'] for total in sales_today_qs_serializer.data])

        sales_weekly_qs = transaction_qs.filter(timestamp__date__range=[monday, sunday])
        sales_weekly_qs_serializer = self.serializer_class(sales_weekly_qs, many=True)
        sales_weekly = sum([total['transaction_total'] for total in sales_weekly_qs_serializer.data])

        sales_monthly_qs = transaction_qs.filter(timestamp__date__range=[first_day_of_the_month, last_day_of_the_month])
        sales_monthly_qs_serializer = self.serializer_class(sales_monthly_qs, many=True)
        sales_monthly = sum([total['transaction_total'] for total in sales_monthly_qs_serializer.data])

        return Response(
            {
                'transaction_qs': serializer.data,
                'sales_today': sales_today,
                'sales_weekly': sales_weekly,
                'sales_monthly': sales_monthly
            }
        )

class ActivityLog(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    queryset = ActivityLog.objects.all().order_by('-timestamp')

class TransactionReceipt(APIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        payload = data['payload']

        '''
            payload is either a confirmation number which will generate a single receipt 
            or a number, let's say 5 and it will generate a receipt for the last 5 transactions
        '''

        if len(payload) == 8: #if payload is a confirmation number
            transaction = Transaction.objects.filter(confirmation_number=payload)
            transaction_serializer = self.serializer_class(transaction, many=True)
            return Response({'transaction_receipt': transaction_serializer.data})

        else:
            transaction_qs = Transaction.objects.all().order_by('-timestamp')[:int(payload)]
            transaction_qs_serializer = self.serializer_class(transaction_qs, many=True)
            transaction_total = sum([total['transaction_total'] for total in transaction_qs_serializer.data])

            return Response({
                'transaction_receipt': transaction_qs_serializer.data,
                'transaction_total': transaction_total
            })