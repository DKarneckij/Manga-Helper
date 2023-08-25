from discord.ext import commands
import json, os
from func.Sheet import Sheet
from func.embed import *
from func.message import *


class Others(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def update(self, ctx):

        progress_message = await send_embed(ctx, "--- Updating AbeBooks ---")

        s = Sheet()
        s.update_abe(ctx)

        await progress_message.delete()
        await send_embed(ctx, "--- Done Updating AbeBooks ---")

    # Sends the results of the last search
    @commands.command() 
    async def pr(self, ctx, *, args=None):

        await ctx.message.delete()

        print(args)

        # Get all _stock.json files
        json_list = []
        for file in os.listdir("data"):
            if file.endswith(".json"):
                json_list.append(file)
                
        print(json_list)

        for json_file in json_list:
            json_path = os.path.join("data", json_file)
            with open(json_path, "r") as f:
                stock = json.load(f)
            if not args:
                await send_stock(ctx, stock)
        
    # @commands.command()
    # async def remove(self, ctx, *, args):

    #     await ctx.message.delete()

    #     delete_list = args.split("$ ")
    #     delete_list = [x.lower() for x in delete_list]

    #     s = sheet()
    #     s.delete_items(delete_list)

    #     await embed_deleted_list(ctx, s.removed_list)

    # @commands.command()
    # async def new(self, ctx):

    #     await ctx.message.delete()
    #     progress_message = await send_embed(ctx, "--- Adding New Manga ---")

    #     s = sheet()
    #     await s.add_new()

    #     await progress_message.delete()
    #     await send_embed(ctx, "--- Done Adding New Manga ---")

async def setup(bot):
    await bot.add_cog(Others(bot))