import discord
from discord.ext import commands
from func.sheet import sheet
from func.HPB import HPB
from func.embed import *
from func.message import *

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sr(self, ctx):

        s = sheet()

        name_list = s.get_names()
        isbn13_list = s.get_isbn13s()
        abe_list = s.get_abes()

        hpb = HPB(name_list, isbn13_list, abe_list)
        stock = await hpb.search()

        await send_stock(ctx, stock)

    
async def setup(bot):
    await bot.add_cog(Search(bot))
