import re
import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.db import transaction

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from author.models import Author
from payments.youkassa_services import create_yokassa_payment, get_yokassa_payment_info
from courses.models import Course
from payments.services import get_statistic_service, patch_payment_service
from payments.models import Payment, PaymentStatus, PaymentType
from payments.serializers import PaymentSerializer, PaymentCreateSerializer, \
    RefundSerializer, StatisticsSerializer
from student.models import Student, StudentCoursePurchase
from notification.models import Notification, NotificationTypes
from .swagger_schema import statistics_schema
User = get_user_model()

logger = logging.getLogger(__name__)


class PaymentListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        ten_minutes_ago = now() - timedelta(minutes=10)
        Payment.objects.filter(status=PaymentStatus.PROCESSING, 
                               created_at__lte=ten_minutes_ago).update(status=PaymentStatus.FAILED)

        if self.request.user.is_staff:
            return Payment.objects.all()
        author = Author.objects.filter(id=self.request.user.id).first()
        if not author:
            return Payment.objects.filter(user=self.request.user).order_by('-id')
        author_courses_ids = Course.objects.filter(author=author).values_list('id', flat=True)
        author_courses_ids = list(map(str, author_courses_ids))
        author_payments = Payment.objects.filter(user=self.request.user)
        return Payment.objects.filter(item_id__in=author_courses_ids).union(author_payments).order_by('-id')


    @swagger_auto_schema(request_body=PaymentCreateSerializer)
    def post(self, request, *args, **kwargs):
        #check if we are author
        if author := Author.objects.filter(id=request.user.id).first():
            if request.data.get('item_id') in author.courses.values_list('id', flat=True):
                return Response({"error": "Author can't buy his own course!"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Author can't buy courses!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
    
        if payment.payment_type == PaymentType.COURSE_PURCHASE:
            course = Course.objects.filter(id=payment.item_id).first()
            
            if not course:
                return Response({"error": "Course not found!"}, status=status.HTTP_404_NOT_FOUND)
            
            if course.price is None or course.price <= 0:
                payment.status = PaymentStatus.COMPLETED
                payment.save()
                patch_payment_service(payment)
                return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
                
            confirm_url = create_yokassa_payment(amount=payment.amount, 
                                                 description=f"Оплата за курс: '{course.name}'", 
                                                 payment_id=payment.id)
            match = re.search(r"orderId=([a-f0-9\-]+)", confirm_url)
            
            if match:
                payment_id = match.group(1)
                payment.yokassa_payment_id = payment_id
                payment.save()
                patch_payment_service(payment)
                return Response({"confirm_url": confirm_url}, status=status.HTTP_201_CREATED)      
        
        payment.save()
        
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = PaymentSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    
    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("pk")
        instance = get_object_or_404(Payment, id=payment_id)
        payment = get_yokassa_payment_info(instance.yokassa_payment_id)
        payment_status = payment.status
        
        if payment_status == "succeeded":
            instance.status = PaymentStatus.COMPLETED
            instance.save()

            if instance.payment_type == PaymentType.COURSE_PURCHASE:
                course = Course.objects.filter(id=instance.item_id).first()
                student = get_object_or_404(Student, id=instance.user.id)
                
                payed_student_course_purchase = StudentCoursePurchase.objects.filter(
                    student=student,
                    course=course
                ).first()
                
                if not payed_student_course_purchase:
                    patch_payment_service(instance)

                return redirect(f"{settings.HOST_URL}/course/{course.id}/?is_success_pay=true")
            
            elif instance.payment_type == PaymentType.SUBSCRIPTION:
                success = patch_payment_service(instance)
                
                if not success:
                    return Response({"error": "Error purchasing subscription"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                return redirect(f"{settings.HOST_URL}/account/tariff?is_success_pay=true")
        
        instance.status = PaymentStatus.FAILED
        instance.save()

        return redirect(f"{settings.HOST_URL}/account/payment-history")
    
    
    
class RefundAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RefundSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RefundSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        refund_payment = serializer.save()
        
        patch_payment_service(refund_payment)
        return Response(RefundSerializer(refund_payment).data, status=status.HTTP_201_CREATED)
        
        
class PaymentStatisticsAPIView(APIView):
    @statistics_schema
    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        author = get_object_or_404(Author, id=request.user.id)
        response_data = get_statistic_service(author=author,
                                              start_date_str=start_date_str, 
                                              end_date_str=end_date_str)
        serializer = StatisticsSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class YookassaView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        payment_id_yokassa = data.get('object', {}).get('id')
        status = data.get('object', {}).get('status')

        if payment_id_yokassa and status == 'succeeded':
            try:
                with transaction.atomic():
                    payment = get_object_or_404(Payment, yokassa_payment_id=payment_id_yokassa)

                    if payment.status != PaymentStatus.COMPLETED:
                        payment.status = PaymentStatus.COMPLETED
                        payment.save()
                        patch_payment_service(payment)

                logger.warning(f"Payment {payment_id_yokassa} successfully updated to PAID, course {payment.item_id} is now available.")
                return Response({"message": "OK"}, status=200)
            except Payment.DoesNotExist:
                logger.error(f"Payment with ID {payment_id_yokassa} not found.")
                return Response({"message": "Payment not found"}, status=404)
            except Course.DoesNotExist:
                logger.error(f"Course with ID {payment.item_id} not found.")
                return Response({"message": "Course not found"}, status=404)
            except Exception as e:
                logger.error(f"Error processing payment {payment_id_yokassa}: {str(e)}")
                return Response({"message": "Error processing payment"}, status=500)
        else:
            logger.warning(f"Invalid payment status or missing payment ID: {request.data}")
            return Response({"message": "Invalid data"}, status=400)