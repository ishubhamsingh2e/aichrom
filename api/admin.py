from django.contrib import admin
from .models import Wallpaper, IconPack, IconPackImage, Preference, AppUser, Style, Color, Transaction, WallpaperTransaction

# Register your models here.


class IconPackImageInline(admin.TabularInline):
    model = IconPackImage
    extra = 1


admin.site.register(Wallpaper)
admin.site.register(IconPackImage)
admin.site.register(AppUser)
admin.site.register(Style)
admin.site.register(Color)
admin.site.register(Transaction)
admin.site.register(WallpaperTransaction)


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'color', 'male',
                    'style_1', 'style_2', 'icon_pack')


@admin.register(IconPack)
class IconPackAdmin(admin.ModelAdmin):
    inlines = [IconPackImageInline]
    search_fields = ['name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display = ('name', 'created_at', 'updated_at')
