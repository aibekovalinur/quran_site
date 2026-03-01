from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Surah, Ayah, Reciter


def index(request):
    """Главная страница"""
    surahs = Surah.objects.all()[:10]
    reciters = Reciter.objects.all()
    total_surahs = Surah.objects.count()
    total_ayahs = Ayah.objects.count()
    return render(request, 'quran/index.html', {
        'surahs': surahs,
        'reciters': reciters,
        'total_surahs': total_surahs,
        'total_ayahs': total_ayahs,
    })


def surah_list(request):
    """Список всех сур"""
    query = request.GET.get('q', '')
    if query:
        surahs = Surah.objects.filter(
            name_latin__icontains=query
        ) | Surah.objects.filter(
            name_translation__icontains=query
        ) | Surah.objects.filter(
            name_arabic__icontains=query
        )
    else:
        surahs = Surah.objects.all()
    return render(request, 'quran/surah_list.html', {
        'surahs': surahs,
        'query': query,
    })


def surah_detail(request, surah_number):
    """Чтение суры — аяты"""
    surah = get_object_or_404(Surah, number=surah_number)
    ayahs = surah.ayahs.all()
    reciters = Reciter.objects.all()

    prev_surah = Surah.objects.filter(number=surah_number - 1).first()
    next_surah = Surah.objects.filter(number=surah_number + 1).first()

    return render(request, 'quran/surah_detail.html', {
        'surah': surah,
        'ayahs': ayahs,
        'reciters': reciters,
        'prev_surah': prev_surah,
        'next_surah': next_surah,
    })


def listen(request):
    """Страница прослушивания"""
    reciters = Reciter.objects.all()
    surahs = Surah.objects.all()
    return render(request, 'quran/listen.html', {
        'reciters': reciters,
        'surahs': surahs,
    })


def search_api(request):
    """API для поиска сур (AJAX)"""
    query = request.GET.get('q', '')
    if len(query) < 1:
        return JsonResponse({'results': []})

    surahs = Surah.objects.filter(
        name_latin__icontains=query
    ) | Surah.objects.filter(
        name_translation__icontains=query
    )
    results = [{
        'number': s.number,
        'name_arabic': s.name_arabic,
        'name_latin': s.name_latin,
        'name_translation': s.name_translation,
        'ayah_count': s.ayah_count,
    } for s in surahs[:20]]

    return JsonResponse({'results': results})
