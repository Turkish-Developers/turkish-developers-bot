from discord.ext import commands, tasks
import discord
import datetime
from store import PdmManager
from views import *




class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_numbers = {
            ":one:": "1️⃣", 
            ":two:": "2️⃣", 
            ":three:": "3️⃣", 
            ":four:": "4️⃣",
            ":five:": "5️⃣",
            ":six:": "6️⃣",
            ":seven:": "7️⃣",
            ":eight:": "8️⃣",
            ":nine:": "9️⃣",
            }

    @commands.Cog.listener()
    async def on_ready(self):
	    print('hello!')
    
    @commands.command()
    @commands.has_role("Admin")
    async def createpoll(self, ctx, *, arg):
        await ctx.message.delete()
        arguments = list(map(lambda a: a.strip(), arg.split(',')))
    

        if len(arguments) <= 2:
            await ctx.send("Yeterli şekilde parametre girmedin :( Örnek: Yaş aralığınız?,1-50,51-100")
            return

        if len(arguments) > 11:
            await ctx.send("En fazla 9 tane seçenek koyabilirsin")
            return

        choices = arguments[1:]
        question = arguments[0]

        description = []
        for x, option in enumerate(choices):
            description += '\n {} {}'.format(list(self.poll_numbers.keys())[x], option)
            description += '\n'

        embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))

        react_message = await ctx.send(embed=embed)

        for reaction in list(self.poll_numbers.values())[0:len(choices)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        await react_message.edit(embed=embed)


class Streamer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("İlgili")
    async def stream(self, ctx, *, arg):
        await ctx.message.delete()
        arguments = list(map(lambda a: a.strip(), arg.split(',')))
        if len(arguments) == 2 and not PdmManager.is_key_in_db(str(ctx.message.author.id), 'streamed_users'):
            header = arguments[0]
            channel = arguments[1]
            allowed_mentions = discord.AllowedMentions(everyone = True)
            embed = discord.Embed(title=f"{header}", description=f"Merhaba @everyone! Ben {ctx.message.author.mention}. Şu an canlı yayındayım!\n", color=discord.Color.blue())
            embed.add_field(name="Hemen katıl:", value=f"{self.bot.get_channel(int(channel)).mention}", inline=True)
            PdmManager.add_sended_key(str(ctx.message.author.id), 'streamed_users')
            await ctx.send(embed=embed, allowed_mentions=allowed_mentions)

class DP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, dc_user:discord.Member):
        if reaction.message.author.id == dc_user.id:
            await reaction.remove(dc_user)
            await reaction.message.channel.send(f"{dc_user.mention}, kendine teşekkür etmeye çalışmak güzel bir şey tabi. fakat bunun için DP kazanamazsın. 😛")
            return

        if reaction.emoji in ['🙏', '🙏🏻', '🙏🏿', '🙏🏽']:
            other_user_id = reaction.message.author.id
            user = UserView(dc_user.id)
            is_success, other_user = user.increase_user_developer_point(other_user_id)
            
            if is_success:
                await reaction.message.channel.send(f"{dc_user.mention}, {reaction.message.author.mention} kullanıcısına teşekkür etti 👏! {reaction.message.author.mention} artık {other_user.get_user_developer_point()} DP(Developer Point) sahibi! 😎")
            else:
                await reaction.remove(dc_user)
                await reaction.message.channel.send(f"{dc_user.mention}, maalesef teşekkür etme hakkın dolmuş 😐 Her gün 1 kere hak kazandığını unutma 🤚")


    @commands.command()
    async def thanks(self, ctx, dc_user:discord.Member):
        other_user_id = dc_user.id

        user = UserView(ctx.message.author.id)
        is_success, other_user = user.increase_user_developer_point(other_user_id)
        if is_success:
            await ctx.send(f"{ctx.message.author.mention}, {dc_user.mention} kullanıcısına **teşekkür etti **👏! {dc_user.mention} artık **{other_user.get_user_developer_point()}** DP(Developer Point) sahibi! 😎")
        else:
            await ctx.send(f"{ctx.message.author.mention}, maalesef teşekkür etme hakkın dolmuş 😐 Her gün 1 kere hak kazandığını unutma 🤚")



    @commands.command()
    async def mydp(self, ctx):
        emojis = ['😎', '😱', '🧠', '🤗', '🧐', '🥳']
        import random
        user = UserView(ctx.message.author.id)
        await ctx.send(f"Toplam {user.get_user_developer_point()} DP'ye sahipsin **{ctx.message.author.mention}**! Eğer DP kazanmak istiyorsan insanlara yardım edebilir, canlı yayınlar açmaya çalışabilirsin {random.choice(emojis)}")
    
    @commands.command()
    async def dp(self, ctx, dc_user:discord.Member):
        user = UserView(dc_user.id)
        await ctx.send(f"{dc_user.display_name} **{user.get_user_developer_point()}** DP'ye sahip! {ctx.message.author.mention}!")

    @commands.command()
    @commands.has_role("Admin")
    async def cleardp(self, ctx):
        UserView.restore_all_gave_dp()

    @commands.command()
    async def showcommands(self, ctx):
        description="""
        --**GENEL**--

        **!tdb mydp** - Toplam ne kadar DP puanınız olduğunu öğrenebilirsiniz
        **!tdb dp @discorduser** - Başka bir kullanıcının toplam DP puanını öğrenebilirsiniz
        **!tdb showdpall **- DP Puanlarının liderlik tablosunu görebilirsiniz
        **!tdb thanks @discorduser** - Kullanıcıya DP puanı kazandırırsınız.

        --**YAYINCI**--

        **!tdb stream <header>, <voice_channel_id>** - Yayıncı, açtığı yayını kullanıcılara haber verir.

        **Not:**
        Eğer bir mesaja 🙏🏻 emojisi kullanırsanız, mesajı atan kişiye DP kazandırabilirsiniz.
        """

        embed = discord.Embed(title = "Komut - Açıklama", description=description, color = 3553599)
        await ctx.send(embed=embed)

    @commands.command()
    async def showdpall(self, ctx):
        users = UserView.get_all_users_dp_point() # [{user_id: 0000, dp_point:0 }]
        description = ''
        count = 1
        print(users)
        for user in users:
            name = self.bot.get_user(user.get('user_id')).display_name
            point = user.get('dp_point')
            description += f"**{count}.** {name} {point}DP\n"
            count += 1

        print(description)
        embed = discord.Embed(title = "👑 DP(Developer Point) Sıralaması", description=description, color = 3553599)
        await ctx.send(embed=embed)

    
    @tasks.loop(minutes=60)
    async def clear_dp(self):
        from datetime import dt
        await self.bot.wait_until_ready()
        now_hour = dt.now().hour
        if now_hour == 11:
            UserView.restore_all_gave_dp()


        



def setup(client):
	client.add_cog(Poll(client))
	client.add_cog(Streamer(client))
	client.add_cog(DP(client))
