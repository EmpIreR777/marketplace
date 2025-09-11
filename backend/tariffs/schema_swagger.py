from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from tariffs.serializers import UserTariffSerializer


get_tariff_of_current_user_schema = swagger_auto_schema(
        method='get',
        operation_summary='Retrieve a tariff of the current user',
        responses={
            200: openapi.Response('User tariff', UserTariffSerializer),
            404: 'Tariff does not exist for the current user.',
        },
    )


set_tariff_for_current_user_schema = swagger_auto_schema(
        method='post',
        operation_summary='Set a tariff of the current user',
        responses={
            200: openapi.Response('User tariff', UserTariffSerializer),
            400: 'Validation error.',
        },
    )


refuse_tariff_for_current_user_schema = swagger_auto_schema(
        method='delete',
        operation_summary='Refuse the current tariff of the current user.',
        responses={
            200: 'User has no tariff.',
            204: 'Tariff was refused success.',
            400: 'Validation error.',
            404: 'Tariff does not exist for the current user.',
        }
    )
