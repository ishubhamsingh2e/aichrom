from django.contrib import admin
from .models import Wallpaper, IconPack, IconPackImage, Preference, AppUser

# Register your models here.

class IconPackImageInline(admin.TabularInline):
    model = IconPackImage
    extra = 1


admin.site.register(Wallpaper)
admin.site.register(IconPackImage)
admin.site.register(Preference)
admin.site.register(AppUser)

@admin.register(IconPack)
class IconPackAdmin(admin.ModelAdmin):
    inlines = [IconPackImageInline]
    search_fields = ['name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']