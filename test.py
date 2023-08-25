import gspread, bs4, asyncio
from func.AbeBooks import AbeBooks
from func.sheet import Sheet
from website.wob import WOB

async def main():
    s = Sheet()

    name_list = s.get_names()
    isbn13_list = s.get_isbn13s()
    abe_list = s.get_abes()

    hpb = WOB(name_list, isbn13_list, abe_list)
    stock = []
    stock = await hpb.search()

asyncio.run(main())