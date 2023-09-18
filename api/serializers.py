from rest_framework import serializers
from .models import Wallpaper, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class WallpaperSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Wallpaper
        fields = '__all__'
