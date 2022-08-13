from typing_extensions import Self
import warnings, json
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from func.sheet import sheet
from func.embed import *
from func.message import *

class Loop(commands.Cog):

    warnings.filterwarnings("ignore")

    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="America/New_York")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.scheduler.add_job(self.loop_sr, CronTrigger(minute=35), args=[self])
        self.scheduler.start()

    async def loop_sr(*args):
        print("Test")
        bot = args[0].bot
        channel = bot.get_channel(997024131067416606)
        message = await channel.fetch_message(1006408720349151292)
        ctx = await bot.get_context(message)
        print(ctx)

        s = sheet()
        stock = await s.search()
        await send_embed(ctx, stock)
        if "new" in stock:
            if stock["new"]:
                await send_embed_new(ctx, stock["new"])

        #If there are broken links within the worksheet
        if s.broken_links:
            s.show_broken_links()
            await dm_broken_links(bot)


def setup(bot):
    bot.add_cog(Loop(bot))