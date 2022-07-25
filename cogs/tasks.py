from discord.ext import commands, tasks
from datetime import datetime as dt
from random import choice
import feedparser
import discord
from store import PdmManager


class TimerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 984467894605848677
        self.feed_url = 'https://medium.com/feed/better-programming'
        self.ask_people_today.start()
        self.send_random_link.start()
        self.questions = [
            "Bugün nasıl geçti? Neler öğrendiniz veya neler yaptınız? Kısaca anlatın yoksa dünyayı ele geçireceğim."
        ]

        self.humor = [
            'Sunucunun en yakışıklı botu benim. MEE6 arkamdan konuşuyor... ',
            'Sunucunun en iyi yazılımcısı benim. Bu arada ',
            'Evet bildirim attım sinirlen diye. ',
            'En kötü Frontend Developer olacağım. Bu arada',
            "Java ile Javascript aynı şey değil mi? Bu arada",
            "Hayatın anlamı 42. Bu arada"
            "İşten en hızlı nasıl kovulursunuz? 'git push origin master'...",
            "Üzülme, işsiz kaldıysan en kötü Front-end geliştirici olursun."
            ]

    @tasks.loop(minutes=60)
    async def send_random_link(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 10:
            feed = feedparser.parse(self.feed_url)
            counter = 0
            while True:
                random_entry_link = choice(feed.entries).link
                if not PdmManager.is_link_in_db(random_entry_link):
                    PdmManager.add_sended_link(random_entry_link)
                    channel = self.bot.get_channel(self.channel_id)
                    allowed_mentions = discord.AllowedMentions(everyone = True)
                    await channel.send(content = f"Selam @everyone! Bugünün öneri makalesini gönderiyorum. Okumanızı tavsiye ederim! {random_entry_link}", allowed_mentions = allowed_mentions)
                    break
                else:
                    counter += 1

                if counter >= 5:
                    break      

    
    @tasks.loop(minutes=60.0)
    async def ask_people_today(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 21:
            channel = self.bot.get_channel(self.channel_id)
            allowed_mentions = discord.AllowedMentions(everyone = True)
            await channel.send(content = f"selam @everyone! {choice(self.humor)} {choice(self.questions)}", allowed_mentions = allowed_mentions)
    
def setup(client):
	client.add_cog(TimerTask(client))
