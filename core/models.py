from django.db import models
import random, string
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

ITEM_CATEGORY = [
    ('BEVERAGE', 'BEVERAGE'),
    ('CANNED GOODS', 'CANNED GOODS'),
    ('DAIRY PRODUCTS', 'DAIRY PRODUCTS'),
    ('FROZEN FOODS', 'FROZEN FOODS'),
    ('PERSONAL CARE', 'PERSONAL CARE'),
    ('CLEANING MATERIAL', 'CLEANING MATERIAL'),
]

TRANSACTION_STATUS = [
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('REFUNDED', 'REFUNDED'),
    ('CANCELED', 'CANCELED'),
    ('RETURNED', 'RETURNED'),
]

COUPON_AMOUNT = [
    (50, 50),
    (100, 100),
    (150, 150),
]

class Coupon(models.Model):
    amount = models.IntegerField(choices=COUPON_AMOUNT, default=50)
    code = models.CharField(max_length=8, null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        super(Coupon, self).save(*args, **kwargs)

class Item(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)
    stocks = models.IntegerField(default=100)
    price = models.FloatField(null=True)
    is_expired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=17, choices=ITEM_CATEGORY, default='BEVERAGE')
    code = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        super(Item, self).save(*args, **kwargs)

class PendingOrder(models.Model):
    pending_order = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='pending_order_item')
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'pending order ({self.pending_order.name})'

    class Meta:
        verbose_name_plural = 'Pending Orders'

class Transaction(models.Model):
    transaction = models.ForeignKey(PendingOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='pending_transaction')
    confirmation_number = models.CharField(max_length=8, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True, related_name='coupon')
    transaction_status = models.CharField(max_length=9, choices=TRANSACTION_STATUS, default='PENDING')

    def __str__(self):
        return str(self.id)

    def compute_transaction(self, total=0):
        coupon = Coupon.objects.filter(coupon=self)
        pending_order = PendingOrder.objects.filter(pending_transaction=self).first()

        if not coupon.exists():
            total = pending_order.quantity * int(pending_order.pending_order.price)
            return total
        
        else:
            amount = coupon.first().amount
            if amount > pending_order.quantity * int(pending_order.pending_order.price):
                return 0
            return pending_order.quantity * int(pending_order.pending_order.price) - amount

class ActivityLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, related_name='activity_log_item')
    pending_order = models.ForeignKey(PendingOrder, on_delete=models.CASCADE, null=True, related_name='activity_log_pending_order')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True,  related_name='activity_log_transaction')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, related_name='activity_log_coupon')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Activity Logs'


def create_activity_log(sender, instance, created, *args, **kwargs):
    if created:
        if sender == Item:
            activity_log = ActivityLog.objects.create(item=instance)
        elif sender == PendingOrder:
            activity_log = ActivityLog.objects.create(pending_order=instance)
        elif sender == Transaction:
            activity_log = ActivityLog.objects.create(transaction=instance)
        elif sender == Coupon:
            activity_log = ActivityLog.objects.create(coupon=instance)
        else:
            pass

post_save.connect(create_activity_log)
    