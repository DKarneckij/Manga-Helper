import gspread, bs4, asyncio
from func.abebooks import AbeBooks
from func.sheet import sheet
from func.HPB import HPB

async def main():
    s = sheet()

    name_list = s.get_names()
    isbn13_list = s.get_isbn13s()
    abe_list = s.get_abes()

    # print(name_list)
    # print(isbn13_list)
    # print(abe_list)

    hpb = HPB(name_list, isbn13_list, abe_list)
    stock = []
    stock = await hpb.search()

asyncio.run(main())