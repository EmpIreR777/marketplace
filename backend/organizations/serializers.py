from author.serializers import AuthorSerializer
from organizations.models import Organization, OrganizationRequisites
from rest_framework import serializers


class OrganizationRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRequisites
        fields = ['bik', 'inn', 'kpp', 'ogrn']

class OrganizationSerializer(AuthorSerializer):
    requisites = OrganizationRequisitesSerializer()

    class Meta:
        model = Organization
        fields = AuthorSerializer.Meta.fields + ['type', 'partner_card', 'license', 'personal_account_name',
                                                 'personal_account_site', 'leadership', 'requisites']


