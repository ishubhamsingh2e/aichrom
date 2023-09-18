from django.urls import path
from .views import WallpaperView


urlpatterns = [
    path('wallpapers', WallpaperView.as_view(), name='wallpapers'),
]
