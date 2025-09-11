import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Q, CharField
from django.db.models.functions import TruncDay, TruncMonth, TruncYear, Cast

from author.models import Author
from student.models import Student, StudentCoursePurchase
from courses.models import Course
from payments.models import Payment, PaymentStatus, PaymentType
from django.http import Http404
from courses.models import Course, ThematicsType
from student.models import StudentCoursePurchase, StudentCoursePurchase
from notification.models import Notification, NotificationTypes
from tariffs.models import Tariff
from tariffs.serializers import UserTariffSerializer
from types import SimpleNamespace

User = get_user_model()

def patch_payment_service(payment: Payment) -> bool:
    try:
        if payment.status == PaymentStatus.COMPLETED and payment.payment_type == PaymentType.COURSE_PURCHASE:
            student = get_object_or_404(Student, id=payment.user.id)
            course = get_object_or_404(Course, id=payment.item_id)
            author_id = course.author.pk
            author_user = User.objects.get(pk=author_id)

            StudentCoursePurchase.objects.get_or_create(
                student=student,
                course=course
            )
            
            Notification.objects.create(
                user=payment.user,
                title=f"Курс успешно приобретен",
                body=f"Вы успешно приобрели курс '{course.name}'",
                notification_type=NotificationTypes.PAYMENT_SUCCESS
            )
            Notification.objects.create(
                user=author_user,
                title=f"Приобретение курса",
                body=f"Курс '{course.name}' был приобретен пользователем '{student.email}'",
                notification_type=NotificationTypes.PAYMENT_SUCCESS
            )
        
        elif payment.status == PaymentStatus.PROCESSING and payment.payment_type == PaymentType.COURSE_PURCHASE:
            course = get_object_or_404(Course, id=payment.item_id)
            
            Notification.objects.create(
                user=payment.user,
                title=f"Оплата за курс создана.",
                body=f"Оплата за курс '{course.name}' успешно создана. Ожидается оплата",
                notification_type=NotificationTypes.EXPECTED_PAYMENT
            )
            
        elif payment.status == PaymentStatus.FAILED and payment.payment_type == PaymentType.COURSE_PURCHASE:
            student = get_object_or_404(Student, id=payment.user.id)
            course = get_object_or_404(Course, id=payment.item_id)

            StudentCoursePurchase.objects.filter(
                student=student,
                course=course
            ).delete()
            
            Notification.objects.create(
                user=payment.user,
                title=f"Ошибка приобретения курса",
                body=f"Вы не приобрели курс '{course.name}'",
                notification_type=NotificationTypes.PAYMENT_FAILED
            )

        elif payment.status == PaymentStatus.COMPLETED and payment.payment_type == PaymentType.REFUND:
            student = get_object_or_404(Student, id=payment.user.id)
            course = get_object_or_404(Course, id=payment.item_id)
            author_id = course.author.pk
            author_user = User.objects.get(pk=author_id)

            StudentCoursePurchase.objects.filter(
                student=student,
                course=course
            ).delete()

            Notification.objects.create(
                user=payment.user,
                title=f"Оплата за курс успешно возвращена",
                body=f"Вы успешно возвратили оплату за курс '{course.name}'",
                notification_type=NotificationTypes.REFUND_APPROVED
            )
            Notification.objects.create(
                user=author_user,
                title=f"Возврат денег за курс",
                body=f"Студент вернул деньги за Ваш курс '{course.name}'",
                notification_type=NotificationTypes.REFUND_APPROVED
            )
        
        elif payment.status == PaymentStatus.COMPLETED and payment.payment_type == PaymentType.SUBSCRIPTION:
            user = payment.user
            tariff = get_object_or_404(Tariff, id=payment.item_id)
            
            user_tariff_data = {'tariff_id': tariff.id, 'is_timeless': False, 'is_paid': True}
            serializer = UserTariffSerializer(data=user_tariff_data, context={'request': SimpleNamespace(user=user)})

            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                    user=user,
                    title=f"Подписка успешно приобретена",
                    body=f"Вы успешно приобрели подписку '{tariff.name}'",
                    notification_type=NotificationTypes.PAYMENT_SUCCESS
                )
            else:
                return False

        elif payment.status == PaymentStatus.FAILED and payment.payment_type == PaymentType.SUBSCRIPTION:
            pass
        
        elif payment.status == PaymentStatus.COMPLETED and payment.payment_type == PaymentType.OTHER:
            pass

        elif payment.status == PaymentStatus.FAILED and payment.payment_type == PaymentType.OTHER:
            pass

        return True

    except Http404:
        return False
    
