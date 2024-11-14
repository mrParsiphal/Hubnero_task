from django.db import models


class ExchangeRates(models.Model):
    base = models.CharField(max_length=3, verbose_name="Базовая валюта")
    relative = models.CharField(max_length=3, verbose_name="Валюта котировки")
    value = models.DecimalField(max_digits=7, decimal_places=5, verbose_name="Курс")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата запроса")
    date_update = models.DateTimeField(verbose_name="Дата обновления курса")

    def __str__(self):
        return f'{self.base}/{self.relative}'

    class Meta:
        db_table = "ExchangeRates"
        verbose_name = "Курс валют"
        verbose_name_plural = "Курсы валют"
