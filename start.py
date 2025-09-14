import requests as r
import asyncio
import aiohttp
from pyppeteer import connect
from logger import setup_logger
import psycopg2
import dotenv
import os
import re

dotenv.load_dotenv('F:\\shitcode\\birge_api\\config.env')

URL = "https://dexscreener.com/solana?rankBy=trendingScoreH6&order=desc"

logger = setup_logger()

def get_conn():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

async def find_element(page_or_frame, selector, is_xpath=False, attempts=15, delay=1, click=False, get_text=False, get_all_matches=False, index=0, wait_time=1.5):
    """
    Универсальная функция для поиска и взаимодействия с элементом.

    :param page_or_frame: страница или фрейм
    :param selector: CSS-селектор или XPath
    :param is_xpath: если True, используется XPath, иначе — CSS-селектор
    :param attempts: количество попыток найти элемент
    :param delay: задержка между попытками в секундах
    :param click: если True, будет клик по элементу
    :param get_text: если True, вернет текст элемента
    :param get_all_matches: усли True, вернет все найденные совпадения
    :param index: индекс элемента в случае, если найдено несколько
    :param wait_time: ожидание после клика (в секундах)
    :return: найденный элемент или None
    """
    logger.info(f"🔍 Начинаем поиск элемента: {selector} (попыток: {attempts})")

    for attempt in range(attempts):
        try:
            logger.info(f"🔄 Попытка {attempt + 1}/{attempts}...")

            # Ищем элементы
            if is_xpath:
                elements = await page_or_frame.xpath(selector)
            else:
                elements = await page_or_frame.querySelectorAll(selector)

            if elements:
                logger.info(f"✅ Элемент найден на попытке {attempt + 1}!")

                # Если True, возвращает все найденные элементы
                if get_all_matches:
                    logger.info("✅ Вернули все элементы.")
                    # return elements
                    
                    if get_text:
                        list_of_texts = [await (await x.getProperty("innerText")).jsonValue() for x in elements]
                        return list_of_texts
                    else:
                        return elements
                # Проверяем есть ли элемент с указанным индесом
                elif len(elements) > index and index >= 0:
                    element = elements[index]
                    # Если требуется клик — кликаем
                    if click:
                        logger.info(f"🔘 Выполняем клик по элементу [{index}]...")
                        await element.click()
                        logger.info("✅ Клик выполнен.")
                        await asyncio.sleep(wait_time)                                                                                        
                    
                    if get_text:
                        logger.info(f"🔘 Получаем текст...")
                        prop = await element.getProperty("innerText")
                        logger.info("✅ Текст получен.")
                        return await prop.jsonValue()
                    
                    return element
                elif index >= len(elements):
                    logger.error(f"❌ Index out of range.")
                    raise IndexError
                else:
                    logger.error(f"❌ Элемент {selector} не найден среди {len(elements)} найденных.")
                    return False

            # Ожидание перед следующей попыткой
            await asyncio.sleep(delay)

        except Exception as e:
            logger.warning(f"⚠️ Ошибка поиска на попытке {attempt + 1}: {e}")
    
    logger.error("❌ Элемент не найден после всех попыток.")
    return False


async def get_ws_url():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:{os.getenv('CHROME_PORT')}/json/version') as resp:
            data = await resp.json()
            return data['webSocketDebuggerUrl']


async def manipul(page):
    await page.waitForSelector('a.ds-dex-table-row.ds-dex-table-row-top', {'timeout': 10000})


    data = await page.evaluate("""
    () => Array.from(document.querySelectorAll('a.ds-dex-table-row.ds-dex-table-row-top')).map(row => ({
    token: row.querySelector('.ds-dex-table-row-base-token-symbol')?.innerText.trim() ?? null,
    age: row.querySelector('.ds-table-data-cell.ds-dex-table-row-col-pair-age')?.innerText.trim() ?? null,
    marketCap: row.querySelector('.ds-table-data-cell.ds-dex-table-row-col-market-cap')?.innerText.trim() ?? null,
    }))
    """)
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            counter = 1
            for i in data[:100]:
                print(f'{i['token']} - {i['marketCap']} - {i['age']}')
                token_name = i['token']
                age, age_unit = re.match(r"(\d+)([a-zA-Z]+)", f'{i['age']}').groups()
                mcap, mcap_unit = re.match(r"([\d\.]+)([a-zA-Z]+)", i['marketCap'][1:]).groups()
                cur.execute(
                    "INSERT INTO newtb (tokenID, tokenname, tokenage, tokenmcap, mcap_unit, age_unit) " \
                    f"VALUES ({counter}, '{token_name}', '{age}', '{mcap}', '{mcap_unit}', '{age_unit}');"
                )
                counter+=1

    # return
    
    # for i in data:
    #     print(f'{i['token']} - {i['marketCap']} - {i['age']}')
        

async def start_browser():
    try:
        ws = await get_ws_url()
        browser = await connect(
            browserWSEndpoint=ws
        )

        page = (await browser.pages())[0]

        await page.goto(URL)

        await open_page(page, browser)

    except Exception as e:
        print(e)

async def open_page(page, browser):
    text_of_pairs = await find_element(
        page, 
        "//div[contains(@class, 'chakra-stack custom-tyhwsl')]",
        True,
        get_text=True
    ) # Like a ,,Showing pairs 1-100 of 60,746,,

    amount_of_pages = int(''.join([x for x in text_of_pairs.split(' ')[4] if x.isdigit()]))//100+1
    
    print(amount_of_pages)

    await manipul(page)

    for i in range(2, 51):
        url = URL.split('?')
        url[0] += '/page-'+str(i)
        url = '?'.join(url)

        page.setDefaultNavigationTimeout(0)
        await page.goto(url, {'waitUntil': 'domcontentloaded'})

        await manipul(page)
    
    await browser.close()

asyncio.run(start_browser())