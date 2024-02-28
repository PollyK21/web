import aiohttp
import asyncio
from datetime import datetime, timedelta
import json


class CurrencyAPI:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_currency_rate(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL + date.strftime("%d.%m.%Y")) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Failed to fetch data: {response.status}")

    async def get_currency_rates(self, days, curency_list):
        current_date = datetime.now()
        all_rates = {}
        # цикл по колву дней заданому от сегодня
        for i in range(days):
            date = current_date - timedelta(days=i)
            try:
                data = await self.fetch_currency_rate(date)
                exchange_rates = data.get('exchangeRate', [])
                rates = {}
                for rate in exchange_rates:
                    if rate["currency"] in ['USD', 'EUR'] or rate["currency"] in curency_list:
                        rates[rate["currency"]] = {"sale": rate["saleRateNB"], "purchase": rate["purchaseRateNB"]}
            except Exception as e:
                print(f"Error fetching data for {date.strftime('%d.%m.%Y')}: {e}")
            all_rates[date.strftime("%d.%m.%Y")] = rates
        return all_rates

    async def write_to_json_file(self, data_list, filename):
        with open(filename, "w") as json_file:
            json.dump(data_list, json_file, indent=4)
        print("The data was successfully written to the JSON file.")


async def main():
    filename = 'data.json'
    try:
        answer = int(input("Вкажіть кількість днів для статистики (не більше 10) - "))
        another = input("Бажаєте додати валюти до переліку?(USD та EUR за замовченням) Y/N - ").upper()
        if another == "Y":
            currency = input("Вкажіть додаткові валюти через пробіл - ").upper()
            curency_list = currency.split()
        else:
            curency_list = []
        if 1 <= answer <= 10:
            api = CurrencyAPI()
            try:
                currency_rates = await api.get_currency_rates(answer, curency_list)
                await api.write_to_json_file(currency_rates, filename)
                for date, rates in currency_rates.items():
                    for rate, data in rates.items():
                        print(f"{date}, {rate}: sale = {data['sale']}, purchase = {data['purchase']},")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Кількість днів має бути в діапазоні від 1 до 10")
    except ValueError:
        print("Ошибка: введите целое число")

if __name__ == "__main__":
    asyncio.run(main())
