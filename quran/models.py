from django.db import models


class Surah(models.Model):
    """Сура Корана"""
    number = models.IntegerField(unique=True, verbose_name='Номер суры')
    name_arabic = models.CharField(max_length=100, verbose_name='Название (арабский)')
    name_latin = models.CharField(max_length=100, verbose_name='Название (латиница)')
    name_translation = models.CharField(max_length=200, verbose_name='Перевод названия')
    revelation_type = models.CharField(max_length=20, verbose_name='Место ниспослания')
    ayah_count = models.IntegerField(verbose_name='Количество аятов')

    class Meta:
        ordering = ['number']
        verbose_name = 'Сура'
        verbose_name_plural = 'Суры'

    def __str__(self):
        return f'{self.number}. {self.name_latin} ({self.name_arabic})'


class Ayah(models.Model):
    """Аят Корана"""
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='ayahs')
    number = models.IntegerField(verbose_name='Номер аята')
    text_arabic = models.TextField(verbose_name='Текст (арабский)')
    text_translation = models.TextField(verbose_name='Перевод', blank=True, default='')

    class Meta:
        ordering = ['surah__number', 'number']
        unique_together = ['surah', 'number']
        verbose_name = 'Аят'
        verbose_name_plural = 'Аяты'

    def __str__(self):
        return f'Сура {self.surah.number}, Аят {self.number}'


class Reciter(models.Model):
    """Чтец Корана"""
    name = models.CharField(max_length=200, verbose_name='Имя')
    name_arabic = models.CharField(max_length=200, verbose_name='Имя (арабский)', blank=True, default='')
    identifier = models.CharField(max_length=100, unique=True, verbose_name='Идентификатор')
    style = models.CharField(max_length=100, verbose_name='Стиль чтения', blank=True, default='')
    audio_base_url = models.URLField(verbose_name='Базовый URL аудио')

    class Meta:
        verbose_name = 'Чтец'
        verbose_name_plural = 'Чтецы'

    def __str__(self):
        return self.name

    def get_surah_audio_url(self, surah_number):
        """Получить URL аудио для конкретной суры"""
        return f'{self.audio_base_url}/{surah_number:03d}.mp3'
