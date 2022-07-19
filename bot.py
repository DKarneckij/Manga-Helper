import discord, asyncio, json
from discord.ext import commands, tasks, menus
from discord.ext.menus import button, First, Last
from data import *

with open('token.json', 'r') as f:
  TOKEN = json.load(f)['token']
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Overwrite for what buttons are displayed and what emotes are used 
# Added looping around for next and previous page
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
        namesStr, pricesStr = '', ''

        for vol in entries:
            name, url, price = vol[0],vol[1],vol[2]
            namesStr += f"[{name}]({url})\n"
            pricesStr += f"{price}\n"

        myEmbed=discord.Embed(
            title='$$$$$$',
            color= discord.Color.blue())
        myEmbed.add_field(name='Volume', 
            value=namesStr, inline=True)
        myEmbed.add_field(name='Price', 
            value=pricesStr, inline=True)
        return myEmbed

# Completes a search for all urls
@bot.command()
async def sr(ctx):
    stock_info = await find_stock()
    await send_embed(ctx, stock_info)

# Sends the results of the last search
@bot.command()
async def pr(ctx):
    with open("stock_info.json", "r") as f:
        stock_info = json.load(f)
    await send_embed(ctx, stock_info)

async def send_embed(ctx, stock_info):
    data = list(zip(stock_info["n"], stock_info["u"], stock_info["p"]))
    formatter = MySource(data, per_page=12)
    menu = MyMenuPages(formatter)
    await menu.start(ctx)

# @client.command()
# async def lp(ctx, enabled = "start", interval = 2):
#    if ctx.channel.id == bot_channel:
#        if enabled.lower() == "start":
#            run_intervals.change_interval(seconds=interval)
#            run_intervals.start(ctx)
#       if enabled.lower() == "stop":
#            run_intervals.stop()

# @tasks.loop()
# async def run_intervals(ctx):
#    await sr(ctx)

bot.run(TOKEN)
