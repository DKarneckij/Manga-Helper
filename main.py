from discord.ext import commands
import os, json, warnings, asyncio
print(os.listdir("func"))
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from func.embed import *
from func.schedule import Schedule
from func.message import *

if not os.path.isfile("token.json"):
    TOKEN = os.environ.get('TOKEN')
else:
    with open('token.json', 'r') as f:
        TOKEN = json.load(f)['token']

try:
    bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
except Exception as e:
    print(f"Error creating bot: {e}")
bot.schedule = Schedule(bot)
warnings.filterwarnings("ignore")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f"Error loading extension {filename}: {e}")

async def main():

    await load()

    scheduler = AsyncIOScheduler(timezone="America/New_York")
    # scheduler.add_job(bot.schedule.update_abe, trigger=CronTrigger.from_crontab('2 1 * * *'))
    # scheduler.add_job(bot.schedule.search, trigger=CronTrigger.from_crontab('* 10-15 * * * '), args=(["All"]))
    scheduler.add_job(bot.schedule.search, trigger=CronTrigger.from_crontab('*/5 * * * *'))
    scheduler.start()

    await bot.start(TOKEN)

asyncio.run(main())