import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Wallpaper, IconPack
from .serializers import WallpaperSerializer, IconPackSerializer


class WallpaperView(APIView):
    serializer_class = WallpaperSerializer

    def post(self, request):
        try:
            tags = request.data.get('tags')

            if tags is None:
                return Response("Tags not provided", status=status.HTTP_400_BAD_REQUEST)

            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                return Response("Invalid JSON format for tags", status=status.HTTP_400_BAD_REQUEST)

            wallpapers = Wallpaper.objects.filter(tags__name__in=tags).distinct()
            serializer = WallpaperSerializer(wallpapers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IconPackView(APIView):
    serializer_class = WallpaperSerializer

    def get(self, request):
        try:
            icon_packs = IconPack.objects.all()
            serializer = IconPackSerializer(icon_packs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            tags = request.data.get('tags')

            if tags is None:
                return Response("Tags not provided", status=status.HTTP_400_BAD_REQUEST)

            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                return Response("Invalid JSON format for tags", status=status.HTTP_400_BAD_REQUEST)

            wallpapers = IconPack.objects.filter(tags__name__in=tags).distinct()
            serializer = IconPackSerializer(wallpapers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
