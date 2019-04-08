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
        fields = ['url','slug','user','nombre','direccion','barrio','longitud','latitud','telefono_contacto','clase']
