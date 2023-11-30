import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


async def fetch_data(session, base_url, date, currencies):
    params = {"date": date.strftime("%d.%m.%Y")}
    async with session.get(base_url, params=params) as response:
        if response.status == 200:
            data = await response.json()
            result = {'date': date.strftime("%d.%m.%Y"), 'exchangeRate': []}

            for item in data['exchangeRate']:
                if item['currency'] in currencies:
                    result['exchangeRate'].append({
                        'currency': item['currency'],
                        'sale': item['saleRate'],
                        'purchase': item['purchaseRate']
                    })

            return result

        else:
            print(f"An error occurred while retrieving data for {date}")


async def main(days):
    if days > 10:
        print("Error: The number of days cannot exceed 10.")
        return

    base_url = "https://api.privatbank.ua/p24api/exchange_rates"

    end_date = datetime.now()  # Current date
    start_date = end_date - timedelta(days=days)

    currencies = ["USD", "EUR"]
    result = []

    async with aiohttp.ClientSession() as session:
        current_date = start_date
        while current_date <= end_date:
            data = await fetch_data(session, base_url, current_date, currencies)
            if data:
                result.append(data)
            current_date += timedelta(days=1)
    print(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Enter the number of days as an argument.")
    else:
        try:
            days = int(sys.argv[1])
            asyncio.run(main(days))
        except ValueError:
            print("Error: Argument must be an integer.")