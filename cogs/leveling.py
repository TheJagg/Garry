import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import math
import sys
import os
import io
from PIL import Image, ImageDraw

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Listener to print to terminal if the cog has loaded correctly
    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling is online!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))

        result = cursor.fetchone()

        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) Values (?,?,?,?,?)", (guild_id,user_id,cur_level,xp,level_up_xp))
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += 25

        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)
            level_up_xp

            await message.channel.send(f"Hey {message.author.mention}! Congrats, you leveled up! {cur_level}")

            cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp =? WHERE guild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, guild_id, user_id))

        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id =? AND user_id = ?", (xp, guild_id, user_id))

        connection.commit()
        connection.close()

    @app_commands.command(name="level",description="A command to check on your server level.")
    async def level(self, interaction: discord.Interaction):
        member_id = interaction.user.id
        guild_id = interaction.guild.id

        #Pull db data
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message(f"Sorry {interaction.user.mention}, you do not currently have a level.")
            #await ctx.send(f"Sorry {ctx.message.author.mention}, you do not currently have a level.")
        else:
            progress = math.floor((result[3]/result[4])*100)

            image = self.generate_progress_bar_image(progress)

            with io.BytesIO() as image_binary:
                image.save(image_binary,'PNG')
                image_binary.seek(0)

                file = discord.File(fp=image_binary, filename="progress.png")

                embed = discord.Embed(title=f"{interaction.user.name}\'s Level Progress", description=f"Current Level: **{result[2]}**\nXP: **{result[3]}** of **{result[4]}**\nYou are **{progress}%** of the way to level **{int(result[2])+1}**!")
                embed.set_image(url="attachment://progress.png")
                await interaction.response.send_message(file=file,embed=embed)
                #await ctx.send(file=file,embed=embed)
        connection.close()

    def generate_progress_bar_image(self,progress):
        width, height = 400, 50
        bar_length = width - 10

        #Colours
        background_colour = "#a8e0ff"
        border_colour = "#000000"
        fill_colour = "#3e517a"

        image = Image.new('RGB',(width,height),background_colour)
        draw = ImageDraw.Draw(image)

        draw.rectangle([5, 5, width - 5, height - 5], outline=fill_colour, width=2)

        # Calculate the length of the filled part of the progress bar
        filled_length = int(bar_length * progress // 100)

        # Draw the filled part of the progress bar
        draw.rectangle([5, 5, 5 + filled_length, height - 5], fill=fill_colour)

        return image
    

async def setup(bot):
    await bot.add_cog(LevelSys(bot))