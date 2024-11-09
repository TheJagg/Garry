import discord
import os
import asyncio
import logging
import importlib
from discord import app_commands
from discord.ext import commands, tasks
from config import token
from itertools import cycle

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())
statuses = cycle(["Is this thing on?","I need more commands","Someone is robbing a bank!"])
guild_id = 664390352794419203

# Check for administrator permissions.
def is_administrator(interaction: discord.Interaction):
    return interaction.user.guild_permissions.administrator

@bot.event
async def on_ready():
    print("All shipe have been acounted for, Ready to roll.")
    change_bot_status.start()
    await load_cogs()
    await sync_commands()

@tasks.loop(seconds=290)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(statuses)))

@bot.command()
async def load(ctx, extension):
    await load_cog(extension)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{extension} loaded')

@bot.command()
async def unload(ctx, extension):
    await unload_cog(extension)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{extension} unloaded!')

@bot.command()
async def reload(ctx, extension):
    await unload_cog(extension)
    await load_cog(extension)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{extension} reloaded!')

@bot.tree.command(name="re_sync", description="Updates the app commands that are run on this bot.")
@app_commands.check(is_administrator)
async def re_sync(interaction: discord.Interaction):
    await sync_commands()
    await interaction.response.send_message("App commands have been updated.", ephemeral=True)

@bot.tree.command(name="update_library", description="Update an imported python file.",guild=discord.Object(id=guild_id))
@app_commands.check(is_administrator)
async def update_library(interaction: discord.Interaction, library: str):
    try:
        # Import the library dynamically
        mod = importlib.import_module(library)
        importlib.reload(mod)
        await interaction.response.send_message(f"`{library}` has been successfully reloaded.", ephemeral=True)
    except ModuleNotFoundError:
        await interaction.response.send_message(f"Module `{library}` not found.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to reload library with error: {e}", ephemeral=True)

@bot.tree.command(name="status",description="Check on the status of Barry")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("The weather today is quite nice, and yes, I am functioning... I think.", ephemeral=True)

async def unload_cog(extension):
    await bot.unload_extension(f'cogs.{extension}')

async def load_cog(extension):
    await bot.load_extension(f'cogs.{extension}')

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f'{filename[:-3]} has been loaded.')
            except Exception as e:
                print(f'Failed to load {filename[:-3]}: {e}')

async def sync_commands():
    try:
        synced_commands = await bot.tree.sync()
        print(f'Synced {len(synced_commands)} commands.')
        synced_commands = await bot.tree.sync(guild=discord.Object(id=guild_id))
        print(f'Synced {len(synced_commands)} guild commands.')
    except Exception as e:
        print(f'Whoops failed to load commands. {e}')

async def main():
    async with bot:
        await bot.start(token)

asyncio.run(main())