from rest_framework import serializers
from . import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = ('id', 'name', 'color_code')


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Style
        fields = ('id', 'name', 'style_code', 'image_url')


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Preference
        fields = ('id', 'image', 'color', 'male', 'style_1', 'style_2')
        read_only_fields = ('id')
        extra_kwargs = {
            'user': {'write_only': True},
        }
        ordering = ('-created_at',)


class IconPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IconPack
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    icon_pack = IconPackSerializer()

    class Meta:
        model = models.Transaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {
            'user': {'write_only': True},
        }
        ordering = ('-created_at',)

class WallpaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallpaper
        fields = '__all__'


class TransactionWallpaperSerializer(serializers.ModelSerializer):
    wallpaper = WallpaperSerializer()

    class Meta:
        model = models.WallpaperTransaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {
            'user': {'write_only': True},
        }
        ordering = ('-created_at',)