def get_filtered_payments(payment_filter, course_ids, exclude_refund=False, refund_only=False):
    payment_query = Payment.objects.filter(status=PaymentStatus.COMPLETED, **payment_filter)
    
    if exclude_refund:
        payment_query = payment_query.exclude(payment_type=PaymentType.REFUND)
    if refund_only:
        payment_query = payment_query.filter(payment_type=PaymentType.REFUND)
        
    return payment_query.annotate(
        item_id_str=Cast('item_id', CharField())
    ).filter(
        item_id_str__in=[str(course_id) for course_id in course_ids]
    )

def get_course_type_statistic(course_ids: list, 
                              start_date: datetime.datetime, 
                              end_date: datetime.datetime) -> list:
    
    course_ids_str = [str(course_id) for course_id in course_ids]

    courses_payment_for_stats = list(Payment.objects.filter(
        payment_type=PaymentType.COURSE_PURCHASE,
        status=PaymentStatus.COMPLETED,
        item_id__in=course_ids_str
    ).values_list('item_id', flat=True))

    courses_with_refunds = list(Payment.objects.filter(
        payment_type=PaymentType.REFUND,
        status=PaymentStatus.COMPLETED,
        item_id__in=courses_payment_for_stats
    ).values_list('item_id', flat=True))

    for refunded in courses_with_refunds:
        if refunded in courses_payment_for_stats:
            courses_payment_for_stats.remove(refunded)

    valid_courses = set(courses_payment_for_stats)

    return list(ThematicsType.objects.annotate(
        total_purchases=Count(
            'courses__purchases',
            distinct=True,
            filter=Q(
                courses__purchases__purchase_date__range=(start_date, end_date),
                courses__id__in=valid_courses
            )
        )
    ).values('name', 'total_purchases').order_by('-total_purchases')[:4])


def get_statistic_service(author: Author, start_date_str: str, end_date_str: str):
    start_date = datetime.datetime.strptime(
        start_date_str, '%Y-%m-%d') if start_date_str else datetime.datetime.min
    end_date = datetime.datetime.strptime(
        end_date_str, '%Y-%m-%d') if end_date_str else datetime.datetime.max
    
    if end_date != datetime.datetime.max:
        end_date = end_date.replace(hour=23, minute=59, second=59)

    payment_filter = {}
    purchase_filter = {}

    if start_date:
        payment_filter['created_at__gte'] = start_date
        purchase_filter['purchase_date__gte'] = start_date
    if end_date:
        payment_filter['created_at__lte'] = end_date
        purchase_filter['purchase_date__lte'] = end_date

    course_ids = Course.objects.filter(author=author).values_list('id', flat=True)
    # course_stats = get_course_type_statistic(course_ids, start_date, end_date)

    course_stats = list(ThematicsType.objects.annotate(
        total_purchases=Count(
            'courses__purchases',
            distinct=True,
            filter=Q(
                courses__purchases__purchase_date__range=(start_date, end_date),
                courses__author=author
            )
        )
    ).filter(total_purchases__gt=0).values('name', 'total_purchases').order_by('-total_purchases')[:4])

    payments = get_filtered_payments(payment_filter, course_ids, exclude_refund=True)
    all_author_payments = Payment.objects.filter(
        status=PaymentStatus.COMPLETED,
        payment_type=PaymentType.COURSE_PURCHASE,
        item_id__in=[str(course_id) for course_id in course_ids]
    )

    best_day = all_author_payments.annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total_purchases=Count('id')
    ).order_by('-total_purchases').first()

    best_month = all_author_payments.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_purchases=Count('id')
    ).order_by('-total_purchases').first()

    best_year = all_author_payments.annotate(
        year=TruncYear('created_at')
    ).values('year').annotate(
        total_purchases=Count('id')
    ).order_by('-total_purchases').first()

    total_sum = payments.aggregate(
        total_sales=Sum('amount')
    )['total_sales'] or 0

    total_sales = payments.count()
    refunds = get_filtered_payments(payment_filter, course_ids, refund_only=True)

    refund_sum = refunds.aggregate(
        total_refund=Sum('amount')
    )['total_refund'] or 0

    refund_sales = refunds.count()
    total_sum -= refund_sum
    net_sales = total_sales - refund_sales
    
    purchase_history = payments.annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total_purchases=Count('id')
    ).order_by('day')

    response_data = {
        'course_stats': list(course_stats),
        'best_day': best_day,
        'best_month': best_month,
        'best_year': best_year,
        'total_sum': total_sum,
        'total_sales': total_sales,
        'net_sales': net_sales,
        'total_sales_day': best_day['total_purchases'] if best_day else 0,
        'total_sales_month': best_month['total_purchases'] if best_month else 0,
        'total_sales_year': best_year['total_purchases'] if best_year else 0,
        'refund_sales': refund_sales,
        'refund_sum': refund_sum,
        'purchase_history': list(purchase_history)
    }

    return response_data