import discord
from discord.ext import commands
from func.sheet import sheet
from func.embed import *
from func.message import *

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")
    
    @commands.command()
    async def sr(self, ctx):
        await ctx.send("----Beginning Search----")
        s = sheet()
        stock = await s.search()
        await send_embed(ctx, stock)

        #If there are broken links within the worksheet
        if s.broken_links:
            s.show_broken_links()
            await dm_broken_links(self.bot)
    

def setup(bot):
    bot.add_cog(Search(bot))
    

