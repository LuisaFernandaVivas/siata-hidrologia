from django.contrib.auth import get_user_model, authenticate, login, logout

from django.utils import timezone

from rest_framework import serializers

from .models import DataBasin

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            ]

class DataBasinSerializer(serializers.ModelSerializer):
    url             = serializers.HyperlinkedIdentityField(
                            view_name='data-api:basin-detail',
                            lookup_field='pk'
                            )
    user            = UserPublicSerializer(read_only=True)
    class Meta:
        model = DataBasin
        fields = ['url','date','water_level','radar_rain','interpolated_rain','water_flow','section_area','water_surface_velocity','water_level_color','radar_rain_color','water_surface_velocity_color']
