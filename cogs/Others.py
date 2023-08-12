import discord
from discord.ext import commands
import json
from func.sheet import sheet
from func.embed import *
from func.message import *


class Others(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def update(self, ctx):

        progress_message = await send_embed(ctx, "--- Updating AbeBooks ---")

        s = sheet()
        s.update_abe()

        await progress_message.delete()
        await send_embed(ctx, "--- Done Updating AbeBooks ---")

    # Sends the results of the last search
    # Different format of embed depending on PC/Mobile
    @commands.command() 
    async def pr(self, ctx, phone='f'):

        await ctx.message.delete()

        with open("stock_info.json", "r") as f:
            stock = json.load(f)
        if phone == 'f':
            await send_stock(ctx, stock)
        else:
            await send_stock_mobile(ctx, stock)

    @commands.command()
    async def remove(self, ctx, *, args):

        await ctx.message.delete()

        delete_list = args.split("$ ")
        delete_list = [x.lower() for x in delete_list]

        s = sheet()
        s.delete_items(delete_list)

        await embed_deleted_list(ctx, s.removed_list)

    @commands.command()
    async def new(self, ctx):

        await ctx.message.delete()
        progress_message = await send_embed(ctx, "--- Adding New Manga ---")

        s = sheet()
        await s.add_new()

        await progress_message.delete()
        await send_embed(ctx, "--- Done Adding New Manga ---")

async def setup(bot):
    await bot.add_cog(Others(bot))