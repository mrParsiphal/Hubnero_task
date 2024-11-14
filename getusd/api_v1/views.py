from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from datetime import datetime, timedelta
import requests

from .models import ExchangeRates


@csrf_exempt
def getExchangeRate(request) -> JsonResponse:
    '''
    Проводит проверку на время последнего запроса (среди всех запросов!),
    если прошло больше 10 сек. отправляет запрос на внешее API и получает данные о текущем курсе USD/RUB
    и отправляет последние 10 (если запросов меньше, то и выведет меньше) результатов запроса.

    :param request
    :return: 10 или меньше последних курсов USD/RUB или отработку ошибки.
    '''
    if request.method != 'GET':
        return JsonResponse({"error": "invalid method"}, status=403)
    coldown = (datetime.now() - ExchangeRates.objects.latest("date").date).total_seconds()
    if coldown > 10:
        cur_ex_rate = requests.get(f'https://api.fastforex.io/fetch-one?from=USD&to=RUB&api_key={settings.API_KEY}')
        query = ExchangeRates()
        query.base = cur_ex_rate.json()['base']
        query.relative = list(cur_ex_rate.json()['result'].keys())[0]
        query.value = list(cur_ex_rate.json()['result'].values())[0]
        query.date_update = datetime.fromisoformat(cur_ex_rate.json()['updated']) + timedelta(hours=3)
        query.save()
        query = ExchangeRates.objects.all().order_by('-pk')[:10]
        result = []
        for row in query:
            record = {}
            record['base'] = row.base
            record['relative'] = row.relative
            record['value'] = row.value
            record['date_update'] = row.date_update
            record['date_query'] = row.date
            result.append(record)
        return JsonResponse({"Exchange rate USD/RUB": result})
    return JsonResponse({'error': f'cooldown {10 - coldown}s'})

