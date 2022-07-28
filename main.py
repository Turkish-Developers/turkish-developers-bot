import os
import discord
import configparser
from discord.ext import commands

cp = configparser.ConfigParser()
cp.read('config.ini')

TOKEN = cp['SETTINGS']['TOKEN']

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix = "!tdb ", intents=intents)

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension("cogs." + f[:-3])

client.run(TOKEN)