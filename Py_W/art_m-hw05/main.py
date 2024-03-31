import aiohttp, asyncio, json, sys, logging

from datetime import date, timedelta, datetime
from http import HTTPStatus


URL = "https://api.privatbank.ua/p24api/exchange_rates"

CURRENCIES = {
    "USD": "U.S. dollar",
    "EUR": "euro"
}

def format_result(result, currencies):
    return {
        result['date']:
            dict(sorted(
                {rate['currency']:
                 {
                    'sale'     : rate.get('saleRate'     , rate['saleRateNB']),
                    'purchase' : rate.get('purchaseRate' , rate['purchaseRateNB'])
                  } for rate in filter(lambda x: x['currency'] in currencies, result['exchangeRate'])}.items(), key=lambda x: currencies.index(x[0])
            ))
    }

def get_result(response, text):
    if response.status == HTTPStatus.OK:
        data = json.loads(text)
        return data

async def request(session, rate_date):
    async with session.get(f"{URL}?json&date={rate_date}") as response:
        logging.info(f"Getting data for {rate_date}")
        try:
            result = get_result(response, await response.text())
            return result
        except Exception as e:
            logging.info(e)


async def main():
    start = datetime.now()

    coroutines = list()
    results = list()

    async with aiohttp.ClientSession() as session:
        if int(sys.argv[1]) > 10:
            logging.warning("Max number of days you can fetch is 10")
            
        rate_date = date.today() - timedelta(days=sys.argv[1])
        while rate_date <= date.today():
            logging.info(rate_date)
            coroutine = request(session, rate_date)
            coroutines.append(coroutine)
            rate_date += timedelta(days=1)

        try:
            results = await asyncio.gather(*coroutines)
        except aiohttp.ClientError as e:
            logging.info(e)
            return
        except Exception as e:
            logging.info(e)
            return

    end = datetime.now()
    time = end - start
    logging.info(json.dumps(results))
    logging.info(f"Time of proccess: {time.seconds}")
    pass



if __name__ == '__main__':
    asyncio.run(main())
