import requests
from datetime import datetime
API_KEY = '3dea425422-c6dcc213dc-smwu9y'

b = datetime.fromisoformat('2024-11-14 03:13:40.443689')
a = datetime.now()
print(a, '-' , b, '=', (a - b).total_seconds())
