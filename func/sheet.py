import gspread, asyncio, re, json, aiohttp, time, os
from bs4 import BeautifulSoup
from func.abebooks import AbeBooks
from func.embed import * 

class sheet():
    
    sa = gspread.service_account(filename="google-credentials.json")
    sh = sa.open("HPB")
    wks = sh.worksheet("Manga")
    
    def __init__(self):
        self.broken_links = []

    async def search(self):

        num_col = 5
        names, urls = sheet.wks.col_values(num_col), sheet.wks.col_values(num_col+1)
        res = {'name': [], 'url' : [], 'price' : [], 'abe' : [], 'isbn' : []}

        # Asynchronous aiohttp requests
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(sheet.get_url_data(self, session, url))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            for name, url, result in zip(names, urls, result):
                if not result:
                    continue
                res["name"].append(name); res["url"].append(url) 
                res["price"].append(result[0]); res['isbn'].append(result[1])

        helper.sort_by_price(res)
        print("----Starting AbeBooks Search----")
        helper.add_abe(res)
        if os.path.isfile("stock_info.json"):
            helper.add_new(res)
        print(res["new"])
        helper.store_stock(res)

        return res

    # Helper Method for Asynchronous Searching
    # Completes Requests and Returns Price
    async def get_url_data(self, session, url):
        async with session.get(url) as resp:

            result_data = await resp.read()
            soup = BeautifulSoup(result_data, "html.parser")

            if helper.is_broken_link(soup):
                self.broken_links.append(url)

            soup_tag = str(soup.find("div", {"class": "text-price-large"}))

            if soup_tag != 'None': 
                regex = re.search('"text-price-large">\$(.+?) <span', soup_tag)
                price = float(regex.group(1))
                isbn = helper.get_isbn(soup)
                return [price, isbn]

    # Sends the broken links in the Google Sheet
    def show_broken_links(self):
        for i in range(len(self.broken_links)):
            sheet.wks.update_cell(i+1,1,self.broken_links[i])

class helper():

    # Finds price from sectioned soup tag
    def find_price(soup_tag):
        regex = re.search('"text-price-large">\$(.+?) <span', soup_tag)
        return float(regex.group(1))
    
    # Checks if a link is broken
    def is_broken_link(soup):
        soup_tag = str(soup.find("div", {"class": "big-blue-header-area mbn"}))
        if soup_tag != 'None':
            return True
        else: return False

    # Gets the ISBN during search        
    def get_isbn(soup):
        soup_tag = str(soup.find_all("div", {"class": "small-6 columns"})[1])
        isbn = re.search('ISBN:</strong> (.+?)</li', soup_tag)
        if isbn:
            return isbn.group(1)
        else: return 'None'
    
    # Loop to add AbeBooks price for all in-stock items
    def add_abe(res):
        for isbn in res["isbn"]:
            price = helper.get_abe(isbn)
            print(price)

            if price == "HTTP 429":
                break

            res['abe'].append(price)
            time.sleep(1)

    # Gets price of book from AbeBooks using an ISBN
    def get_abe(isbn):

        if isbn == 'None':
            return 'No ISBN'

        abe = AbeBooks().getPriceByISBN(isbn)

        if abe == None:
            return "HTTP 429"

        if abe['success']:
            available = [abe['pricingInfoForBestNew'], abe['pricingInfoForBestUsed']]
            available = [float(x['bestPriceInPurchaseCurrencyWithCurrencySymbol'][4:].replace(',','')) for x in available if x is not None]
            return (min(available))
        return '--'

    # Sorts the results by price
    def sort_by_price(res):
        res["price"], res["name"], res["url"], res["isbn"] = zip(
            *sorted(zip(res["price"], res["name"], res["url"], res["isbn"])))

    def add_new(new_stock):
        new_stock["new"] = []


        with open("stock_info.json", "r") as f:
            old_stock = json.load(f)
        
        for name in new_stock["name"]:
            if name not in old_stock["name"]:
                new_stock["new"].append(name)

    # Dump Stock Into a .json to be used by the pr() method
    def store_stock(res):
        new_json = json.dumps(res)
        with open('stock_info.json', 'w') as f:
            f.write(new_json)