from discord.ext import commands, tasks
from datetime import datetime as dt
import random
import feedparser
import discord
from store import PdmManager
from tools import Article


class TimerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.turkish_developers_id = 643739727849062400
        self.channel_id = 984467894605848677
        self.python_channel_id = 996853962919661568
        self.python_role_id = 772894720790888458

        self.frontend_channel_id = 996825047853432863
        self.frontend_role_id = 794649516447236096

        self.feed_url = 'https://medium.com/feed/better-programming'
        

        self.ask_people_today.start()
        self.send_random_link.start()
        self.ask_to_interested_user.start()
        self.python_article.start()
        self.css_article.start()


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
        if now_hour == 9:
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
                await channel.send(content=f"{random_user.mention}", embed=self.embed_message("", f"{random_user.mention}, Naber? Neler yapıyorsun?"))

        if now_hour == 23:
            PdmManager.clear_key_in_db('interested_users')
            PdmManager.clear_key_in_db('streamed_users')


    @tasks.loop(minutes=60.0)
    async def python_article(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 8:
            article_data = self.send_article(
                channel_id=self.python_channel_id,
                rss_link="https://realpython.com/atom.xml",
                store_key='python_article',
                role_id=self.python_role_id
            )
            
            if article_data:
                channel = article_data.get('channel')
                article_data.pop('channel')
                await channel.send(**article_data.get('data'))

    @tasks.loop(minutes=60.0)
    async def css_article(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 8:
            article_data = self.send_article(
                channel_id=self.frontend_channel_id,
                rss_link="https://css-tricks.com/feed/",
                store_key='css-article',
                role_id=self.frontend_role_id
            )
            
            if article_data:
                channel = article_data.get('channel')
                article_data.pop('channel')
                await channel.send(**article_data.get('data'))


    def send_article(self, channel_id, rss_link, store_key, role_id):
        channel = self.bot.get_channel(channel_id)
        link,title,summary = Article.get_article(rss_link)

        if 'podcast' in link:
            return False

        allowed_mentions = discord.AllowedMentions(everyone = True)

        if not PdmManager.is_key_in_db(str(link), store_key):
            PdmManager.set_key_value(str(link), store_key)
        else:
            if PdmManager.get_key_value(link, store_key) == link:
                return False

        return {"channel": channel, "data": {"content": f"Merhaba <@&{role_id}>, size yeni çıkan bir makale öneriyorum: {link}", "allowed_mentions": allowed_mentions}}


    def embed_message(self, title, description):
        return discord.Embed(title=f"{title}", description=f"{description}", color=discord.Color.green())

        
    
    
def setup(client):
	client.add_cog(TimerTask(client))
