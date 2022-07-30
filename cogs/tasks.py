from discord.ext import commands, tasks
from datetime import datetime as dt
import random
import feedparser
import discord
from store import PdmManager


class TimerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.turkish_developers_id = 643739727849062400
        self.channel_id = 984467894605848677
        self.feed_url = 'https://medium.com/feed/better-programming'
        

        self.ask_people_today.start()
        self.send_random_link.start()
        self.ask_to_interested_user.start()


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
                random_entry_link = random.choice(feed.entries).link
                if not PdmManager.is_key_in_db(random_entry_link, 'link'):
                    PdmManager.add_sended_key(random_entry_link, 'link')
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
            await channel.send(content = f"selam @everyone! {random.choice(self.humor)} {random.choice(self.questions)}", allowed_mentions = allowed_mentions)

    @tasks.loop(minutes=60)
    async def ask_to_interested_user(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        print(now_hour)
        if now_hour in [15, 18, 20, 22]:
            users = []

            turkish_developers_guild = self.bot.get_guild(self.turkish_developers_id)
            channel = self.bot.get_channel(self.channel_id)
            role = discord.utils.find(lambda r: r.name == 'İlgili', turkish_developers_guild.roles)
            
            for user in turkish_developers_guild.members:
                if role in user.roles and user.status != discord.Status.offline:
                    users.append(user)
        
            if not users:
                return

            random_user = random.choice(users)
            if not PdmManager.is_key_in_db(str(random_user.id), 'interested_users'):
                PdmManager.add_sended_key(str(random_user.id), 'interested_users')
                await channel.send(embed=self.embed_message("", f"{random_user.mention}, bugün bize bilmediğimizi düşündüğün bir Yazılım & Programlama bilgisi verebilir misin?"))

        if now_hour == 11:
            PdmManager.clear_key_in_db('interested_users')
            PdmManager.clear_key_in_db('streamed_users')

    def embed_message(self, title, description):
        return discord.Embed(title=f"{title}", description=f"{description}", color=discord.Color.green())

        
    
    
def setup(client):
	client.add_cog(TimerTask(client))
