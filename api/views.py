import json
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallpaper
from .serializers import WallpaperSerializer


class WallpaperView(APIView):
    serializer_class = WallpaperSerializer

    def post(self, request):
        tags = json.loads(request.data['tags'])
        wallpapers = Wallpaper.objects.filter(tags__name__in=tags).distinct()
        serializer = WallpaperSerializer(wallpapers, many=True)
        return Response(serializer.data)
