from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet, 
    PendingOrderView,
    CouponDetail, 
    VoidPendingOrder, 
    TransactionView, 
    SalesView, 
    ActivityLog, 
    TransactionDetail,
    TransactionReceipt
)

router = DefaultRouter()
router.register('', ItemViewSet, basename='item')

urlpatterns = [
    path('item/', include(router.urls)),
    path('pending_order/', PendingOrderView.as_view()),
    path('<str:code>/coupon/', CouponDetail.as_view()),
    path('void_pending_order/<int:pk>/', VoidPendingOrder.as_view()),
    path('transaction/', TransactionView.as_view()),
    path('transaction/sales/', SalesView.as_view()),
    path('activity_log/', ActivityLog.as_view()),
    path('transaction/<int:pk>/', TransactionDetail.as_view()),
    path('transaction/receipt', TransactionReceipt.as_view()),

]