import discord

my_id = 197903946084384768

async def dm_broken_links(bot):
    discordUser = await bot.fetch_user(my_id)
    await discordUser.send('Fix the links!')
