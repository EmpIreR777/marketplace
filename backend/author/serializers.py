from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from author.models import Author, AuthorType, Document, DocumentType, RequiredDocument, FIZAuthor, FOPAuthor, LLCAuthor
from feedback.models import Feedback
from userauth.serializers import UserSerializer
from django.conf import settings


User = get_user_model()


class FIZAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIZAuthor
        fields = '__all__'


class FOPAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FOPAuthor
        fields = '__all__'


class LLCAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLCAuthor
        fields = '__all__'
            

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['file', 'document_type']


class AuthorSerializer(UserSerializer):
    documents = DocumentsSerializer(many=True)
    logo = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    verify_fields = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.title  if obj.title else f'{obj.last_name} {obj.first_name} {obj.middle_name}'


    def get_logo(self, obj):
        if hasattr(obj, 'logo') and obj.logo:
            if hasattr(obj.logo, 'url'):
                return f'{settings.HOST_URL}{obj.logo.url}'
        return super().get_photo(obj)
    
    
    def get_verify_fields(self, obj):
        if obj.author_type == AuthorType.INDIVIDUAL and hasattr(obj, 'fiz_author'):
            return FIZAuthorSerializer(obj.fiz_author).data
        elif obj.author_type == AuthorType.INDIVIDUAL_ENTREPRENEUR and hasattr(obj, 'fop_author'):
            return FOPAuthorSerializer(obj.fop_author).data
        elif obj.author_type == AuthorType.ORGANIZATION and hasattr(obj, 'llc_author'):
            return LLCAuthorSerializer(obj.llc_author).data
        else:
            return {}


    class Meta:
        model = Author
        fields = UserSerializer.Meta.fields + ['author_type', 'alias', 'full_title', 'title',
                                               'prepositional_title', 'genitive_title',
                                               'description', 'logo', 'website', 'address', 'legal_address',
                                               'education_type', 'is_premium_partner', 'documents', 
                                               'is_verified', "verify_fields", "verification_status"]
        read_only_fields = ['verification_status']

    def update(self, instance, validated_data):
        request = self.context.get("request")
        
        if request and request.FILES.get("photo"):
            instance.photo = request.FILES["photo"]
        
        if request and request.FILES.get("documents"):
            documents = request.FILES.getlist("documents")
            Document.objects.bulk_create([Document(author=instance, file=document) for document in documents])
            
        validated_data.pop("verify_fields", None)
        missing_documents = self.get_missing_documents(instance)
                 
        if missing_documents:
            raise ValidationError({
                "documents": f"Отсутствуют обязательные документы: {', '.join(missing_documents)}"
            })

        return super().update(instance, validated_data)

    def get_missing_documents(self, author):
        required_docs = RequiredDocument.objects.filter(author_type=author.author_type).first()
        if not required_docs:
            return []

        required_doc_types = set(required_docs.document_types.values_list("id", flat=True))
        author_doc_types = set(author.documents.values_list("document_type_id", flat=True))

        missing_doc_types = required_doc_types - author_doc_types
        if not missing_doc_types:
            return []

        missing_doc_names = DocumentType.objects.filter(id__in=missing_doc_types).values_list(
            "document_type", flat=True)
        return list(missing_doc_names)


class AuthorsFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "feedback_author", "feedback_text", "feedback_rating", "feedback_date"]


class AuthorForCourseSerializer(UserSerializer):
    logo = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        return obj.title  if obj.title else f'{obj.last_name} {obj.first_name} {obj.middle_name}'

    def get_logo(self, obj):
        if hasattr(obj, 'logo') and obj.logo:
            if hasattr(obj.logo, 'url'):
                return f'{settings.HOST_URL}{obj.logo.url}'
        return super().get_photo(obj)
    
    
    class Meta:
        model = Author
        fields = ['id', 'photo', 'is_active', 'account_type', 'email'
                  ] + ['author_type', 'alias', 'full_title', 'title', 
                  'prepositional_title', 'genitive_title', 'description',
                  'logo', 'is_verified', "verification_status"]
        