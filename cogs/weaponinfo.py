from discord import *
from discord.ext import commands
from random import choice
import datetime
from requests import get
from fuzzywuzzy import process
def download(url, file_name):
    with open(file_name, "wb") as file:
        file.write(get(url).content)
class WeaponInfo():
    def __init__(self,bot):
        self.bot = bot
        self.bot.loop.run_in_executor(None,download,"http://starbright.dyndns.org/starwort/weapon_info.txt","weapon_info.txt")
        self.bot.loop.run_in_executor(None,download,"http://starbright.dyndns.org/starwort/prototypes.txt","prototypes.txt")
        tmp = open("weapon_info.txt")
        self.list = [[j.strip() for j in i.split("|")] for i in tmp.readlines()]
        tmp.close()
        tmp = open("prototypes.txt")
        self.prototypes = [[j.strip() for j in i.split("|")] for i in tmp.readlines()]
        tmp.close()
        self.matchlist = [i[0] for i in self.list]
        self.indexes = dict([(self.list[i][0],i) for i in range(len(self.list))])
        self.protoindexes = dict([(self.prototypes[i][0],i) for i in range(len(self.prototypes))])
    @commands.command(pass_context=True,aliases=["info", "winfo"])
    async def weaponinfo(self,ctx,*,weapon):
        match = process.extractOne(weapon,self.matchlist)
        if match[1] < 75:
            await ctx.send(f"That does not appear to be a weapon! The best match, {match[0]} was <75% ({match[1]}%)")
            return
        matchAcc = match[1]
        match = match[0]
        index = self.indexes[match]
        data = self.list[index]
        wdata = data[2:]
        wproto = self.prototypes[self.protoindexes[wdata[0]]]
        embed=Embed(title="Weapon Info", description=f"Info for weapon {match} (Search: {weapon})", colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))))
        embed.set_thumbnail(url=data[1])
        embed.add_field(name="Type:", value=wdata[0], inline=False)
        embed.add_field(name=wproto[1], value=wdata[1], inline=True)
        embed.add_field(name=wproto[2], value=wdata[2], inline=True)
        embed.add_field(name=wproto[3], value=wdata[3], inline=True)
        embed.add_field(name=wproto[4], value=wdata[4], inline=True)
        embed.add_field(name=wproto[5], value=f"{wdata[5]}%", inline=True)
        embed.add_field(name=wproto[6], value=f"{wdata[6]}%", inline=True)
        embed.add_field(name=wproto[7], value=f"{wdata[7]}p", inline=False)
        embed.add_field(name=wproto[8], value=(round(int(wdata[8])/10))*u"\u2588" + (10 - (round(int(wdata[8])/10)))*u"\u2591" + f" ({wdata[8]}/100)", inline=True)
        embed.add_field(name=wproto[9], value=(round(int(wdata[9])/10))*u"\u2588" + (10 - (round(int(wdata[9])/10)))*u"\u2591" + f" ({wdata[9]}/100)", inline=True)
        embed.add_field(name=wproto[10], value=(round(int(wdata[10])/10))*u"\u2588" + (10 - (round(int(wdata[10])/10)))*u"\u2591" + f" ({wdata[10]}/100)", inline=True)
        embed.set_footer(text=f"Requested by {str(ctx.author)}")
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(WeaponInfo(bot))
