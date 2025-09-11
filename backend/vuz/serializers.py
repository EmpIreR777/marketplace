from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from .models import OrganizationsVuz, Cities, Contacts, Metros, Subjects, \
    AdmissionOffices, Programs, Forms, Faculties, Specialties


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ['id', 'name', 'is_capital', 'city_type']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['site', 'phones', 'email', 'address', 'post_index']


class MetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metros
        fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['id', 'name', 'name_rp']


class AdmissionOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionOffices
        fields = [
            'type', 'source', 'site', 'email', 'phones',
            'address', 'longitude_latitude', 'post_index',
            'schedule', 'description', 'start_date', 'end_date',
            'is_full_year'
        ]


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['id', 'name']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculties
        fields = ['id', 'name', 'address', 'email', 'phone']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialties
        fields = ['id', 'name', 'code', 'qualification', 'description', 'level_code']


class ProgramSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)
    form = FormSerializer(read_only=True)
    
    class Meta:
        model = Programs
        fields = [
            'id', 'profile', 'duration', 'budget_places', 
            'budget_score', 'commercial_places', 'commercial_score', 
            'cost', 'faculty', 'specialty', 'form', 'calculation_data'
        ]


class OrganizationVuzListSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    contact = ContactSerializer(read_only=True)
    metro = MetroSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    admission_office = AdmissionOfficeSerializer(read_only=True)
    programs_count = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationsVuz
        fields = [
            'id', 'type', 'source', 'name', 'code', 'full_name', 'short_name',
            'obrnadzor_name', 'obrnadzor_checked', 'short_seo', 'about',
            'logo', 'logo_storage', 'video_link',
            'sort', 'sort_for_region', 'sort_for_top',
            'published', 'is_state', 'is_hostel', 'is_military',
            'is_departmental', 'is_partner', 'has_leads', 'is_confirmed',
            'is_top100',
            'inn', 'kpp', 'monitoring_code', 'longitude_latitude',
            'organization_type', 'sub_type', 'site',
            'licence_num', 'licence_date',
            'accreditation_number', 'accreditation_date',
            'rating', 'esi', 'esi24', 'esi_marks',
            'ege_score', 'cost',
            'old_names', 'delete_reason', 'confirmed_and_date',
            'calculation_data',
            'created_at', 'updated_at', 'external_updated_at',
            'city', 'contact', 'metro', 'subject', 'admission_office',
            'programs_count'
        ]
    
    def get_programs_count(self, obj):
        return getattr(obj, 'programs_count', 0)


class OrganizationVuzDetailSerializer(OrganizationVuzListSerializer):
    class Meta(OrganizationVuzListSerializer.Meta):
        pass


class ProgramListSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True)
    form = FormSerializer(read_only=True)
    organization_vuz = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Programs
        fields = [
            'id', 'profile', 'duration', 'budget_places', 
            'budget_score', 'commercial_places', 'commercial_score', 
            'cost', 'faculty', 'specialty', 'form',
            'organization_vuz', 'calculation_data'
        ]


##############################################################################################################
# Filters serializers
##############################################################################################################

class FacultyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculties
        fields = ['id', 'name']


class SpecialtyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialties
        fields = ['id', 'name', 'level_code']


class FormFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = ['id', 'name']


class VuzFiltersSerializer(serializers.Serializer):
    city = serializers.DictField(read_only=True)
    subject = serializers.DictField(read_only=True)
    metro = serializers.DictField(read_only=True)
    faculty = serializers.DictField(read_only=True)
    specialty = serializers.DictField(read_only=True)
    form = serializers.DictField(read_only=True)
    level_code = serializers.DictField(read_only=True)
    organization_type = serializers.DictField(read_only=True)
    price = serializers.DictField(read_only=True)
    rating = serializers.DictField(read_only=True)
    is_state = serializers.DictField(read_only=True)
    
    cities_total = serializers.IntegerField(read_only=True, required=False)
    subjects_total = serializers.IntegerField(read_only=True, required=False)
    metros_total = serializers.IntegerField(read_only=True, required=False)
    faculties_total = serializers.IntegerField(read_only=True, required=False)
    specialties_total = serializers.IntegerField(read_only=True, required=False)
    forms_total = serializers.IntegerField(read_only=True, required=False)
    level_codes_total = serializers.IntegerField(read_only=True, required=False)
    organization_types_total = serializers.IntegerField(read_only=True, required=False)


class ProgramFiltersSerializer(serializers.Serializer):
    faculty = FacultyFilterSerializer(many=True)
    specialty = SpecialtyFilterSerializer(many=True)
    form = FormFilterSerializer(many=True)
    price_min = serializers.IntegerField()
    price_max = serializers.IntegerField()
    duration_min = serializers.IntegerField()
    duration_max = serializers.IntegerField()
    budget_places_min = serializers.IntegerField()
    budget_places_max = serializers.IntegerField()
    min_commercial_places = serializers.IntegerField()
    max_commercial_places = serializers.IntegerField()
    min_budget_score = serializers.IntegerField()
    max_budget_score = serializers.IntegerField()
    min_commercial_score = serializers.IntegerField()
    max_commercial_score = serializers.IntegerField()
    total_count = serializers.IntegerField()