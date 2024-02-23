from rest_framework import serializers
from . import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = ('id', 'name', 'color_code')


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Style
        fields = ('id', 'name', 'style_code')


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Preference
        fields = ('id', 'image', 'color', 'male', 'style_1', 'style_2')
        read_only_fields = ('id')
        extra_kwargs = {
            'user': {'write_only': True},
        }
        ordering = ('-created_at',)
