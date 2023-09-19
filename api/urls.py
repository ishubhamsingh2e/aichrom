from django.urls import path
from .views import WallpaperView, IconPackView

urlpatterns = [
    path('wallpapers', WallpaperView.as_view(), name='wallpapers'),
    path('iconpacks', IconPackView.as_view(), name='icon-packs')
]
