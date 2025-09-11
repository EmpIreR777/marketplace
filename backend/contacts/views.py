from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from contacts.models import Contact
from contacts.swagger_schemas import get_all_contacts_schema, create_contact_schema
from contacts.serializers import ContactCreateSerializer, GetContactsSerializer


class ContactsView(GenericAPIView):
    http_method_names = ["get", "post"]

    @get_all_contacts_schema
    def get(self, request):
        if not request.user.is_authenticated and not request.user.is_staff:
            return Response({"detail": "Only admin can get contacts"},
                            status=status.HTTP_403_FORBIDDEN)

        contacts = Contact.objects.all().order_by('-created_at')
        pagination_result = self.paginator.paginate_queryset(contacts, request)
        serializer = GetContactsSerializer(pagination_result, many=True)
        return Response(serializer.data)

    @create_contact_schema
    def post(self, request):
        serializer = ContactCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
