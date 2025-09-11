from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers

from tariffs.models import Tariff, TariffDurationType, UserTariff


class UserTariffSerializer(serializers.ModelSerializer):
    tariff_id = serializers.PrimaryKeyRelatedField(source='tariff', queryset=Tariff.objects.all())

    class Meta:
        model = UserTariff
        fields = ('id', 'tariff_id', 'expire', 'is_timeless', 'is_paid')
        read_only_fields = ('id',)
        
    def validate(self, attrs):
        tariff = attrs.get('tariff')
        is_timeless = attrs.get('is_timeless', False)
        expire_date = None

        if not is_timeless:
            if tariff.duration == TariffDurationType.MONTHLY:
                expire_date = timezone.now() + timedelta(days=30)
            elif tariff.duration == TariffDurationType.YEARLY:
                expire_date = timezone.now() + timedelta(days=365)

        attrs['expire'] = expire_date
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        existing_user_tariff = UserTariff.objects.filter(user=user).first()
        
        if existing_user_tariff:
            existing_user_tariff.delete()

        user_tariff = super().create(validated_data)
        user_tariff.full_clean()
        return user_tariff

    @transaction.atomic
    def update(self, instance, validated_data):
        user_tariff = super().update(instance, validated_data)
        user_tariff.full_clean()
        return user_tariff


class TariffSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    features = serializers.SerializerMethodField(method_name='get_features')

    class Meta:
        model = Tariff
        fields = ('id', 'name', 'price', 'total_price', 'discount',
                  'percentage', 'features', 'duration')
        read_only_fields = ('features',)

    def get_features(self, instance) -> list[str]:
        return instance.features.values_list('text', flat=True)
