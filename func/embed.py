from re import A
import discord
from discord.ext import menus
from discord.ext.menus import button, First, Last

class MyMenuPages(menus.MenuPages, inherit_buttons=False):
        
        @button('<:left:997635441752805419>', position=First(1))
        async def go_to_previous_page(self, payload):
            last_page = self._source.get_max_pages() - 1
            if self.current_page == 0:
                await self.show_checked_page(last_page)
            else: await self.show_checked_page(self.current_page - 1)

        @button('<:right:997635412434632704>', position=Last(1))
        async def go_to_next_page(self, payload):
            last_page = self._source.get_max_pages() - 1
            if self.current_page == last_page:
                await self.show_checked_page(0)
            else: await self.show_checked_page(self.current_page + 1)

# Overwrite for how pages are formated
class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        names, prices, prices_abe = '', '', ''

        for vol in entries:
            name, url, price, price_abe = vol[0],vol[1],vol[2], vol[3]
            names += f"[{name}]({url})\n"
            prices += f"{price}\n"
            prices_abe += f"{price_abe}\n"

        myEmbed=discord.Embed(
            title='$$$$$$',
            color= discord.Color.blue())
        myEmbed.add_field(name='Volume', 
            value=names, inline=True)
        myEmbed.add_field(name='Price', 
            value=prices, inline=True)
        myEmbed.add_field(name='AbeBooks', 
            value=prices_abe, inline=True)
        return myEmbed

class MySource_Mobile(menus.ListPageSource):
    async def format_page(self, menu, entries):
        names = ''

        for vol in entries:
            name, url, price, price_abe = vol[0],vol[1],vol[2], vol[3]
            names += f"[{name}]({url}) {price}  / {price_abe}\n"

        myEmbed=discord.Embed(
            title='$$$$$$',
            color= discord.Color.blue())
        myEmbed.add_field(name='Volume', 
            value=names, inline=True)
        return myEmbed

class MySource_New(menus.ListPageSource):
    async def format_page(self, menu, entries):
        new_items = 'Place Holder'

        for new in entries:
            new_items += f"{new}\n"

        myEmbed=discord.Embed(
            title='New',
            color= discord.Color.red())
        myEmbed.add_field(name='Volume', 
            value=new_items, inline=True)
        return myEmbed

# Overwrite for what buttons are displayed and what emotes are used 
# Added looping around for next and previous page
async def send_embed(ctx, stock):
    data = list(zip(stock["name"], stock["url"], stock["price"], stock["abe"]))
    formatter = MySource(data, per_page=10)
    menu = MyMenuPages(formatter)
    await menu.start(ctx)

async def send_embed_mobile(ctx, stock):
    data = list(zip(stock["name"], stock["url"], stock["price"], stock["abe"]))
    formatter = MySource_Mobile(data, per_page=9)
    menu = MyMenuPages(formatter)
    await menu.start(ctx)

async def send_embed_new(ctx, new):
    formatter = MySource_New(new, per_page = 10)
    menu = MyMenuPages(formatter)
    await menu.start(ctx)

async def send_broken_links(ctx, links):
    await ctx.send(links)
