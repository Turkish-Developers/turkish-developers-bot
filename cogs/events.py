from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.describe_yourself_channel_id = 721340809646964789

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.id == self.describe_yourself_channel_id): 
            await message.add_reaction('🎉')

    
def setup(client):
	client.add_cog(Greetings(client))
