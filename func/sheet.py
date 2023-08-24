import gspread, asyncio, re, json, aiohttp, time, os, requests
from bs4 import BeautifulSoup
from func.abebooks import AbeBooks

class sheet():
    
    sa = gspread.service_account(filename="google-credentials.json")
    sh = sa.open("Manga")
    wks = sh.worksheet("Manga")
    LIST_COL = 1
    NEW_COL = 6
    LOW_COL = 9
    HIGH_COL = 13
    
    def __init__(self):
        self.broken_links = []
        self.removed_list = []

    def get_names(self):
        return self.wks.col_values(self.LIST_COL)[2:]
    
    def get_isbn13s(self):
        return self.wks.col_values(self.LIST_COL + 2)[2:]

    def get_abes(self):
        return self.wks.col_values(self.LIST_COL + 3)[2:]
    
    def update_abe(self):

        # Update Abe
        isbns = self.wks.col_values(self.LIST_COL+2)[2:]
        abes = []

        error = False
        # Get the new list of AbeBooks prices
        for isbn in isbns:
            if not error:
                time.sleep(1.5)
                abe = self._get_abe(isbn)
                if abe == "Error":
                    error = True
            else: 
                abe = "Error"
            print(isbn)
            abes.append([abe])

        if not error:
            self.wks.update(f'D3:D{len(isbns) + 2}', abes, value_input_option='RAW')

        names = self.wks.col_values(self.LIST_COL)[2:]
        urls = self.wks.col_values(self.LIST_COL+1)[2:]
        abes = self.wks.col_values(self.LIST_COL+3)[2:]

        low, high = [], []
        for name, url, abe in zip(names, urls, abes):

            if abe == "No ISBN" or abe == "Error": continue

            if abe == "--" or float(abe) >= 100:
                high.append([name, url, abe])
            elif float(abe) <= 25:
                low.append([name, url, abe])

        # Sort by price (abe value)
        low.sort(key=lambda x: float(x[2]))
        high.sort(key=lambda x: float(x[2]) if x[2].replace(".", "", 1).isdigit() else float('10000'))
        
        # Update Low
        self.wks.update(f'I3:K{len(low) + 2}', low, value_input_option='RAW')

        # Update High
        self.wks.update(f'M3:O{len(high) + 2}', high, value_input_option='RAW')

    async def add_new(self):

        # Retrieve new_names and new_urls from the worksheet
        new_names, new_urls = self.wks.col_values(self.NEW_COL)[2:], self.wks.col_values(self.NEW_COL+1)[2:]

        new_items = []  # List to hold dictionaries of items

        async with aiohttp.ClientSession() as session:
            # Loop through new_names and new_urls to fetch data and create items
            for name, url in zip(new_names, new_urls):
                async with session.get(url) as response:
                    result_data = await response.read()
                    soup = BeautifulSoup(result_data, "html.parser")
                    isbn = self._get_isbn(soup)

                    # Create a dictionary for the item
                    item = {
                        "name": name,
                        "url": url,
                        "isbn": isbn,
                        "abe": "-"
                    }
                    new_items.append(item)

        error = False
        # Update the abe field for each item, handling potential errors
        for item in new_items:
            if not error:
                time.sleep(1.5)
                abe = self._get_abe(item["isbn"])
                if abe == "Error":
                    error = True
            else: 
                abe = "Error"
            print(f"{item['name']} : {abe}")
            item["abe"] = abe

        # Prepare data for updating the worksheet
        names = self.wks.col_values(self.LIST_COL)[2:]
        urls = self.wks.col_values(self.LIST_COL+1)[2:]
        isbns= self.wks.col_values(self.LIST_COL+2)[2:]
        abes = self.wks.col_values(self.LIST_COL+3)[2:]

        for item in new_items:
            names.append(item["name"])
            urls.append(item["url"])
            isbns.append(item["isbn"])
            abes.append(item["abe"])

        # Sort based on names
        pairs = list(zip(names, urls, isbns, abes))
        sorted_pairs = sorted(pairs, key=lambda pair: pair[0])
        values = [list(pair) for pair in sorted_pairs]

        try:
            # Update the worksheet
            self.wks.update(f'A3:D{len(values) + 2}', values, value_input_option='RAW')

            # Clear specific columns
            self.wks.batch_clear(['F3:F'])
            self.wks.batch_clear(['G3:G'])
        except Exception as e:
            print("Error updating data:", e)


    async def search(self, list_choice):

        column_indices = {
            "All": (sheet.LIST_COL, sheet.LIST_COL + 1, sheet.LIST_COL + 3),
            "Expensive": (sheet.HIGH_COL, sheet.HIGH_COL + 1, sheet.HIGH_COL + 2)}
        
        col_idx_names, col_idx_urls, col_idx_abes = column_indices[list_choice]

        names = self.wks.col_values(col_idx_names)[2:]
        urls = self.wks.col_values(col_idx_urls)[2:]
        abes = self.wks.col_values(col_idx_abes)[2:]
        

        in_stock = {'name': [], 'url' : [], 'price' : [], 'abe' : []}

        # Asynchronous aiohttp requests
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(sheet.get_url_data(self, session, url))
                tasks.append(task)
            search_results = await asyncio.gather(*tasks)
            for name, url, abe, search_result in zip(names, urls, abes, search_results):
                if not search_result:
                    continue
                in_stock["name"].append(name)
                in_stock["url"].append(url) 
                in_stock["price"].append(search_result[0])
                in_stock["abe"].append(abe) 

        print(in_stock)

        # Sort In Stock Items by Price
        self._sort_by_price(in_stock)

        # Handle Broken Links if any 
        self._show_broken_links()

        # Find the real expensive stuff
        self._add_expensive(in_stock)

        # Find all new manga that cost less than 15$, and not include those that have already been found
        if os.path.isfile("stock_info.json"):
            self._add_new_stock(in_stock)
            # Merge the expensive stock with the previous stock
            if list_choice == "Expensive":
                in_stock = self._merge_stock(in_stock)

        self._store_stock(in_stock)

        return in_stock

    def _merge_stock(self, in_stock):

        with open("stock_info.json", "r") as f:
            old_stock = json.load(f)

        for i, name in enumerate(in_stock["new"]):
            if name in old_stock:
                index = old_stock["name"].index(name)
                old_stock["price"][index] = in_stock["price"][i]
            else:
                old_stock["name"].append(name)
                old_stock["url"].append(in_stock["url"][i])
                old_stock["price"].append(in_stock["price"][i])
                old_stock["abe"].append(in_stock["abe"][i])
        
        return old_stock


    # Helper Method for Asynchronous Searching
    # Completes Requests and Returns Price
    async def get_url_data(self, session, url):
        async with session.get(url) as resp:

            result_data = await resp.read()
            soup = BeautifulSoup(result_data, "html.parser")

            if self._is_broken_link(soup):
                self.broken_links.append(url)

            soup_tag = str(soup.find("div", {"class": "text-price-large"}))
            print(soup_tag)

            if soup_tag != 'None': 
                regex = re.search('"text-price-large">\$(.+?) <span', soup_tag)
                price = None
                if len(regex.group(1)) > 6:
                    price = float(regex.group(1).replace(",", ""))
                else:
                    price = float(regex.group(1))
                print(price)
                return [price]

    # Delete a list of items from the worksheet
    def delete_items(self, delete_list):

        # Deletes item from column
        def del_at_index(index, col):
            requests = [ 
                {
                    'deleteRange': {
                        'range': {
                            'sheetId': sheet.wks._properties['sheetId'],
                            'startRowIndex': index-1,
                            'endRowIndex': index,
                            'startColumnIndex': col-1,
                            'endColumnIndex': col+3,
                        },
                        'shiftDimension': 'ROWS',
                    }
                }
            ]
            sheet.sh.batch_update({'requests': requests})

        all_names = self.wks.col_values(self.LIST_COL)
        cheap_names = self.wks.col_values(self.LOW_COL)
        for delete_name in delete_list:
            for index, name in enumerate(all_names):
                if name.lower() == delete_name:
                    deleted = all_names.pop(index)
                    print(f"Deleted {deleted} from All")
                    del_at_index(index + 1, self.LIST_COL)
                    break

            for index, name in enumerate(cheap_names):
                if name.lower() == delete_name:
                    deleted = cheap_names.pop(index)
                    print(f"Deleted {deleted} from Cheap")
                    del_at_index(index + 1, self.LOW_COL)
                    break
            self.removed_list.append(delete_name)

        with open("stock_info.json", "r") as f:
            stock = json.load(f)
        
        for delete_name in delete_list:
            for index, name in enumerate(stock["name"]):
                if name.lower() == delete_name:
                    stock["name"].pop(index)
                    stock["price"].pop(index)
                    stock["abe"].pop(index)
                    stock["url"].pop(index)

        
        new_json = json.dumps(stock)
        with open('stock_info.json', 'w') as f:
            f.write(new_json)

    # Gets the ISBN during search        
    def _get_isbn(self, soup):
        soup_tag = str(soup.find_all("div", {"class": "small-6 columns"})[1])
        isbn = re.search('ISBN:</strong> (.+?)</li', soup_tag)
        if isbn:
            return isbn.group(1)
        else: return 'None'

    # Gets price of book from AbeBooks using an ISBN
    def _get_abe(self, isbn):

        if isbn == 'None':
            return 'No ISBN'

        abe = AbeBooks().getPriceByISBN(isbn)

        if abe == None:
            return "Error"

        if abe['success']:
            available = [abe['pricingInfoForBestNew'], abe['pricingInfoForBestUsed']]
            available = [float(x['bestPriceInPurchaseCurrencyWithCurrencySymbol'][4:].replace(',','')) for x in available if x is not None]
            return (min(available))
        return '--'

    def _add_expensive(self, in_stock):
        in_stock["expensive"] = []
        for url, price, abe in zip(in_stock["url"], in_stock["price"], in_stock["abe"]):
            try:
                if float(abe) > 100 and float(price) < 15:
                    in_stock["expensive"].append(url)
            except (ValueError, TypeError):
                pass  

    # Sends the broken links in the Google Sheet
    def _show_broken_links(self):
        for i in range(len(self.broken_links)):
            sheet.wks.update_cell(i+1,17,self.broken_links[i])

    # Checks if a link is broken
    def _is_broken_link(self, soup):
        soup_tag = str(soup.find("div", {"class": "big-blue-header-area mbn"}))
        if soup_tag != 'None':
            return True
        else: return False

    # Sorts the results by price
    def _sort_by_price(self, res):
        res["price"], res["name"], res["url"], res["abe"] = zip(
            *sorted(zip(res["price"], res["name"], res["url"], res["abe"])))

    # Compares current run to previous run, and notes any new books found
    def _add_new_stock(self, in_stock):
        in_stock["new"] = []

        with open("stock_info.json", "r") as f:
            old_stock = json.load(f)
        
        for name, price in zip(in_stock["name"], in_stock["price"]):
            if name in old_stock["name"]:
                try:
                    price_float = float(price)
                    index = old_stock["name"].index(name)
                    old_price = old_stock["price"][index]
                    try:
                        old_price_float = float(old_price)
                        if old_price_float > 15 and price_float < 15:
                            in_stock["new"].append(name)
                    except (ValueError, TypeError):
                        pass
                except (ValueError, TypeError):
                    pass
            if name not in old_stock["name"]:
                try:
                    price_float = float(price)
                    if price_float < 15:
                        in_stock["new"].append(name)
                except (ValueError, TypeError):
                        pass

    # Dump Stock Into a .json to be used by the pr() method
    def _store_stock(self, res):
        new_json = json.dumps(res)
        with open('stock_info.json', 'w') as f:
            f.write(new_json)