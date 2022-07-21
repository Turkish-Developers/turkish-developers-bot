import os
import discord
import configparser
from discord.ext import commands

cp = configparser.ConfigParser()
cp.read('config.ini')

TOKEN = cp['SETTINGS']['TOKEN']

client = commands.Bot(command_prefix = "!tdb ")

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension("cogs." + f[:-3])

client.run(TOKEN)