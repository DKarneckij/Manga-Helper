import asyncio, aiohttp, re, json
from bs4 import BeautifulSoup

class HPB():

    def __init__(self, name_list, isbn13_list, abe_list) -> None:
        # Initialize the class with input data lists
        self.name_list = name_list
        self.isbn13_list = isbn13_list
        self.abe_list = abe_list

    async def search(self):

        # Prepare a dictionary to store search results
        stock = {'website': "Half Price Books", 'name': [], 'url' : [], 'price' : [], 'abe' : []}
        
        # Generate URLs for each ISBN
        urls = [f"https://www.hpb.com/on/demandware.store/Sites-hpb-Site/en_US/Search-Show?q={isbn}&search-button=&lang=en_US"
                for isbn in self.isbn13_list]

        # Asynchronous aiohttp requests
        async with aiohttp.ClientSession() as session:

            tasks = []
            # Create tasks for fetching data from each URL
            for url in urls:
                task = asyncio.ensure_future(self.get_url_data(session, url))
                tasks.append(task)

            # Gather results from all tasks asynchronously
            search_results = await asyncio.gather(*tasks)

            # Process search results and populate stock dictionary
            for name, url, abe, search_result in zip(self.name_list, urls, self.abe_list, search_results):
                if not search_result:
                    continue
                stock["name"].append(name)
                stock["url"].append(url) 
                stock["price"].append(search_result[0])
                stock["abe"].append(abe)

        # Sort results based on price
        stock["price"], stock["name"], stock["url"], stock["abe"] = zip(
            *sorted(zip(stock["price"], stock["name"], stock["url"], stock["abe"])))
        
        # Store stock
        new_json = json.dumps(stock)
        with open('data/halfpricebooks_stock.json', 'w') as f:
            f.write(new_json)
        
        return stock

    
    async def get_url_data(self, session, url):

        # Fetch data from a URL using aiohttp
        async with session.get(url) as resp:
            
            result_data = await resp.read()
            # Parse HTML data using BeautifulSoup
            soup = BeautifulSoup(result_data, "html.parser")

            # Find target div elements containing pricing information
            target_div = soup.find_all("div", class_="mobile-list-view-pricing")

            if target_div:

                pattern = r'content="([^"]*)"'
                min_price = float("inf")

                # Extract pricing information
                for target in target_div:
                    regex = re.search(pattern, str(target))
                    price = float(regex.group(1).replace(",", ""))
                    min_price = min(min_price, price)

                return [min_price]