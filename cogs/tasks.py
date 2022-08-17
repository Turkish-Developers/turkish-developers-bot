from discord.ext import commands, tasks
from datetime import datetime as dt
import random
import feedparser
import discord
from store import PdmManager
from tools import Article, Reddit
from views import QuestionView


class TimerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.set_constant_variables()

        # Tasks Start
        self.ask_people_today.start()
        self.send_reddit_humor.start()
        self.update_status.start()
        self.send_random_link.start()
        self.ask_to_interested_user.start()
        self.get_random_question.start()
        self.python_article.start()
        self.frontend_article.start()
        self.backend_article.start()
        self.uiux_article.start()
        self.mlai_article.start()
        # Tasks Start End


    def set_constant_variables(self):
        # Channels & Roles #
        self.turkish_developers_id = 643739727849062400

        self.today_article_channel_id = 1009504838725419098
        self.today_article_channel_role = 1009517046087823470 

        
        self.channel_id = 984467894605848677
        self.python_channel_id = 1009514826223067146
        self.python_role_id = 1009513244513271818

        self.frontend_channel_id = 1009514864135393291
        self.frontend_role_id = 1009513745703260230 

        self.backend_channel_id = 1009514914500595793
        self.backend_role_id = 1009513835545239692

        self.uiux_channel_id = 1009514978736349225
        self.uiux_channel_role_id = 1009513882370457700 

        self.mlai_channel_id = 1009515088341897226
        self.mlai_role_id = 1009514028118310964 

        # Feed Urls #

        self.feed_urls = ['https://medium.com/feed/better-programming',
        'https://stackoverflow.blog/newsletter/feed/']

        self.frontend_article_urls = [
            "https://tympanus.net/codrops/feed/",
            "https://css-tricks.com/feed/",
            "https://dev.to/feed",
            "https://1stwebdesigner.com/feed/",
            "https://addyosmani.com/rss.xml",
            "https://feeds.feedburner.com/2ality",
            "https://www.sitepoint.com/sitepoint.rss"
        ]

        self.backend_article_urls = [
            "https://blog.alexellis.io/rss/",
            "https://devblogs.microsoft.com/dotnet/feed/"
        ]

        self.uiux_article_urls = [
            'https://uxplanet.org/feed',
            'https://www.nngroup.com/feed/rss/',
            'http://feeds.feedburner.com/uxmovement'

        ]

        self.mlai_article_urls = [
            'https://machinelearningmastery.com/blog/feed/',
            'https://blog.google/technology/ai/rss/',
            'https://blog.bigml.com/feed/',
            'https://news.mit.edu/rss/topic/machine-learning'

        ]

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
            "Üzülme, işsiz kaldıysan en kötü Front-end geliştirici olursun.",
            "Akılsız coder'in zahmetini CPU çeker...",
            "en iyi kod yazılmamış olandır...",
            "iki kişinin bildiği encryption key sır değildir yeğen.",
            "söz uçar jira kalır.",
            "bugünün comment'ini yarına bırakma."
            "damlaya damlaya memory leak olur.",
            "denize düşen python'a sarılır."
            ]




    @tasks.loop(minutes=60)
    async def send_random_link(self):
        await self.bot.wait_until_ready()
        import random
        now_hour = dt.now().hour
        if now_hour == 9:
            feed = feedparser.parse(random.choice(self.feed_urls))
            counter = 0
            while True:
                random_entry_link = random.choice(feed.entries).link
                if not PdmManager.is_key_in_db(random_entry_link, 'link'):
                    PdmManager.add_sended_key(random_entry_link, 'link')
                    channel = self.bot.get_channel(self.toda)
                    allowed_mentions = discord.AllowedMentions(everyone = True)
                    await channel.send(content = f"Günaydın <@&{self.today_article_channel_role}>, Bugünün öneri makalesini sıcak sıcak gönderiyorum. Elleriniz yanmasın aman. Okumanızı tavsiye ederim! {random_entry_link}", allowed_mentions = allowed_mentions)
                    break
                else:
                    counter += 1

                if counter >= 5:
                    break      

    @tasks.loop(seconds=5)
    async def update_status(self):
        await self.bot.wait_until_ready()
        import random
        activity_list = [
        '!tdb showcommands', 
        'Toplam: ' + str(len(self.bot.get_guild(self.turkish_developers_id).members)) + " TD ❤️"
        ]


        activity = discord.Activity(type=discord.ActivityType.listening, name=random.choice(activity_list))
        await self.bot.change_presence(activity=activity)




    @tasks.loop(hours=1)
    async def get_random_question(self):
        await self.bot.wait_until_ready()
        import random

        if random.randint(1, 10) == 5:
            question_text, question_id = QuestionView.get_random_question()
            if question_id:
                channel = self.bot.get_channel(self.channel_id)
                message = await channel.send('**Rastgele Bir Soru gizemli bir şekilde Ortaya ÇIKTI 😱! İlk Çözen ol ve DP Kazan 😎**\n\n' +question_text.replace('<code>', '**'))
                await message.add_reaction('🇦')
                await message.add_reaction('🇧')
                await message.add_reaction('🇨')
                await message.add_reaction('🇩')


                PdmManager.set_key_value(str(message.id), 'question')
                PdmManager.set_key_value(str(question_id), 'question_id')

        

    @tasks.loop(hours=2)
    async def send_reddit_humor(self):
        await self.bot.wait_until_ready()
        title, link = Reddit.get_last_image_on_subreddit()
        channel = self.bot.get_channel(self.channel_id)



        if not PdmManager.is_key_in_db(str(link), 'reddit_humor'):
            PdmManager.set_key_value(str(link), 'reddit_humor')
        else:
            if PdmManager.get_key_value(link, 'reddit_humor') == link:
                return False

        e = discord.Embed(title=title)
        e.set_image(url=link)

        await channel.send(embed=e)

    
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
        if now_hour in [20, 22]:
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
            PdmManager.clear_key_in_db('suggested_users')


    @tasks.loop(minutes=60.0)
    async def python_article(self):
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 9:
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
    async def frontend_article(self):
        await self.bot.wait_until_ready()
        import random
        now_hour = dt.now().hour
        if now_hour == 9:
            article_data = self.send_article(
                channel_id=self.frontend_channel_id,
                rss_link=random.choice(self.frontend_article_urls),
                store_key='frontend-article',
                role_id=self.frontend_role_id
            )
            
            if article_data:
                channel = article_data.get('channel')
                article_data.pop('channel')
                await channel.send(**article_data.get('data'))

    @tasks.loop(minutes=60.0)
    async def backend_article(self):
        await self.bot.wait_until_ready()
        import random
        now_hour = dt.now().hour
        if now_hour == 9:
            article_data = self.send_article(
                channel_id=self.backend_channel_id,
                rss_link=random.choice(self.backend_article_urls),
                store_key='backend-article',
                role_id=self.backend_role_id
            )
            
            if article_data:
                channel = article_data.get('channel')
                article_data.pop('channel')
                await channel.send(**article_data.get('data'))

    @tasks.loop(minutes=60.0)
    async def uiux_article(self):
        await self.bot.wait_until_ready()
        import random
        now_hour = dt.now().hour
        if now_hour == 9:
            article_data = self.send_article(
                channel_id=self.uiux_channel_id,
                rss_link=random.choice(self.uiux_article_urls),
                store_key='uiux-article',
                role_id=self.uiux_channel_role_id
            )
            
            if article_data:
                channel = article_data.get('channel')
                article_data.pop('channel')
                await channel.send(**article_data.get('data'))

    @tasks.loop(minutes=60.0)
    async def mlai_article(self):
        await self.bot.wait_until_ready()
        import random
        now_hour = dt.now().hour
        if now_hour == 9:
            article_data = self.send_article(
                channel_id=self.mlai_channel_id,
                rss_link=random.choice(self.mlai_article_urls),
                store_key='mlai-article',
                role_id=self.mlai_role_id
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

        return {"channel": channel, "data": {"content": f"Değerli <@&{role_id}> abonelerimiz, istediğiniz günlük içerik burada: {link}", "allowed_mentions": allowed_mentions}}


    def embed_message(self, title, description):
        return discord.Embed(title=f"{title}", description=f"{description}", color=discord.Color.green())

        
    
    
def setup(client):
	client.add_cog(TimerTask(client))
