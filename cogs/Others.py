import discord
from discord.ext import commands
import json
from func.sheet import sheet
from func.embed import *
from func.message import *


class Others(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # Sends the results of the last search
    # Different format of embed depending on PC/Mobile
    @commands.command() 
    async def pr(self, ctx, phone='f'):
        with open("stock_info.json", "r") as f:
            stock = json.load(f)
        if phone == 'f':
            await send_embed(ctx, stock)
        else:
            await send_embed_mobile(ctx, stock)

def setup(bot):
    bot.add_cog(Others(bot))