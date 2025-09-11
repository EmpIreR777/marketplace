from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from .filter import OrganizationFilter
from .models import Organization
from .serializers import OrganizationSerializer



class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OrganizationFilter
    ordering_fields = ['personal_account_name']
    ordering = ['personal_account_name']
    lookup_field = 'id'
    http_method_names = ["get", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrganizationSerializer
        elif self.action == 'create':
            return OrganizationSerializer

        return OrganizationSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
