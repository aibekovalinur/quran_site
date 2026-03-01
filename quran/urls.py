from django.urls import path
from . import views

app_name = 'quran'

urlpatterns = [
    path('', views.index, name='index'),
    path('surahs/', views.surah_list, name='surah_list'),
    path('surah/<int:surah_number>/', views.surah_detail, name='surah_detail'),
    path('listen/', views.listen, name='listen'),
    path('api/search/', views.search_api, name='search_api'),
]
