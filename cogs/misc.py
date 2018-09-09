from discord import *
from discord.ext import commands
import datetime
from random import choice
from ast import literal_eval
import pygal
import aiofiles
class Miscellaneous():
    def __init__(self,bot):
        self.bot = bot
    @commands.group(pass_context=True)
    async def outcomes(self,ctx):
        """Provides a pie chart of the all-time outcomes of a command"""
        if ctx.invoked_subcommand == None:
            await ctx.send("You need to provide a category; \"mode\", \"map\", or \"weapon\"!")
    @outcomes.command(pass_context=True)
    async def mode(self,ctx):
        file = open("modist")
        dist = literal_eval(file.read())
        file.close()
        chart = pygal.Pie()
        chart.title = "Distribution of chosen modes by mode"
        for i in dist.keys():
            chart.add(i,dist[i])
        chart.render_to_png("modes.png")
        await ctx.send(file=File("modes.png"))
    @outcomes.command(pass_context=True)
    async def map(self,ctx):
        file = open("madist")
        dist = literal_eval(file.read())
        file.close()
        chart = pygal.Pie()
        chart.title = "Distribution of chosen maps by map"
        for i in dist.keys():
            chart.add(i,dist[i])
        chart.render_to_png("maps.png")
        await ctx.send(file=File("maps.png"))
    @outcomes.command(pass_context=True)
    async def weapon(self,ctx):
        file = open("wdist")
        dist = literal_eval(file.read())
        file.close()
        chart = pygal.Pie()
        chart.title = "Distribution of chosen weapons by weapon"
        for i in dist.keys():
            chart.add(i,dist[i])
        chart.render_to_png("weapons.png")
        await ctx.send(file=File("weapons.png"))
    @commands.command(pass_context=True)
    async def ping(self,ctx):
        '''Display the bot's ping time'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(description=f"Ping time: {round(self.bot.latency * 1000,3)}ms", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_author(name="Pong!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def invite(self, ctx):
        '''Link to invite the bot'''
        embed = Embed(description="To invite the bot to your server, click [here](https://discordapp.com/oauth2/authorize?client_id=424540163579052043&scope=bot&permissions=122944)", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(pass_context=True, aliases=["suggestion"])
    async def support(self,ctx):
        '''Link to the support server'''
        embed = Embed(description="If you need support or have a suggestion for the bot, click [here](https://discord.gg/3xuDR3G)", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(aliases=['credit'])
    async def credits(self,ctx):
        '''Display credits for the bot's lists and other data'''
        credits = f'''Original weapon, mode and map lists created by {self.bot.get_user(196685856466010112)} at my request (he was very helpful when making the three bots that preceded this one)
Weapon info list created by me [Starwort#6129]
All lists maintained by me [Starwort#6129]
Hide & Seek emoji created by MrSatnav [tag unknown], an ex-member of Ink2Death
Sub and Special Weapon emoji from the Splatoon Wiki (<https://splatoonwiki.org>)
All other emoji created by the talented {self.bot.get_user(366208016187523082)}
Code, obviously, by me [Starwort#6129] with a few snippets taken from discord.py examples'''
        await ctx.send(credits)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self,ctx,newprefix):
        '''Sets the server's custom prefix (the original will still work). Requires the Manage Server permission. To use spaces in your prefix quote it.
        You can even use a space at the end of the prefix.
        
        Example 1 (no spaces):
        [p]setprefix splat!
        Example 2 (with trailing space):
        [p]setprefix "splat "
        
        To remove your server's prefix:
        [p]setprefix ""'''
        newprefix = newprefix.lstrip(' ')
        if len(newprefix) > 10:
            return await ctx.send('In order to prevent abuse to my disk, the custom prefix length has been capped at 10. Sorry!')
        add = ('removed' if newprefix == '' else f'changed to `{newprefix}`') if ctx.guild.id in self.bot.additionalprefixdata else f'set to `{newprefix}`'
        outmsg = f'Your server\'s custom prefix has been {add}'
        self.bot.additionalprefixdata[ctx.guild.id] = newprefix
        if newprefix == '': del self.bot.additionalprefixdata[ctx.guild.id]
        async with aiofiles.open('prefixes.txt','w') as file:
            await file.write(repr(self.bot.additionalprefixdata))
        await ctx.send(outmsg)
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
