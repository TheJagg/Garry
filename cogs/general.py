from discord import app_commands
from discord.ext import commands
import discord.embeds
import sys
import os

class General(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    #Listener to print to terminal if the cog has loaded correctly
    @commands.Cog.listener()
    async def on_ready(self):
        print("General is online!")

#Example Embed with new App Commands
    '''
    @app_commands.command(name="testembed", description="Testing an embed framework.")
    async def testembed(self, interaction: discord.Interaction):
        emb = discord.Embed(title="Oh lookie here!")
        emb.set_author(name=interaction.user.name)
        await interaction.response.send_message(embed=emb)
    '''
        
async def setup(bot):
    await bot.add_cog(General(bot))