import discord
from discord.ext import commands
from func.sheet import Sheet
from website.hpb import HPB
from func.embed import *
from func.message import *

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sr(self, ctx):

        await ctx.message.delete()

        await send_embed(ctx, f"--- Searching For Manga ---")

        s = Sheet()

        name_list = s.get_names()
        isbn13_list = s.get_isbn13s()
        abe_list = s.get_abes()

        website_stock = []

        # Search HalfPriceBooks
        hpb = HPB(name_list, isbn13_list, abe_list)
        website_stock.append(await hpb.search())

        # Search WorldofBooks
        for stock in website_stock:
            await send_stock(ctx, stock)

    
async def setup(bot):
    await bot.add_cog(Search(bot))
