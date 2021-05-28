from django.contrib import admin
from service import models
from django.utils.safestring import mark_safe


@admin.register(models.Border)
class BorderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'colorable', 'thumb']
    readonly_fields = ('thumb',)

    @staticmethod
    def thumb(obj):
        return mark_safe(f"<img src='{obj.image.url}'  width='50' height='50' />")


@admin.register(models.Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'max_users_count', 'start_date', 'end_date', 'available_users_count']
    readonly_fields = ('available_users_count',)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.SettingJson)
class SettingJsonAdmin(admin.ModelAdmin):
    list_display = ['data']
