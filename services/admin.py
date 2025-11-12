from django.contrib import admin

from .models import Service, Master


# 🔹 Service modeli uchun admin sozlamalari
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


# 🔹 Master modeli uchun admin sozlamalari
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'experience', 'created_at')
    list_filter = ('service', 'experience')
    search_fields = ('name', 'phone')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')



