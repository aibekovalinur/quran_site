import requests
from django.core.management.base import BaseCommand
from quran.models import Surah, Ayah, Reciter


class Command(BaseCommand):
    help = 'Загрузка данных Корана из API alquran.cloud'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка данных Корана...')

        # 1. Загрузка списка сур
        self.stdout.write('Загружаем список сур...')
        resp = requests.get('https://api.alquran.cloud/v1/surah', timeout=30)
        resp.raise_for_status()
        surahs_data = resp.json()['data']

        for s in surahs_data:
            Surah.objects.update_or_create(
                number=s['number'],
                defaults={
                    'name_arabic': s['name'],
                    'name_latin': s['englishName'],
                    'name_translation': s['englishNameTranslation'],
                    'revelation_type': s['revelationType'],
                    'ayah_count': s['numberOfAyahs'],
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Загружено {len(surahs_data)} сур'))

        # 2. Загрузка аятов (арабский текст)
        self.stdout.write('Загружаем аяты (арабский текст)...')
        resp = requests.get('https://api.alquran.cloud/v1/quran/quran-uthmani', timeout=60)
        resp.raise_for_status()
        arabic_data = resp.json()['data']['surahs']

        for surah_data in arabic_data:
            surah = Surah.objects.get(number=surah_data['number'])
            for ayah_data in surah_data['ayahs']:
                ayah_num = ayah_data['numberInSurah']
                Ayah.objects.update_or_create(
                    surah=surah,
                    number=ayah_num,
                    defaults={
                        'text_arabic': ayah_data['text'],
                    }
                )
            self.stdout.write(f'  Сура {surah.number} — {len(surah_data["ayahs"])} аятов')

        self.stdout.write(self.style.SUCCESS('Арабский текст загружен!'))

        # 3. Загрузка перевода (английский — Sahih International)
        self.stdout.write('Загружаем перевод (English — Sahih International)...')
        resp = requests.get('https://api.alquran.cloud/v1/quran/en.sahih', timeout=60)
        resp.raise_for_status()
        translation_data = resp.json()['data']['surahs']

        for surah_data in translation_data:
            surah = Surah.objects.get(number=surah_data['number'])
            for ayah_data in surah_data['ayahs']:
                ayah_num = ayah_data['numberInSurah']
                Ayah.objects.filter(surah=surah, number=ayah_num).update(
                    text_translation=ayah_data['text']
                )

        self.stdout.write(self.style.SUCCESS('Перевод загружен!'))

        # 4. Создание чтецов
        self.stdout.write('Добавляем чтецов...')
        reciters = [
            {
                'name': 'Mishary Rashid Alafasy',
                'name_arabic': 'مشاري راشد العفاسي',
                'identifier': 'ar.alafasy',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy',
            },
            {
                'name': 'Abdul Rahman Al-Sudais',
                'name_arabic': 'عبدالرحمن السديس',
                'identifier': 'ar.abdurrahmaansudais',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.abdurrahmaansudais',
            },
            {
                'name': 'Saud Ash-Shuraim',
                'name_arabic': 'سعود الشريم',
                'identifier': 'ar.saaborshuraym',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.saaborshuraym',
            },
            {
                'name': 'Maher Al-Muaiqly',
                'name_arabic': 'ماهر المعيقلي',
                'identifier': 'ar.maaboralmuaiqly',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.maaboralmuaiqly',
            },
            {
                'name': 'Abdul Basit Abdul Samad',
                'name_arabic': 'عبدالباسط عبدالصمد',
                'identifier': 'ar.abdulbasitmurattal',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.abdulbasitmurattal',
            },
            {
                'name': 'Saad Al-Ghamdi',
                'name_arabic': 'سعد الغامدي',
                'identifier': 'ar.saadalghamidi',
                'style': 'Murattal',
                'audio_base_url': 'https://cdn.islamic.network/quran/audio-surah/128/ar.saadalghamidi',
            },
        ]

        for r in reciters:
            Reciter.objects.update_or_create(
                identifier=r['identifier'],
                defaults=r,
            )

        self.stdout.write(self.style.SUCCESS(f'Добавлено {len(reciters)} чтецов'))
        self.stdout.write(self.style.SUCCESS('Все данные загружены успешно!'))
