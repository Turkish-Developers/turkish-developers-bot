import os
import discord
import configparser
import asyncio
from discord.ext import commands

cp = configparser.ConfigParser()
cp.read('config.ini')

TOKEN = cp['SETTINGS']['TOKEN']

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix = "!tdb ", intents=intents)

async def load_extensions():
	for f in os.listdir("./cogs"):
		if f.endswith(".py"):
			await client.load_extension("cogs." + f[:-3])


async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)

asyncio.run(main())