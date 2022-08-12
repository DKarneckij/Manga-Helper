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
        self.scheduler.add_job(Loop.loop_sr, CronTrigger(minute=0))
        self.scheduler.start()

    async def loop_sr(self):
        s = sheet()
        stock = await s.search()
        send_embed(stock)
        if stock.has_key("new"):
            send_embed_new(stock["new"])

        #If there are broken links within the worksheet
        if s.broken_links:
            s.show_broken_links()
            await dm_broken_links(self.bot)


def setup(bot):
    bot.add_cog(Loop(bot))