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

        print("Test")

        await ctx.message.delete()

        s = sheet()
        stock = await s.search(ctx)
        await send_embed(ctx, stock)

        # Send embed if there's new item/s compared to last run
        if "new" in stock:
            if stock["new"]:
                await send_embed_new(ctx, stock["new"])

        # Sends a dm and adds broken links to the worksheet
        if s.broken_links:
            s.show_broken_links()
            await dm_broken_links(self.bot)
    

def setup(bot):
    bot.add_cog(Search(bot))
    

