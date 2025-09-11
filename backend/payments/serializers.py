from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from payments.youkassa_services import refund_yokassa_payment
from yookassa.domain.exceptions import BadRequestError

from courses.models import Course
from tariffs.models import Tariff
from payments.models import Payment, PaymentType, PaymentStatus
from student.models import StudentCoursePurchase


class CoursePaymentDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['id', 'price', 'name']
    
    
class TariffPaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tariff
        fields = ['id', 'price', 'name']

class PaymentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    
    def get_item(self, obj):
        if obj.payment_type == PaymentType.COURSE_PURCHASE or obj.payment_type == PaymentType.REFUND:
            course = Course.objects.filter(id=obj.item_id).first()
            return CoursePaymentDetailSerializer(course).data if course else None
        elif obj.payment_type == PaymentType.SUBSCRIPTION:
            tariff = Tariff.objects.filter(id=obj.item_id).first()
            return TariffPaymentSerializer(tariff).data if tariff else None
        return None
    
    class Meta:
        model = Payment
        fields = ["id", "user", "item", "item_id", "amount", "status", 
                  "payment_type", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at"]
        ref_name = 'PaymentSerializer_Payments'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.payment_type == PaymentType.REFUND:
            data["refund_reason"] = instance.refund_reason
        return data


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["item_id", "payment_type"]

    def create(self, validated_data):
        user = self.context["request"].user
        item_id = validated_data["item_id"]
        payment_type = validated_data["payment_type"]

        if payment_type == PaymentType.COURSE_PURCHASE:
            course = Course.objects.filter(id=item_id).first()
            if not course:
                raise serializers.ValidationError("Course not found.")
            
            amount = course.price if course.price else Decimal('0.00')
            validated_data["amount"] = amount
            paid_courses_ids = StudentCoursePurchase.objects.filter(
                student=user).values_list("course_id", flat=True)

            if item_id in paid_courses_ids:
                raise serializers.ValidationError("This item is already bought.")

            return Payment.objects.create(user=user, **validated_data)
        
        elif payment_type == PaymentType.SUBSCRIPTION:
            tariff = Tariff.objects.filter(id=item_id).first()
            if not tariff:
                raise serializers.ValidationError("Tariff not found.")
            
            if tariff.price <= 0:
                raise serializers.ValidationError("Tariff price must be greater than 0.")
            
            validated_data["amount"] = tariff.price
            return Payment.objects.create(user=user, **validated_data)

        else:
            raise serializers.ValidationError("Invalid payment type.")


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["status"]
        
    def validate_status(self, value):
        if value not in PaymentStatus.values:
            raise serializers.ValidationError("Invalid status")
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data["status"]
        instance.save()
        return instance

class BestDayStatisticsSerializer(serializers.Serializer):
    day = serializers.DateField()
    total_purchases = serializers.IntegerField()
    

class CourseStatsSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_purchases = serializers.IntegerField()


class BestDayStatisticsSerializer(serializers.Serializer):
    day = serializers.DateTimeField()
    total_purchases = serializers.IntegerField()


class BestMonthStatisticsSerializer(serializers.Serializer):
    month = serializers.DateTimeField()
    total_purchases = serializers.IntegerField()


class BestYearStatisticsSerializer(serializers.Serializer):
    year = serializers.DateTimeField()
    total_purchases = serializers.IntegerField()


class StatisticsSerializer(serializers.Serializer):
    course_stats = CourseStatsSerializer(many=True)
    best_day = BestDayStatisticsSerializer()
    best_month = BestMonthStatisticsSerializer()
    best_year = BestYearStatisticsSerializer()
    total_sales = serializers.IntegerField()
    net_sales = serializers.IntegerField()
    total_sum = serializers.IntegerField()
    total_sales_day = serializers.IntegerField()
    total_sales_month = serializers.IntegerField()
    total_sales_year = serializers.IntegerField()
    refund_sales = serializers.IntegerField()
    refund_sum = serializers.IntegerField()
    purchase_history = serializers.ListField(child=serializers.DictField())
    

class RefundSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'status', 'payment_type',
                  'created_at', 'updated_at', 'course_id', 'refund_reason']
        read_only_fields = ['id', 'user', 'status', 'amount', 'payment_type', 'created_at']


    def validate_course_id(self, value):
        user = self.context['request'].user
        purchase = StudentCoursePurchase.objects.filter(student=user, course_id=value).exists()
        
        if not purchase:
            raise serializers.ValidationError("You haven't purchased this course.")
        
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        course_id = validated_data.pop('course_id')
        refund_reason = validated_data.pop('refund_reason')

        original_payment = Payment.objects.filter(
            user=user, item_id=str(course_id), status=PaymentStatus.COMPLETED
        ).order_by('-created_at').first()

        if not original_payment:
            raise serializers.ValidationError("No completed payment found for this course.")
        
        if original_payment.amount is None or original_payment.amount <= 0:
            refund_payment = Payment.objects.create(
                user=user,
                item_id=str(course_id),
                status=PaymentStatus.COMPLETED,
                payment_type=PaymentType.REFUND,
                amount=0,
                refund_reason=refund_reason
            )

            return refund_payment

        elif original_payment.created_at < timezone.now() - timezone.timedelta(days=5):
            refund_payment = Payment.objects.create(
                user=user,
                item_id=str(course_id),
                status=PaymentStatus.PROCESSING,
                payment_type=PaymentType.REFUND,
                amount=original_payment.amount,
                refund_reason=refund_reason
            )

            return refund_payment
        
        else:
            try:
                yokassa_refund = refund_yokassa_payment(
                    payment_id=original_payment.yokassa_payment_id, 
                    amount=original_payment.amount
                )
            except BadRequestError as e:
                raise serializers.ValidationError(e.content.get('description'))
            except Exception as e:
                raise serializers.ValidationError("Yokassa refund failed.")
            
            refund_payment = Payment.objects.create(
                user=user,
                item_id=str(course_id),
                status=PaymentStatus.COMPLETED,
                payment_type=PaymentType.REFUND,
                amount=original_payment.amount,
                refund_reason=refund_reason,
                yokassa_payment_id=yokassa_refund.id
            )

            return refund_payment
    