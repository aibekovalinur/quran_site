from django.contrib import admin
from .models import Surah, Ayah, Reciter


@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ['number', 'name_arabic', 'name_latin', 'name_translation', 'revelation_type', 'ayah_count']
    search_fields = ['name_arabic', 'name_latin', 'name_translation']


@admin.register(Ayah)
class AyahAdmin(admin.ModelAdmin):
    list_display = ['surah', 'number', 'text_arabic']
    list_filter = ['surah']


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_arabic', 'identifier']
