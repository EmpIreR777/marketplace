from uuid import UUID

from django.contrib.admin import register
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from unfold import admin
from unfold.contrib.filters.admin import RangeDateTimeFilter, RangeNumericFilter
from yookassa.domain.exceptions import BadRequestError

from payments.models import Payment, PaymentStatus, PaymentType
from courses.models import Course
from payments.youkassa_services import refund_yokassa_payment
from payments.services import patch_payment_service
from payments.download_payments import export_payments_excel

##############################################################################################################
# Admin Models
##############################################################################################################
@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'buyer', 'author_corse', 'amount', 
                    'payment_type', 'status', 'formatted_created_at', 'formatted_updated_at')
    ordering = ('-created_at',)

    search_fields = ('user__email', 'user__last_name', 'user__first_name', 'user__middle_name')
    list_filter_submit = True
    list_filter = ('payment_type', 'status', ('amount', RangeNumericFilter),
                   ('updated_at', RangeDateTimeFilter), ('created_at', RangeDateTimeFilter))

    readonly_fields = ('id', 'created_at', 'updated_at')
    fields = ('id', 'user', 'item_id', 'amount', 'payment_type', 'status', 'updated_at', 'created_at')

    autocomplete_fields = ('user',)
    actions = ("confirm_payment", "cancel_payment", "refund_payment", "export_selected_to_csv")

    def buyer(self, obj):
        return f"{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}"
    

    def author_corse(self, obj):
        try:
            course = Course.objects.filter(id=UUID(obj.item_id)).first()
            if course and course.author:
                return f"{course.author.full_title or course.author.title} ({course.author.alias})"
        except (ValueError, ValidationError):
            return "Некорректный ID курса"
        return "Автор не найден"
    

    def course_name(self, obj):
        try:
            course = Course.objects.filter(id=UUID(obj.item_id)).first()
            if course:
                return f"{course.name}"
        except (ValueError, ValidationError):
            return "Некорректный ID курса"
        return "Курс не найден"


    def formatted_created_at(self, obj):
        return localtime(obj.created_at).strftime("%d.%m.%Y %H:%M")
    

    def formatted_updated_at(self, obj):
        return localtime(obj.updated_at).strftime("%d.%m.%Y %H:%M")


    def confirm_payment(self, request, queryset):
        queryset.update(status=PaymentStatus.PAID)


    def cancel_payment(self, request, queryset):
        queryset.update(status=PaymentStatus.FAILED)


    def refund_payment(self, request, queryset):
        for payment in queryset:
            original_payment = get_object_or_404(Payment, id=payment.id)
            course = get_object_or_404(Course, id=UUID(original_payment.item_id))

            try:
                yokassa_refund = refund_yokassa_payment(
                    payment_id=original_payment.yokassa_payment_id,
                    amount=original_payment.amount
                )

                refund_reason = "Возврат администратором"
                refund_payment = Payment.objects.create(
                    user=payment.user,
                    item_id=payment.item_id,
                    status=PaymentStatus.COMPLETED,
                    payment_type=PaymentType.REFUND,
                    amount=original_payment.amount,
                    refund_reason=refund_reason
                )
                refund_payment.yokassa_payment_id = yokassa_refund.id
                refund_payment.save()
                patch_payment_service(refund_payment)
            except BadRequestError as e:
                self.message_user(request, f"Платеж за курс '{course.name}' уже был возвращен", level='error')
                continue
            except Exception as e:
                self.message_user(request, f"Ошибка возврата через Юкассу: {str(e)}", level='error')
                continue

            self.message_user(request, f"Возврат средств для курса '{course.name}' выполнен успешно.")


    def export_selected_to_csv(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Не выбраны платежи для экспорта.", level="error")
            return

        self.message_user(request, "Отчет сформирован и загружен на Ваш компьютер.", level="success")
        return export_payments_excel(queryset)
    

    export_selected_to_csv.short_description = "Сформировать Exel-отчет"
    buyer.short_description = "Покупатель"
    author_corse.short_description = "Автор курса"
    course_name.short_description = "Название курса"

    formatted_updated_at.short_description = "Дата обновления"
    formatted_created_at.short_description = "Дата создания"

    confirm_payment.short_description = "Отметить оплату как выполненную"
    cancel_payment.short_description = "Отметить оплату как невыполненную"
    refund_payment.short_description = "Произвести возврат средств"
