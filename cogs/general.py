from discord import app_commands
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions, has_permissions, has_role
import discord.embeds
import random
import uuid
import sys
import os

from framework import embed_image

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

    @commands.command(aliases=['cc'])
    @commands.has_role('Nitro')
    async def clearchat(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command(aliases=['b'])
    @commands.has_role('Nitro')
    async def batch(self, ctx):
        for _ in range(10):
            str = uuid.uuid4().hex
            str = str[:6]
            await ctx.send("https://prnt.sc/" + str)

    @commands.command()
    async def test_embed(self,ctx,title,description,url=None):
        embed = embed_image(title,description,url)
        await ctx.send(embed=embed)

        
async def setup(bot):
    await bot.add_cog(General(bot))