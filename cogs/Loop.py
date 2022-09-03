import warnings
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from func.sheet import sheet
from func.embed import *
from func.message import *

class Loop(commands.Cog):

    warnings.filterwarnings("ignore")

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = AsyncIOScheduler(timezone="America/New_York")
        scheduler.add_job(self.loop_sr, 'cron', minute='0', args=[self])
        scheduler.start()

    async def loop_sr(*args):

        # Create ctx for the embed function to use
        bot = args[0].bot
        channel = bot.get_channel(997024131067416606)
        message = await channel.fetch_message(1006408720349151292)
        ctx = await bot.get_context(message)

        s = sheet()
        stock = await s.search(ctx)
        await send_embed(ctx, stock)

        # Send embed if there's new item/s compared to last run
        if "new" in stock:
            if stock["new"]:
                await send_embed_new(ctx, stock["new"])

        # Sends a dm and adds broken links to the worksheet if any found
        if s.broken_links:
            s.show_broken_links()
            await dm_broken_links(bot)

def setup(bot):
    bot.add_cog(Loop(bot))