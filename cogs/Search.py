import discord
from discord.ext import commands
from func.sheet import sheet
from func.embed import *
from func.message import *

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sr(self, ctx):

        await ctx.message.delete()
        await send_embed(ctx, "--- Searching HPB ---")

        # Run the search
        s = sheet()
        stock = await s.search("All")

        await send_stock(ctx, stock)

        # Send embed and message if there's new item/s compared to last run
        if stock["new"]:
            print("New in Stock")
            await send_new_stock(ctx, stock["new"])

        # Send message of all the expensive stuff
        if stock["expensive"]:
            print("Expensive in Stock")
            await dm_expensive_urls(self.bot, stock["expensive"])

        # Sends a dm if there's any broken links
        if s.broken_links:
            await dm_broken_links(self.bot)

    
async def setup(bot):
    await bot.add_cog(Search(bot))
