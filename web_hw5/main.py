import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys
import ssl

# python3 main.py 2

class CurrencyAPI:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_currency_rate(self, date):
        # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # # ssl_context.verify_mode = ssl.CERT_NONE
        # ssl_context.check_hostname = False
        async with aiohttp.ClientSession() as session:
            # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            # ssl_context.check_hostname = False  
            # ссылка с датой
            async with session.get(self.API_URL + date.strftime("%d.%m.%Y")) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Failed to fetch data: {response.status}")

    async def get_currency_rates(self, days):
        rates = {}
        current_date = datetime.now()
        # цикл по колву дней заданому от сегодня
        for i in range(days):
            date = current_date - timedelta(days=i)
            # try:
            data = await self.fetch_currency_rate(date)
            rates[date.strftime("%d.%m.%Y")] = {
                "USD": data["exchangeRate"][0]["purchaseRate"],
                "EUR": data["exchangeRate"][1]["purchaseRate"]
                }
            # except Exception as e:
            #     print(f"Error fetching data for {date.strftime('%d.%m.%Y')}: {e}")
        return rates


async def main():
    if len(sys.argv) != 2:
        print("Вкажіть кількість днів.")
    else:
        days = int(sys.argv[1])
        if days <= 10:
            api = CurrencyAPI()
            try:
                currency_rates = await api.get_currency_rates(days)
                for date, rates in currency_rates.items():
                    print(f"Date: {date}, USD: {rates['USD']}, EUR: {rates['EUR']}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Максимальна кількість днів 10.")

if __name__ == "__main__":
    asyncio.run(main())

