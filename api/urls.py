from django.urls import path
from .views import GetTransaction, WallpaperListView, IconPackApiView, SendOTP, VerifyOTP, GetPreferenceImage, GetPreferenceSchema, TransactionSchema, WallpaperTransactionSchema

urlpatterns = [
    path('wallpapers/', WallpaperListView.as_view(), name='wallpapers'),
    path('iconpacks/', IconPackApiView.as_view(), name='icon-packs'),
    path("get_preferance_schema/", GetPreferenceSchema.as_view(), name=""),
    path('preference_image/', GetPreferenceImage.as_view(), name='icon-pack'),
    path("send_otp/", SendOTP.as_view(), name="send-otp"),
    path("verify_otp/", VerifyOTP.as_view(), name="verify-otp"),
    path("transaction/", TransactionSchema.as_view(), name="transaction"),
    path("wallpaper_transaction/", WallpaperTransactionSchema.as_view(), name="transaction"),
    path("restore/", GetTransaction.as_view(), name="transaction")
]
