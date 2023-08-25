import discord
from func.Embed import *
from func.Sheet import Sheet
from func.message import *
from website.HPB import HPB

class Schedule():
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 997024131067416606
        self.message_id = 1006408720349151292

    async def search(self):

        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        ctx = await self.bot.get_context(message)

        await send_embed(ctx, f"--- Searching For Manga ---")

        s = Sheet()

        name_list = s.get_names()
        isbn13_list = s.get_isbn13s()
        abe_list = s.get_abes()

        website_stock = []

        # Search HalfPriceBooks
        hpb = HPB(name_list, isbn13_list, abe_list)
        website_stock.append(await hpb.search())

        # Search WorldofBooks
        for stock in website_stock:
            await send_stock(ctx, stock)
    
    async def update_abe(self):

        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        ctx = await self.bot.get_context(message)
        
        await send_embed(ctx, f"--- Updating Manga ---")

        s = Sheet()
        await s.update_abe()

        await send_embed(ctx, f"--- Done Updating Manga ---")
