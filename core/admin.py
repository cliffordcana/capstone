from django.contrib import admin
from .models import Item, PendingOrder, Coupon, Transaction, ActivityLog

admin.site.register(Item)
admin.site.register(PendingOrder)
admin.site.register(Coupon)
admin.site.register(Transaction)
admin.site.register(ActivityLog)