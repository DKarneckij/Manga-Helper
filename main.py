from discord.ext import commands
import os, json, warnings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from func.sheet import sheet
from func.embed import *
from func.message import *

if not os.path.isfile("token.json"):
    TOKEN = os.environ.get('TOKEN')
else:
    with open('token.json', 'r') as f:
        TOKEN = json.load(f)['token']
        
bot = commands.Bot(command_prefix='$')
warnings.filterwarnings("ignore")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

async def loop_sr():

    # Create ctx for the embed function to use
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

scheduler = AsyncIOScheduler(timezone="America/New_York")
scheduler.add_job(loop_sr, 'cron', minute='0')
scheduler.start()

bot.run(TOKEN)