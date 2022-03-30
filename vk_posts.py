import requests
import io
import json
from tqdm.auto import tqdm
from datetime import datetime
import pandas as pd

TOKEN = "b28e4bfeb28e4bfeb28e4bfedbb2f5a204bb28eb28e4bfed0ca66cd942802c94c2f1cb3"
VERSION = "5.130"

wall_get_url = "https://api.vk.com/method/wall.get"  # endpoint, на который мы отправляем такие запросы

data = requests.get(
    wall_get_url,
    params={
        "owner_id": -115668604,  # ID юзера
        "count": 28,  # кол-во постов
        "v": VERSION,  # версия API
        "access_token": TOKEN,  # токен доступа
        "offset": 1700  # смещение, необходимое для выборки определенного подмножества записей
    }
).json()

with io.open('vk_response_18.txt', 'w', encoding='utf-8') as output:
    output.write(json.dumps(data, ensure_ascii=False))

# я вручную меняла параметры и название итогового файла (ну 18 файлов получилось)
