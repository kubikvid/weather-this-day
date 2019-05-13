#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from urllib import parse
import asyncio
from typing import Iterable, Generator, List, Tuple, Dict
from datetime import datetime
from sys import argv

from bs4 import BeautifulSoup
import aiohttp
import pymongo

if len(argv) < 2:
    print("Please provide a city ID from Gismeteo site")
    exit(0)

HOST = "www.gismeteo.ru"
PATH = "/diary/{city}".format(city=argv[1])

YEARS = range(1997, 2019)
MONTHS = range(1, 13)

MONGO_HANDLER = pymongo.MongoClient('localhost')

DB = MONGO_HANDLER.get_database('weather')

COLLECTION = DB['history']


def get_full_path(year: int, month: int):
    full_path = "/".join(map(str, (PATH, year, month)))
    return parse.urljoin(HOST, full_path)


async def get_weather_html(year: int, month: int):
    full_path = get_full_path(year, month)
    url = ''.join(("https://", HOST, full_path))
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'
                },
                ssl=True
        ) as resp:
            t = await get_weather_data_from_html(resp.content.read_nowait().decode("utf_8"), year, month)
            inserted = await insert_weather_data(t)
            return resp


def _get_combinations(years: Iterable, months: Iterable) -> Generator:
    """Получить все комбинации года и месяца
    :param years:
    :param months:
    :return:
    """
    for year in years:
        for month in months:
            yield (year, month)


async def get_weather_data_from_html(html_str: str, year: int, month: int):
    doc = BeautifulSoup(html_str, features="lxml")
    temperatures = [e.text for e in doc.find_all("td", {"class": "first_in_group"})]
    res = []
    day = 1
    for i in range(0, len(temperatures), 2):
        try:
            doc = (datetime(year, month, day), {"d": int(temperatures[i]), "n": int(temperatures[i + 1])})
        except ValueError as ve:
            doc = (datetime(year, month, day), {"d": "nd", "n": "nd"})
        finally:
            # doc = {datetime(year, month, day): {}}
            res.append(doc)
            day += 1
    return res


async def insert_weather_data(weather_data: List[Tuple[datetime, Dict[str, int]]], city_id: int = 4720):
    """[(datetime(2013, 4, 1), {temperature: {'n': -1, 'd': 5} } ), ...]
    :param weather_data:
    :param city_id:
    :return:
    """
    # items = (wd.items() for wd in weather_data)
    if not weather_data:
        return 0
    docs = ({
        "date": key,
        "city_id": city_id,
        "temperature": {
            "n": value.get("n"),
            "d": value.get("d")
        }
    } for key, value in weather_data)

    insert_many = COLLECTION.insert_many(docs)
    return len(insert_many.inserted_ids)


async def main():
    await asyncio.gather(*[
        get_weather_html(year, month) for year, month in _get_combinations(YEARS, MONTHS)
    ])


if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    print(f"Finished in {(datetime.now() - start).total_seconds()} sec")
