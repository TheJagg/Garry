import discord
import discord.embeds


# Embed with just a title and description
def embed(title, description):
    emb = discord.Embed(
        title = str(title),
        description = str(description)
    )
    return emb

# Embed function with a title description and an image
def embed_image(title, description, url=None):
    emb = discord.Embed(
        title = str(title),
        description = str(description),
        colour = discord.Color.blue()
    )
    if url is not None:
        emb.set_image(url=str(url))
    return emb