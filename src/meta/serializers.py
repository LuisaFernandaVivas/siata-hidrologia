from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from rest_framework import serializers

from .models import Basin

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


class BasinSerializer(serializers.ModelSerializer):
    url             = serializers.HyperlinkedIdentityField(
                            view_name='basin-api:basin-detail',
                            lookup_field='slug'
                            )
    user            = UserPublicSerializer(read_only=True)
    class Meta:
        model = Basin
        fields = ['url','user','slug','pk','nombre','municipio','longitud','latitud','direccion','barrio','water_level_history_path','radar_rain_history_path','statistical_model_path','picture_path','camera_path','three_hours_image_path','one_day_image_path','three_days_image_path','monthly_image_path','basin_json_path','basin_mask_path']
