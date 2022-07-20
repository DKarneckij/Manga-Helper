import gspread, asyncio, re, json, aiohttp
from bs4 import BeautifulSoup

sa = gspread.service_account(filename="credentials.json")
sh = sa.open("HPB")
wks = sh.worksheet("Manga")


async def find_stock():
    print('-----Beginning Search-----')

    names, urls = wks.col_values(5), wks.col_values(6)
    res = {'n': [], 'u' : [], 'p' : []}

    # Asynchronous aiohttp requests
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(get_url_data(session, url))
            tasks.append(task)
        prices = await asyncio.gather(*tasks)

        for name, url, price in zip(names, urls, prices):
            if price == None:
                continue
            res["n"].append(name)
            res["u"].append(url)
            res["p"].append(price)

    # Sort result by price
    res["p"], res["n"], res["u"] = zip(*sorted(zip(res["p"], 
                                                    res["n"], res["u"])))

    # Dump res into a .json to be used by the pr() method
    new_json = json.dumps(res)
    with open('stock_info.json', 'w') as f:
        f.write(new_json)
    print("-----Done searching-----")

    return res

# Helper Method for find_stock
# Iterates through tasks and retrieves the price
async def get_url_data(session, url):

    async with session.get(url) as resp:

        result_data = await resp.read()
        soup = BeautifulSoup(result_data, "html.parser")
        soup_tag = str(soup.find("div", {"class": "text-price-large"}))

        if soup_tag != 'None': 
            regex = re.search('"text-price-large">\$(.+?) <span', soup_tag)
            price = float(regex.group(1))
            return price 

