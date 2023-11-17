import requests
from requests.auth import HTTPBasicAuth
from time import perf_counter
import json
from typing import Tuple, Union, Literal
from pprint import pprint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Локальный импорт:
import sys
from pathlib import Path
__root__ = Path(__file__).absolute().parent.parent
sys.path.append(str(__root__))

from config import Config
# ~Локальный импорт


def ranger():
    for rng in (
            range(ord('A'), ord('Z') + 1),
            range(ord('_'), ord('_') + 1),
            range(ord('a'), ord('z') + 1),
            range(ord('0'), ord('9') + 1)
    ):
        for code in rng:
            yield chr(code)


def pick_a_letter(affix: str, find_at_login: bool = True, prev_delta: float = 0.0) \
        -> Tuple[Union[str, Literal[False]], float]:
    """ По выборке 80% наименьших результатов считаем максимальную и среднюю продолжительность поиска:
        максимум даст новую букву, разница между максимумом и средним даст ожидаемую дельту, которую передадим
        следующей итерации поиска.
        Если текущая дельта в 10 (100?) раз меньше предыдущей, значит на данной итерации нет выделенного максимума и,
        мы, соответственно, дошли до конца поисковой строки.
        Возвращаем найденную букву (False, если дошли до конца) и текущую дельту
    """

    config = Config.get_instance()

    attempts = 100
    border = attempts // 5

    session = requests.Session()

    for letter in ranger():
        print(letter, end=' ')

    # Прогрев
    response = session.get(
        config.fastapi.dsn,
        headers={"content-type": "application/json"},
        verify=False,
        auth=HTTPBasicAuth(config.fastapi.login, config.fastapi.password)
    )

    return False, 0.0


if __name__ == '__main__':

    config = Config.get_instance()

    tail = '1'*20

    results = {}

    attempts = 100
    border = attempts // 5

    session = requests.Session()

    for letter in ranger():
        print(letter, end=' ')



    # Прогрев
    response = session.get(
        config.fastapi.dsn,
        headers={"content-type": "application/json"},
        verify=False,
        auth=HTTPBasicAuth(config.fastapi.login, config.fastapi.password)
    )

    print(response.status_code, response.text)
    exit(0)

    # for code in range(ord('z'), ord('a') - 1, -1):
    for code in [ord('z'), ord('u')]:
        letter = chr(code)

        login = f'{letter}'

        times = []
        for att in range(attempts):
            t0 = perf_counter()
            response = session.get(
                config.fastapi.dsn,
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
