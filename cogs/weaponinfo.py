from discord import *
from discord.ext import commands
from random import choice, shuffle
import datetime
from fuzzywuzzy import process
import asyncio, aiohttp, aiofiles
import sys
import os
class WeaponInfo():
    def __init__(self,bot):
        self.client = aiohttp.ClientSession()
        self.bot = bot
        with open("weapon_info.txt") as tmp:
            self.list = [[j.strip() for j in i.split("|")] for i in tmp.readlines()]
        with open("prototypes.txt") as tmp:
            self.prototypes = [[j.strip() for j in i.split("|")] for i in tmp.readlines()]
        self.matchlist = [i[0] for i in self.list]
        self.indexes = dict([(self.list[i][0],i) for i in range(len(self.list))])
        self.protoindexes = dict([(self.prototypes[i][0],i) for i in range(len(self.prototypes))])
        self.squid_colours = [ 
            0xfe447d, # pink
            0xf78f2e, # orange
            0xfedc0c, # yellow orange
            0xd1f20a, # lime green
            0x5cd05b, # emerald green
            0x03c1cd, # teal
            0x0e10e6, # blue
            0x9208e7, # violet
            0xf84c00, # red violet
            0xf3f354, # yellow
            0xbff1e5, # mint
            0x3bc335, # green
            0x7af5ca, # sea green
            0x448bff, # light blue
            0x101ab3, # dark blue
            0xd645c8, # fuchsia
            0x0afe15, # neon green
            0x0acdfe, # cyan
            0xff9600, # neon orange
            0xb21ca1  # dark fuchsia
        ]
    def __unload(self):
        asyncio.get_event_loop().create_task(self.client.close())
    async def get(self,*args, **kwargs):
        response = await self.client.request('GET', *args, **kwargs)
        return await response.read()
    async def download(self,url, name):
        content = await self.get(url)
        async with aiofiles.open(name,'wb') as file:
            await file.write(content)
    @commands.command(hidden=True)
    @commands.is_owner()
    async def updatelists(self,ctx):
        await ctx.send('Updating `weapon_info.txt`...')
        await self.download("http://starbright.dyndns.org/starwort/weapon_info.txt","weapon_info.txt")
        await ctx.send('Done!\nUpdating `prototypes.txt`...')
        await self.download("http://starbright.dyndns.org/starwort/prototypes.txt","prototypes.txt")
        await ctx.send('Done!')
        await ctx.send('Resetting the internal list cache...\n`weapon_info.txt`...')
        async with aiofiles.open("weapon_info.txt") as tmp:
            self.list = [[j.strip() for j in i.split("|")] for i in await tmp.readlines()]
        await ctx.send('Done!\n`prototypes.txt`...')
        async with aiofiles.open("prototypes.txt") as tmp:
            self.prototypes = [[j.strip() for j in i.split("|")] for i in await tmp.readlines()]
        await ctx.send('Done!\nSetting inherited variables...')
        self.matchlist = [i[0] for i in self.list]
        self.indexes = dict([(self.list[i][0],i) for i in range(len(self.list))])
        self.protoindexes = dict([(self.prototypes[i][0],i) for i in range(len(self.prototypes))])
        await ctx.send('Done!')
    @commands.command(pass_context=True,aliases=["info", "winfo"])
    async def weaponinfo(self,ctx,*,weapon):
        '''
        This command gets you weapon info.
        '''
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
        shuffle(self.squid_colours)
        embed=Embed(title="Weapon Info", description=f"Info for weapon {match} (Search: {weapon})", colour=Colour(choice(self.squid_colours)))
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
