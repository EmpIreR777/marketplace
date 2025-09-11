from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from author.serializers import AuthorSerializer

user_author_schema = swagger_auto_schema(
    tags=["Auhtor"],
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
            "author_type": openapi.Schema(
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

author_list_schema = swagger_auto_schema(
    operation_summary="Получение списка авторов",
    operation_description="Выводит список всех сущностей которые могут быть авторами курсов.",
    responses={
        200: openapi.Response(
            description="Список авторов",
            schema=AuthorSerializer()
        )
    }
)

unverified_authors_schema = swagger_auto_schema(
    operation_summary="Получение списка неверифицированных авторов",
    operation_description="Только администратор может получить список авторов, находящихся на верификации.",
    responses={
        200: openapi.Response(
            description="Список неверифицированных автором",
            schema=AuthorSerializer()
        )
    }
)

verify_author_schema = swagger_auto_schema(
    operation_summary="Верификация автора",
    operation_description="Только администратор может верифицировать автора.",
    request_body=AuthorSerializer,
    responses={
        200: "Author verified successfully."
    }
)

retrieve_author_schema = swagger_auto_schema(
    operation_summary="Получение автора",
    operation_description="Автор может получить только себя . \
        Администратор может получить любого автора.",
    responses={
        200: openapi.Response(
            description="Детали профиля",
            schema=AuthorSerializer()
        ),
        403: "Permission denied."
    }
)

delete_author_admin_schema = swagger_auto_schema(
    operation_summary="Удаление автора администратором",
    operation_description="Помечает автора как удаленный, \
        помечая юзера, как не активного, удаляя его документы и фото.",
    request_body=None,
    responses={
        204: 'Автор помечен как удаленный, все прошло успешно.',
        403: 'Недостаточно прав для выполнения операции'
    }
)
