import discord
from discord.ext import commands
import os, json

if not os.path.isfile("token.json"):
    TOKEN = os.environ.get('TOKEN')
else:
    with open('token.json', 'r') as f:
        TOKEN = json.load(f)['token']
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)