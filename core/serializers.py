from .models import Item, PendingOrder, Coupon, Transaction, ActivityLog
from rest_framework import serializers

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id',
            'amount',
            'code',
            'is_valid',
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'stocks',
            'is_expired',
            'price',
            'category',
            'code'
        ]
        read_only_fields = [
            'code'
        ]

class PendingOrderSerializer(serializers.ModelSerializer):
    pending_order_item = serializers.CharField(source='pending_order.name', read_only=True)
    pending_order_price = serializers.FloatField(source='pending_order.price', read_only=True)

    class Meta:
        model = PendingOrder
        fields = [
            'id',
            'pending_order',
            'quantity',
            'ordered',
            'timestamp',
            'pending_order_item',
            'pending_order_price',
        ]
        read_only_fields = [
            'timestamp',
        ] 

class TransactionSerializer(serializers.ModelSerializer):
    transaction_price = serializers.SerializerMethodField()
    transaction_item = serializers.SerializerMethodField()
    transaction_quantity = serializers.SerializerMethodField()
    transaction_category = serializers.SerializerMethodField()
    transaction_total = serializers.SerializerMethodField()
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    coupon_amount = serializers.IntegerField(source='coupon.amount', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction',
            'confirmation_number',
            'timestamp',
            'coupon',
            'coupon_code',
            'coupon_amount',
            'transaction_category',
            'transaction_status',
            'transaction_price',
            'transaction_item',
            'transaction_quantity',
            'transaction_total',
        ]
        read_only_fields = [
            'timestamp',
            'confirmation_number',
        ] 

    def get_transaction_price(self, obj):
        transaction = Transaction.objects.filter(id=obj.id).first()
        return transaction.transaction.pending_order.price
    
    def get_transaction_item(self, obj):
        transaction = Transaction.objects.filter(id=obj.id).first()
        return transaction.transaction.pending_order.name

    def get_transaction_quantity(self, obj):
        transaction = Transaction.objects.filter(id=obj.id).first()
        return transaction.transaction.quantity
    
    def get_transaction_category(self, obj):
        transaction = Transaction.objects.filter(id=obj.id).first()
        return transaction.transaction.pending_order.category

    def get_transaction_total(self, obj):
        return obj.compute_transaction()

class ActivityLogSerializer(serializers.ModelSerializer):
    transaction_log = serializers.SerializerMethodField()
    pending_order_log = serializers.SerializerMethodField()
    item_log = serializers.SerializerMethodField()
    coupon_log = serializers.SerializerMethodField()
    null_values = [
        'item',
        'pending_order_item',
        'pending_order',
        'transaction',
        'coupon',
        'transaction_log',
        'item_log',
        'pending_order_log',
        'coupon_log'
    ]

    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'item',
            'pending_order',
            'transaction',
            'coupon',
            'timestamp',
            'transaction_log',
            'pending_order_log',
            'item_log',
            'coupon_log'
        ]

    def get_transaction_log(self, obj):
        activity_log = ActivityLog.objects.values(
            'transaction__transaction__pending_order__name',
            'transaction__confirmation_number'
        ).filter(id=obj.id)

        for activity in activity_log:
            transaction_item = activity['transaction__transaction__pending_order__name']
            confirmation_number = activity['transaction__confirmation_number']

            if transaction_item is not None or confirmation_number is not None:
                return f"Transaction completed ({transaction_item}) with transaction number ({confirmation_number})"

    def get_pending_order_log(self, obj):
        activity_log = ActivityLog.objects.values(
            'pending_order__pending_order__name',
            'pending_order__pending_order__code'
        ).filter(id=obj.id)
        
        for activity in activity_log:
            pending_order_item = activity['pending_order__pending_order__name']
            pending_order_code = activity['pending_order__pending_order__code']
            
            if pending_order_item is not None or pending_order_code is not None:
                return f"Added to pending order ({pending_order_item}) with item code ({pending_order_code})"

    def get_item_log(self, obj):
        activity_log = ActivityLog.objects.values('item__name', 'item__stocks').filter(id=obj.id)
        for activity in activity_log:
            item = activity['item__name']
            quantity = activity['item__stocks']
            
            if item is not None or quantity is not None: 
                return f"Added to inventory ({item}) -- quantity ({quantity})"

    def get_coupon_log(self, obj):
        activity_log = ActivityLog.objects.values('coupon__code', 'coupon__amount').filter(id=obj.id)
        for activity in activity_log:
            coupon_code = activity['coupon__code']
            coupon_amount = activity['coupon__amount']
            
            if coupon_code is not None or coupon_amount is not None: 
                return f"Coupon code generated ({coupon_code}) -- amount ({coupon_amount})"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for values in self.null_values:
            try:
                if rep[values] is None:
                    rep.pop(values)
            except KeyError:
                pass
        return rep
                