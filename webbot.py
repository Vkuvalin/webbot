import requests
import json
from urllib3 import connection
import random

# Для игнорирования ошибки о просроченном сертификате
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Удаление юзер агента
def request(self, method, url, body=None, headers=None):
    if headers is None:
        headers = {}
    else:
        # Avoid modifying the headers passed into .request()
        headers = headers.copy()
    super(connection.HTTPConnection, self).request(method, url, body=body, headers=headers)

connection.HTTPConnection.request = request

listNumber = ['номер мобильного телефона']              # Вписать мобильнее номера
host = 'db.swapmap.app'
post = 'api/v1/auth/token'
post2 = 'api/v1/wallet/balance'
post3 = 'api/v1/likes/like'
post4 = 'api/v1/wallet/popullar/transfer'
userTransfer = {"count": "1.0000", "to_user_id": 12345} # Вписать user_id

for i in range(len(listNumber)):
    try:
        bon = {"phone": listNumber[i], "pin_code": "55555"}

        # Получаем токен
        def getPost(host, post, **bon):
            token = requests.post("https://" + host + "/" + post, json=bon, verify=False,
                                  headers={"User-Agent": None, })
            return json.loads(token.text)['data']['accessToken']

        tok = getPost(host, post, **bon)

        # Получение баланса
        jsonData = requests.get("https://" + host + "/" + post2, verify=False,
                                headers={"Authorization": 'Bearer ' + tok, "User-Agent": None, })
        jsonData = json.loads(jsonData.text)

        # Проверка состояния баланса
        if jsonData['data']['balance_popullar'] >= 100:
            transfer = requests.post("https://" + host + "/" + post4, json=userTransfer, verify=False,
                                 headers={"Authorization": 'Bearer ' + tok, "User-Agent": None, })
            transferresponse = json.loads(transfer.text)

        else:
            # Ставит лайки в заданном диапазоне (рандомно)
            count = 0
            while count <= 1000:
                likeData = {"obj_id": random.randint(50000, 65000), "type": "note"}
                like = requests.post("https://" + host + "/" + post3, json=likeData, verify=False,
                                     headers={"Authorization": 'Bearer ' + tok, "User-Agent": None, })
                likeresponse = json.loads(like.text)['code_http']

                if likeresponse == 200:
                    print(likeresponse)
                    count += 1
                else:
                    print('Не 200')
    except:
        print('Ошибочка :(')
    finally:
        print(str(listNumber[i]) + ' - номер отработан!', end='\n')