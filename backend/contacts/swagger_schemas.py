from drf_yasg.utils import swagger_auto_schema

from contacts.serializers import ContactCreateSerializer, GetContactsSerializer


get_all_contacts_schema = swagger_auto_schema(
    operation_summary="Получить список обращений (только для администратора)",
    operation_description="Доступно только для администратора.",
    responses={200: GetContactsSerializer(many=True)},
)

create_contact_schema = swagger_auto_schema(
    operation_summary="Создать обращение",
    operation_description="Создание нового обращения пользователем.",
    request_body=ContactCreateSerializer,
    responses={201: ContactCreateSerializer, 400: "Ошибка валидации"},
)