import requests
from requests.auth import HTTPBasicAuth
from time import perf_counter
import json
from pprint import pprint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(str(__root__))

from common import Dependencies
# ~Локальный импорт

host = 'http://127.0.0.1:80'

url = f"{host}/"

tail = '1'*20

results = {}

attempts = 2000
border = attempts // 5

session = requests.Session()

response = session.get(
    url,
    headers={"content-type": "application/json"},
    verify=False,
    auth=HTTPBasicAuth('11', '11')
)


# for code in range(ord('z'), ord('a') - 1, -1):
for code in [ord('z'), ord('u')]:
    letter = chr(code)

    login = f'{letter}'

    times = []
    for att in range(attempts):
        t0 = perf_counter()
        response = session.get(
            url,
            headers={"content-type": "application/json"},
            verify=False,
            auth=HTTPBasicAuth(login, '11')
        )
        times.append(perf_counter() - t0)

    len_t = len(times)
    times.sort()
    times = times[0:attempts-border]
    t_sum = sum(times)

    # results[letter] = f'{t_sum / attempts:.5f}'

    # print(f'{login}: {t_sum / len_t:.3f}')
    print(f'{login}: {t_sum}')


print(response.status_code)
pprint(results)

content = response.content.decode()
json_content = json.loads(content)
pprint(json_content, width=255)
