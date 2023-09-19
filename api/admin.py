from django.contrib import admin
from .models import Wallpaper, Tag, IconPack

# Register your models here.

admin.site.register(Wallpaper)
admin.site.register(IconPack)
admin.site.register(Tag)
