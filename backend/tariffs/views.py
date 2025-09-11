import re

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tariffs.filters import TariffDurationTypeFilter
from tariffs.models import Tariff, UserTariff
from tariffs.schema_swagger import (
    get_tariff_of_current_user_schema,
    refuse_tariff_for_current_user_schema,
    set_tariff_for_current_user_schema
)
from tariffs.serializers import TariffSerializer, UserTariffSerializer
from payments.youkassa_services import create_yokassa_payment
from payments.models import PaymentType
from payments.serializers import PaymentCreateSerializer


class TariffViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = TariffDurationTypeFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Tariff.objects.filter(is_show=True, is_active=True).order_by('price')
        return UserTariff.objects.select_related('user', 'tariff').all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TariffSerializer
        return UserTariffSerializer

    @get_tariff_of_current_user_schema
    @action(methods=['get'], detail=False, url_path='user_tariff', pagination_class=None,
            filterset_class=None)
    def get_tariff_of_current_user(self, request: Request):
        user_tariff = self._get_user_tariff_by_current_user(request.user)
        serializer = self.get_serializer(instance=user_tariff) if user_tariff else None
        return Response(data={"tariff": serializer.data} if serializer else {"tariff": None})

    @set_tariff_for_current_user_schema
    @action(methods=['post'], detail=False, url_path='user_tariff/set', filterset_class=None)
    def set_tariff_for_current_user(self, request):
        tariff_id = request.data.get('tariff_id')
        if not tariff_id:
            return Response({"error": "Tariff ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tariff = Tariff.objects.get(id=tariff_id)
        except Tariff.DoesNotExist:
            return Response({"error": "Tariff not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentCreateSerializer(
            data={"item_id": tariff_id, "payment_type": PaymentType.SUBSCRIPTION},
            context={"request": request}
        )
        
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        confirm_url = create_yokassa_payment(amount=payment.amount, 
                                             description=f"Оплата за подписку: '{tariff.name}'", 
                                             payment_id=payment.id)
        match = re.search(r"orderId=([a-f0-9\-]+)", confirm_url)
        if match:
            payment.yokassa_payment_id = match.group(1)
            payment.save()

        return Response({"confirm_url": confirm_url}, status=status.HTTP_201_CREATED)


    @refuse_tariff_for_current_user_schema
    @action(methods=['delete'], detail=False, url_path='user_tariff/refuse', filterset_class=None)
    def refuse_tariff_for_current_user(self, request: Request):
        try:
            self.get_queryset().get(user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise NotFound(detail='Tariff was not found.')

    def _get_user_tariff_by_current_user(self, user) -> UserTariff | Response:
        return self.get_queryset().filter(user=user).first()
