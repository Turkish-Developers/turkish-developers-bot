from discord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.describe_yourself_channel_id = 721340809646964789

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id == message.author.id:
            return

        thanks_items = ['teşekkürler', 'teşekkür', 'sağol', 'sağ ol', 'tesekkür', 'tesekkürler']
        if (message.channel.id == self.describe_yourself_channel_id): 
            await message.add_reaction('🎉')
        
        if any([item for item in thanks_items if item in message.content]):
            await message.author.send('Birisine teşekkür etmenin en iyi yolu; Eğer DP verme hakkın varsa, mesajına 🙏🏻 emojisi koyarak DP kazandırmak olduğunu unutma 😊')

        

    
def setup(client):
	client.add_cog(Greetings(client))
