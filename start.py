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
    A universal function for searching and interacting with an element.

    :param page_or_frame: page or frame
    :param selector: CSS selector or XPath
    :param is_xpath: If True, XPath is used, otherwise, a CSS selector is used.
    :param attempts: number of attempts to find an element
    :param delay: delay between attempts in seconds
    :param click: If True, there will be a click on the element
    :param get_text: If True, returns the text of the element.
    :param get_all_matches: If True, it will return all matches found.
    :param index: индекс element if several are found
    :param wait_time: wait after click (in seconds)
    :return: the found element or None
    """
    logger.info(f"🔍 Element search: {selector} (attempts: {attempts})")

    for attempt in range(attempts):
        try:
            logger.info(f"🔄 Attempt {attempt + 1}/{attempts}...")

            # Element search
            if is_xpath:
                elements = await page_or_frame.xpath(selector)
            else:
                elements = await page_or_frame.querySelectorAll(selector)

            if elements:
                logger.info(f"✅ Element found on attempt {attempt + 1}!")

                # If True, returns all found elements.
                if get_all_matches:
                    logger.info("✅ All items returned.")
                    # return elements
                    
                    if get_text:
                        list_of_texts = [await (await x.getProperty("innerText")).jsonValue() for x in elements]
                        return list_of_texts
                    else:
                        return elements
                # We check if there is an element with the specified index
                elif len(elements) > index and index >= 0:
                    element = elements[index]
                    # If a click is required, click
                    if click:
                        logger.info(f"🔘 Click on the element [{index}]...")
                        await element.click()
                        logger.info("✅ Click done.")
                        await asyncio.sleep(wait_time)                                                                                        
                    
                    if get_text:
                        logger.info(f"🔘 Getting the text...")
                        prop = await element.getProperty("innerText")
                        logger.info("✅ Text received.")
                        return await prop.jsonValue()
                    
                    return element
                elif index >= len(elements):
                    logger.error(f"❌ Index out of range.")
                    raise IndexError
                else:
                    logger.error(f"❌ Element {selector} not found among {len(elements)} found.")
                    return False

            # Waiting before next attempt
            await asyncio.sleep(delay)

        except Exception as e:
            logger.warning(f"⚠️ Search error on attempt {attempt + 1}: {e}")
    
    logger.error("❌ Element not found after all attempts.")
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
    
    with get_conn() as conn, conn.cursor() as cur:
        query = "insert into newtb (tokenname, tokenage, tokenmcap) values (%s, %s, %s)"
        list_of_tuple = []

        for i in data:
            params = []

            # Output of entered information
            print(f"{i['token']} - {i['marketCap']} - {i['age']}")
            token_name = i['token'].lower()
            params.append(token_name)

            # Age verification
            age_match = re.match(r"(\d+)([a-zA-Z]+)", f'{i['age']}')
            if not age_match:
                continue
            age, age_unit = age_match.groups()

            # Converting age to a standard format (days)
            age = int(age)
            if age_unit == 'mo':
                age = age * 30
            elif age_unit == 'y':
                age = age * 365
            params.append(age)

            # Check for capitalization
            mcap_match = re.match(r"([\d\.]+)([a-zA-Z]+)", i['marketCap'][1:])
            if not mcap_match:
                continue
            mcap, mcap_unit = mcap_match.groups()
            
            # Bringing capitalization to a unified format
            mcap = float(mcap)
            if mcap_unit == 'K':
                mcap = mcap * 1000
            elif mcap_unit == 'M':
                mcap = mcap * 1000000
            elif mcap_unit == 'B':
                mcap = mcap * 1000000000
            params.append(int(mcap))

            list_of_tuple.append(tuple(params))

        cur.executemany(query, list_of_tuple)
        
        conn.commit()
        

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
        get_text=True,
        attempts=100
    ) # Like a ,,Showing pairs 1-100 of 60,746,,

    amount_of_pages = int(''.join([x for x in text_of_pairs.split(' ')[4] if x.isdigit()]))//100+1
    
    print(amount_of_pages)
    while True:
        try:
            num = int(input(f"Enter the number of pages to process (from 1 to {amount_of_pages}): "))
            if num <= amount_of_pages and num >= 1:
                break
            else:
                continue
        except:
            print("Input error")

    await manipul(page)

    for i in range(1, num):
        base_url, query_params = URL.split('?', 1) if '?' in URL else (URL, '')
        
        new_url = f"{base_url}/page-{i+1}"
        if query_params:
            new_url += f"?{query_params}"

        page.setDefaultNavigationTimeout(0)
        await page.goto(new_url, {'waitUntil': 'domcontentloaded'})

        await manipul(page)
    
    await browser.close()


if __name__ == "__main__":
    asyncio.run(start_browser())