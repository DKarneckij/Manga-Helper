import discord
from func.embed import *
from func.sheet import sheet
from func.message import *

class Schedule():
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 997024131067416606
        self.message_id = 1006408720349151292

    async def search(self, list_choice):

        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        ctx = await self.bot.get_context(message)


        await send_embed(ctx, f"--- Searching {list_choice} Manga ---")

        s = sheet()
        stock = await s.search(list_choice)
        await send_stock(ctx, stock)

        # Send embed and message if there's new item/s compared to last run
        if stock["new"]:
            print("New in Stock")
            await send_new_stock(ctx, stock["new"])

        if s.broken_links:
            await dm_broken_links(ctx)
    
    async def update_abe(self):

        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        ctx = await self.bot.get_context(message)
        
        await send_embed(ctx, f"--- Updating Manga ---")

        s = sheet()
        await s.update_abe()

        await send_embed(ctx, f"--- Done Updating Manga ---")
