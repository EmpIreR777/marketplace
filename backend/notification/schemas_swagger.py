from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from notification.serializers import NotificationBaseSerializer, NotificationCreateSerializer, \
    NotificationTypesSerializer

notifications_list_schema = swagger_auto_schema(
    operation_summary="Уведомления пользователя.",
    operation_description="Возвращает список уведомлений пользователя.",
    responses={
        200: openapi.Response(
            description="Список уведомлений",
            schema=NotificationBaseSerializer(),
        ),
        204: openapi.Response(
            description="Пустой список",
        ),
        401: "Unauthorized",
    }
)
notifications_count_schema = swagger_auto_schema(
    operation_summary="Список непрочитанных уведомлений.",
    operation_description="Возвращает кол-во непрочитанных уведомлений у пользователя.",
    responses={
        200: openapi.Response(
            description="Количество непрочитанных уведомлений",
            schema=openapi.Schema(
                type=openapi.TYPE_INTEGER,
                example=5
            )
        ),
        401: "Unauthorized",
    }
)
notifications_create_schema = swagger_auto_schema(
    operation_summary="Создание уведомления",
    operation_description="Доступно только для администратора."
                          "Позволяет создать уведомление для пользователя.",
    responses={
        201: openapi.Response(
            description="Уведомление успешно создано",
            schema=NotificationCreateSerializer(),
        ),
        400: "Bad Request",
        401: "Unauthorized",
    }

)
notifications_get_types_schema = swagger_auto_schema(
    operation_summary="Список возможных типов уведомлений.",
    operation_description="Доступно только для администратора."
                          "Получение типов уведомлений.",
    responses={
        200: openapi.Response(
            description="Список типов",
            schema=NotificationTypesSerializer,
        ),
        400: "Bad Request",
        401: "Unauthorized",
    }
)
notifications_mark_all_as_read_schema = swagger_auto_schema(
    operation_summary="Пометить все непрочитанные уведомления как прочитанные.",
    responses={
        200: openapi.Response(
            description="Статус операции",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Описание статуса операции.",
                        example="marked 1 notifications as read"
                    ),
                    "is_success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Флаг успешности операции.",
                        example=True
                    ),
                }
            )
        ),
        400: "Bad Request",
        401: "Unauthorized",
    }
)

notifications_mark_read_by_id_schema = swagger_auto_schema(
    operation_summary="Пометить уведомление как прочитанное по его ID.",
    responses={
        200: openapi.Response(
            description="Статус",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "is_success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Флаг успешности операции.",
                        example=True
                    ),
                }
            )
        ),
        400: "Bad Request",
        401: "Unauthorized",
    }
)
