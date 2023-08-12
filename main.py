from discord.ext import commands
import os, json, warnings, asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from func.sheet import sheet
from func.embed import *
from func.message import *
from func.Schedule import Schedule

if not os.path.isfile("token.json"):
    TOKEN = os.environ.get('TOKEN')
else:
    with open('token.json', 'r') as f:
        TOKEN = json.load(f)['token']
        
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
bot.schedule = Schedule(bot)
warnings.filterwarnings("ignore")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()

    scheduler = AsyncIOScheduler(timezone="America/New_York")
    scheduler.add_job(bot.schedule.update_abe, trigger=CronTrigger.from_crontab('0 7 * * *'))
    scheduler.add_job(bot.schedule.search, trigger=CronTrigger.from_crontab('0,20,40 19-21 * * * '), args=(["All"]))
    scheduler.add_job(bot.schedule.search, trigger=CronTrigger.from_crontab('5,10,15,25,30,35,45,50,55 19-21 * * * '), args=(["Expensive"]))
    scheduler.start()

    await bot.start(TOKEN)

asyncio.run(main())