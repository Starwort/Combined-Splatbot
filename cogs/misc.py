from discord import *
from discord.ext import commands
import datetime
from random import choice
from ast import literal_eval
import pygal
class Misc():
    def __init__(self,bot):
        self.bot = bot
        self.modefile = open("mode_list.txt")
        self.modes = self.modefile.read().split("\n")
        self.modefile.close()
        self.mapfile = open("map_list.txt")
        self.maps = self.mapfile.read().split("\n")
        self.mapfile.close()
    @commands.command(pass_context=True)
    async def scrims(self,ctx, noScrims: int):
        """Generates N scrims; code originally produced for use in Spyke"""
        try:
            noScrims = int(noScrims)
            if noScrims > 50:
                raise Exception
        except:
            await ctx.send(content="The number of scrims must be whole and less than or equal to 50!")
            return
        scrims = []
        minus1map = None
        minus2map = None
        minus1mode = None
        minus2mode = None
        for i in range(noScrims):
            map = None
            while map in [None, minus1map, minus2map]:
                map = choice(self.maps)
            mode = None
            while mode in [None, self.modes[0], minus1mode, minus2mode]:
                mode = choice(self.modes)
            scrims.append([map,mode])
            minus2map = minus1map
            minus1map = map
            minus2mode = minus1mode
            minus1mode = mode
        out = "\n"
        for i in range(noScrims):
            out += f'Game #{i+1}: {" ".join(scrims[i][1].split(" ")[slice(len(scrims[i][1].split(" "))-1)])} on {" ".join(scrims[i][0].split(" ")[slice(len(scrims[i][0].split(" "))-1)])}\n'
        await ctx.send(content=out.strip())
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
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(description=f"Ping time: {round(self.bot.latency * 1000,3)}ms", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_author(name="Pong!", icon_url="https://cdn.discordapp.com/avatars/424540163579052043/b67d194871881f83a7e67f3ed35a02ea.png?size=1024")
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def invite(self, ctx):
        embed = Embed(description="To invite the bot to your server, click [here](https://discordapp.com/api/oauth2/authorize?client_id=424540163579052043&permissions=2048&scope=bot)", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(pass_context=True, aliases=["suggestion"])
    async def support(self,ctx):
        embed = Embed(description="If you need support or have a suggestion for the bot, click [here](https://discord.gg/3xuDR3G)", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(aliases=['credit'])
    async def credits(self,ctx):
        credits = f'''Original weapon, mode and map lists created by {self.bot.get_user(196685856466010112)} at my request (he was very helpful when making the three bots that preceded this one)
Hide & Seek emoji created by MrSatnav [tag unknown], an ex-member of Ink2Death
Sub and Special Weapon emoji from the Splatoon Wiki (<https://splatoonwiki.org>)
All other emoji created by the talented {self.bot.get_user(366208016187523082)}
Code, obviously, by me [Starwort#6129] with a few snippets taken from discord.py examples'''
        await ctx.send(credits)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self,ctx,newprefix):
        '''Sets the guild prefix. Requires the Manage Server permission. To use spaces in your prefix quote it.
        You can even use a space at the end of the prefix.
        Example 1 (no spaces):
        [p]setprefix splat!
        Example 2 (with trailing space):
        [p]setprefix "splat "'''
        if len(newprefix) > 10:
            return await ctx.send('In order to prevent abuse to my disk, the prefix length has been capped at 10. Sorry!')
        add = ('removed' if newprefix.strip(' ') == '' else f'changed to `{newprefix}`') if ctx.guild.id in self.bot.additionalprefixdata else f'set to `{newprefix}`'
        outmsg = f'Your server\'s prefix has been {add}'
        self.bot.additionalprefixdata[ctx.guild.id] = newprefix
        if newprefix == '': del self.bot.additionalprefixdata[ctx.guild.id]
        with open('prefixes.txt','w') as file:
            file.write(repr(self.bot.additionalprefixdata))
        await ctx.send(outmsg)
def setup(bot):
    bot.add_cog(Misc(bot))
