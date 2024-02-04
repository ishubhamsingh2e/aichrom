from django.urls import path
from .views import WallpaperListView, IconPackApiView, SendOTP, VerifyOTP

urlpatterns = [
    path('wallpapers/', WallpaperListView.as_view(), name='wallpapers'),
    path('iconpacks/', IconPackApiView.as_view(), name='icon-packs'),
    path("send_otp/", SendOTP.as_view(), name="send-otp"),
    path("verify_otp/", VerifyOTP.as_view(), name="verify-otp"),
]
