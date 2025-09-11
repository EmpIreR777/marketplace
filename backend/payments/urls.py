from django.urls import path
from payments.views import PaymentListAPIView, PaymentDetailAPIView, \
    PaymentStatisticsAPIView, RefundAPIView, YookassaView


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetailAPIView.as_view(), name="payment-detail"), 
    path("payments/statistics/", PaymentStatisticsAPIView.as_view(), name="payment-statistics"),
    path('payments/refund/', RefundAPIView.as_view(), name='refund'),
    path('payments/yookassa/', YookassaView.as_view(), name='yookassa'),
]
