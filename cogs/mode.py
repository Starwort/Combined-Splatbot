from discord import *
from discord.ext import commands
from random import choice
import datetime
from requests import get  # to make GET request
from ast import literal_eval
import aiohttp
import asyncio
async def download(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get("url") as r:
            data = await r.text()
            with open(file_name, "wb") as file:
                file.write(data)
class Mode():
    def __init__(self,bot):
        self.bot = bot
        await download("http://starbright.dyndns.org/starwort/mode_list.txt","mode_list.txt")
        tmp = open("mode_list.txt")
        self.list = [i.strip() for i in tmp.readlines()]
        tmp.close()
    @commands.command(pass_context=True)
    async def mode(self,ctx):
        Mode = choice(self.list)
        Mode = Mode.split(" ")
        wname = " ".join(Mode[slice(len(Mode)-1)])
        distfile = open("modist")
        dist = literal_eval(distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        distfile.close()
        distfile = open("modist", "w")
        distfile.write(repr(dist))
        distfile.close()
        wurl = Mode[(len(Mode)-1)]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Mode!", icon_url="https://cdn.discordapp.com/avatars/424540163579052043/b67d194871881f83a7e67f3ed35a02ea.png?size=1024")
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)

        embed.add_field(name="Mode Chosen:", value=wname)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Mode(bot))
