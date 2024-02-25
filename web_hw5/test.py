import requests
import json


url = 'https://api.privatbank.ua/p24api/exchange_rates'
date = "20.02.2022"  
params = {'json': '', 'date': date}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
    exchange_rates = data.get('exchangeRate', [])

    data_list = []
    for rate in exchange_rates:
        data_list.append(rate.get('currency'))

    with open("data.json", "w") as json_file:
        json.dump(data_list, json_file, indent=4)

    print("успешно записаны в файл ")
else:
    print('Ошибка', response.status_code)