import json, os, os.path
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sheet import Sheet
from embed import embed
from message import message
import warnings

if not os.path.isfile("token.json"):
    TOKEN = os.environ.get('TOKEN')
else:
    with open('token.json', 'r') as f:
        TOKEN = json.load(f)['token']
bot = commands.Bot(command_prefix='$')
sheet = Sheet()
warnings.filterwarnings("ignore")
scheduler = AsyncIOScheduler(timezone="America/New_York")



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # scheduler.add_job(tik, CronTrigger(second=0))
    # scheduler.add_job(tok, CronTrigger(second=20))
    # scheduler.start()

async def tik():
    print("Tik")
async def tok():
    print("Tok")

# Completes a search for all urls
@bot.command()
async def sr(ctx):
    await ctx.send("----Beginning Search----")
    stock = await sheet.search()
    await embed.send_embed(ctx, stock)

    #If there are broken links within the worksheet
    if sheet.broken_links:
        sheet.send_broken_links()
        await message.dm_broken_links(bot)
        

# Sends the results of the last search
# Different format of embed depending on PC/Mobile
@bot.command() 
async def pr(ctx, phone='f'):
    with open("stock_info.json", "r") as f:
        stock = json.load(f)
    if phone == 'f':
        await embed.send_embed(ctx, stock)
    else:
        await embed.send_embed_mobile(ctx, stock)

bot.run(TOKEN)