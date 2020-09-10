"""danielj"""
# https://discordapp.com/oauth2/authorize?client_id=753011266187952288&scope=bot&permissions=8
import discord
from database.db import SQL
from discord.ext import commands
from pathlib import Path

sql = SQL()
print(f"Using discord.py version {discord.__version__}")
client = commands.Bot(command_prefix=sql.get_prefix)
client.remove_command("help")

with open("token.txt", "r") as f:
    tkn = f.readline()

@client.event
async def on_guild_join(guild):
    sql.add_prefix(guild.id, "!")  # Default prefix set upon bot joining the server

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


for cog in Path("cogs/").iterdir():
    if cog.suffix == ".py":
        client.load_extension(f"cogs.{cog.stem}")


@client.event
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("PoKéMoN GO"))


client.run(tkn)
