import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys
import json

# python3 main.py 2
# python3 main.py 2 PLN


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

    async def get_currency_rates(self, days):
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
    if len(sys.argv) not in [2,3]:
        print("Вкажіть кількість днів.")
    else:
        days = int(sys.argv[1])
        if len(sys.argv) > 2:
            currency = sys.argv[2]
            currency.upper()
        else:
            currency = None
        filename = 'data.json'
        if days <= 10:
            api = CurrencyAPI()
            try:
                currency_rates = await api.get_currency_rates(days)
                await api.write_to_json_file(currency_rates, filename)
                for date, rates in currency_rates.items():
                    for rate, data in rates.items():
                        if rate in ['USD', 'EUR'] or rate == currency:
                            print(f"{date}, {rate}: sale = {data['sale']}, purchase = {data['purchase']},")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Максимальна кількість днів - 10.")

if __name__ == "__main__":
    asyncio.run(main())
