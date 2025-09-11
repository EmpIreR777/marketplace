from rest_framework import serializers

from contacts.models import Contact


class ContactCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    theme = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    is_agreed = serializers.BooleanField(required=True)

    class Meta:
        model = Contact
        fields = '__all__'

    def validate_is_agreed(self, value):
        """ Гарантирует, что is_agreed всегда True """
        if not value:
            raise serializers.ValidationError("Вы должны согласиться с условиями.")
        return value
        
        
class GetContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "email", "theme", "message", "is_agreed", "created_at"]