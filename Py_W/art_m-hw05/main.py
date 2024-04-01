import aiohttp, asyncio, json, sys

from datetime import date, timedelta, datetime


URL = "https://api.privatbank.ua/p24api/exchange_rates"

CURRENCIES = {
    "USD": "U.S. dollar",
    "EUR": "euro"
}


async def request(session, rate_date):
    date = rate_date.strftime("%d.%m.%Y")
    async with session.get(f"{URL}?json&date={date}") as response:
        print(f"Getting data for {rate_date}...")
        try:
            data = await response.json()
            rates = dict()
            for rate in data.get('exchangeRate', []):
                if rate.get('currency') in CURRENCIES:
                    rates[rate.get('currency')] = {
                        'sale': rate.get('saleRate'),
                        'purchase': rate.get('purchaseRate')}
            return {str(rate_date): rates}
        except Exception as e:
            print(e)


async def main():
    start = datetime.now()

    coroutines = list()
    results = list()

    async with aiohttp.ClientSession() as session:
        if int(sys.argv[1]) > 10:
            print("Max number of days you can fetch is 10")
            
        rate_date = date.today() - timedelta(days=int(sys.argv[1])-1)
        while rate_date <= date.today():
            coroutine = request(session, rate_date)
            coroutines.append(coroutine)
            rate_date += timedelta(days=1)
        try:
            results = await asyncio.gather(*coroutines)
            ex_rates = json.dumps(results, indent=2, ensure_ascii=False)
        except aiohttp.ClientError as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return

    end = datetime.now()
    time = end - start
    print(ex_rates)
    print(f"Time of proccess: {time.seconds} seconds")


if __name__ == '__main__':
    asyncio.run(main())
