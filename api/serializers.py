from rest_framework import serializers
from .models import Wallpaper, Tag, IconPack


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class WallpaperSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Wallpaper
        fields = '__all__'


class IconPackSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = IconPack
        fields = '__all__'
