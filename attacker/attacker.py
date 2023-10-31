import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode, b64decode
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

# auth = b64encode(f'{Dependencies.LOGIN}:{Dependencies.PASS}'.encode("ascii")).decode('ascii')
#
# response = requests.get(
#     url,
#     headers={"content-type": "application/json", "Authorization": f'Basic {auth}'},
#     verify=False,
# )

response = requests.get(
    url,
    headers={"content-type": "application/json"},
    verify=False,
    auth=HTTPBasicAuth(Dependencies.LOGIN, Dependencies.PASS + '11')
)


print(response.status_code)

content = response.content.decode()
json_content = json.loads(content)
pprint(json_content, width=255)
