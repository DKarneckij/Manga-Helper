import asyncio, aiohttp, re
from bs4 import BeautifulSoup

class HPB():

    def __init__(self, name_list, isbn13_list, abe_list) -> None:
        self.name_list = name_list
        self.isbn13_list = isbn13_list
        self.abe_list = abe_list
    async def search(self):

        stock = {'website': "Half Price Books", 'name': [], 'url' : [], 'price' : [], 'abe' : []}
        
        urls = [f"https://www.hpb.com/on/demandware.store/Sites-hpb-Site/en_US/Search-Show?q={isbn}&search-button=&lang=en_US"
                for isbn in self.isbn13_list]

        # Asynchronous aiohttp requests
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(self.get_url_data(session, url))
                tasks.append(task)
            search_results = await asyncio.gather(*tasks)
            for name, url, abe, search_result in zip(self.name_list, urls, self.abe_list, search_results):
                if not search_result:
                    continue
                stock["name"].append(name)
                stock["url"].append(url) 
                stock["price"].append(search_result[0])
                stock["abe"].append(abe)

        stock["price"], stock["name"], stock["url"], stock["abe"] = zip(
            *sorted(zip(stock["price"], stock["name"], stock["url"], stock["abe"])))
        
        return stock

    
    async def get_url_data(self, session, url):
        async with session.get(url) as resp:

            result_data = await resp.read()
            soup = BeautifulSoup(result_data, "html.parser")

            target_div = soup.find_all("div", class_="mobile-list-view-pricing")

            if target_div:

                pattern = r'content="([^"]*)"'
                min_price = float("inf")

                for target in target_div:
                    regex = re.search(pattern, str(target))
                    price = float(regex.group(1).replace(",", ""))
                    min_price = min(min_price, price)

                return [min_price]