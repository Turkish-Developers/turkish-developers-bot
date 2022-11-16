from discord.ext import commands
from store import PdmManager
from discord import Embed


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

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggestion_channel_id = 1005201507089661982

        self.question_channel_id = 984467960259280896
        self.question_role_id_list = [
            1007757021682081953,
            1007739463826407565,
            1007739916920295425,
            1007739975850274926,
            1007756869965725696,
            1007756917168422962,
            1007739222339362918,
            1007739376383565905,
            1007739517140222003,
            1007740092846190673,
            1007740167949406338,
            1007756569041178685,
            1007756118161887363,
            1007757879975084033,
            1007757914821369896,
            1007758166110519397,
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id == message.author.id:
            return

        if (message.channel.id == self.suggestion_channel_id): 
            suggestion = message.content
            await message.delete()
            if not PdmManager.is_key_in_db(str(message.author.id), 'suggested_users'):
                PdmManager.add_sended_key(str(message.author.id), 'suggested_users')
                suggestion_id = int(PdmManager.get_key_value(1, 'suggestion_id'))
                if suggestion_id:
                    count = PdmManager.set_key_value(str(suggestion_id + 1), 'suggestion_id')
                else:
                    count = PdmManager.set_key_value("1", 'suggestion_id')
                
                channel = await message.channel.send(embed=Embed(title=f"Öneri #{count}",description=suggestion))
                await channel.add_reaction('👍🏻')
                await channel.add_reaction('👎🏻')
            else:
                await message.author.send('Önerilerin için teşekkür ederiz. Her gün 1 kere öneri verebilirsin 😊')

    
async def setup(client):
	await client.add_cog(Greetings(client))
	await client.add_cog(Suggestions(client))
