from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

user_auth_schema = swagger_auto_schema(
    tags=["User Auth"],
    manual_parameters=[
        openapi.Parameter(
            "user_id",
            openapi.IN_PATH,
            description="ID пользователя",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Email пользователя"
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Пароль пользователя"
                    ),
                    "first_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Имя пользователя"
                    ),
                    "last_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Фамилия пользователя"
                    ),
                    "middle_name": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Отчество пользователя"
                    ),
                    "bio": openapi.Schema(
                        type=openapi.TYPE_STRING, description="О себе"
                    ),
                    "birth_date": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Дата рождения"
                    ),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Номер телефона"
                    ),
                    "photo": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Фото профиля (URL)"
                    ),
                },
                required=["email", "password"],
            ),
            "documents": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "document": openapi.Schema(
                            type=openapi.TYPE_FILE,
                            description="Документы для верификации",
                        ),
                    },
                ),
            ),
            "account_type": openapi.Schema(
                type=openapi.TYPE_STRING, description="Тип аккаунта"
            ),
            "is_verified": openapi.Schema(
                type=openapi.TYPE_BOOLEAN, description="Проверен ли аккаунт"
            ),
        },
        required=["user"],
    ),
    responses={
        200: openapi.Response(description="Профиль пользователя обновлен"),
        400: openapi.Response(description="Некорректные данные"),
        404: openapi.Response(description="Пользователь не найден"),
    },
    consumes=["multipart/form-data"],
)
