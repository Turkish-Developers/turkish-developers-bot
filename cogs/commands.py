from discord.ext import commands



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
    async def createpoll(self, ctx, *, arg):
        import discord
        arguments = list(map(lambda a: a.strip(), arg.split(',')))
        print(arguments)

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






def setup(client):
	client.add_cog(Poll(client))
