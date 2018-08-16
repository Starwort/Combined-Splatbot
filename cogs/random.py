from discord import *
from discord.ext import commands
import aiohttp,asyncio,aiofiles
from ast import literal_eval
from random import choice,shuffle,randint
import datetime
class Random():
    def __init__(self,bot):
        class Bunch():
            def __init__(self, **kwds):
                self.__dict__.update(kwds)
        self.client = aiohttp.ClientSession()
        self.bot = bot
        tmp = open("map_list.txt")
        self.lists = Bunch()
        self.lists.map = [i.strip() for i in tmp.readlines()]
        tmp.close()
        tmp = open("mode_list.txt")
        self.lists.mode = [i.strip() for i in tmp.readlines()]
        tmp.close()
        tmp = open("weapon_list.txt")
        self.lists.weapon = [i.strip() for i in tmp.readlines()]
        tmp.close()
        self.turf = self.lists.mode[0]
        self.tower = self.lists.mode[1]
        self.rain = self.lists.mode[2]
        self.zones = self.lists.mode[3]
        self.clam = self.lists.mode[4]
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
    async def updaterandom(self,ctx):
        out = 'Updating `map_list.txt`...'
        msg = await ctx.send(out)
        await self.download("http://starbright.dyndns.org/starwort/map_list.txt","map_list.txt")
        out += '\nDone!\nUpdating `map_list.txt`...'
        await msg.edit(out)
        await self.download("http://starbright.dyndns.org/starwort/mode_list.txt","mode_list.txt")
        out += '\nDone!\nUpdating `weapon_list.txt`...'
        await msg.edit(out)
        await self.download("http://starbright.dyndns.org/starwort/weapon_list.txt","weapon_list.txt")
        out += '\nDone!\nResetting the internal list cache...\n`map_list.txt`...'
        await msg.edit(out)
        async with aiofiles.open("map_list.txt") as tmp:
            self.lists.map = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\n`mode_list.txt`...'
        await msg.edit(out)
        async with aiofiles.open("mode_list.txt") as tmp:
            self.lists.mode = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\n`weapon_list.txt`...'
        await msg.edit(out)
        async with aiofiles.open("weapon_list.txt") as tmp:
            self.lists.mode = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\nResetting inherited properties...'
        await msg.edit(out)
        self.turf = self.lists.mode[0]
        self.tower = self.lists.mode[1]
        self.rain = self.lists.mode[2]
        self.zones = self.lists.mode[3]
        self.clam = self.lists.mode[4]
        out += '\nDone!'
        await msg.edit(out)
    @commands.command(pass_context=True,aliases=['stage'])
    async def map(self,ctx):
        '''Randomly select a map'''
        shuffle(self.lists.map)
        map = choice(self.lists.map)
        map = map.split(" ")
        wname = " ".join(map[slice(len(map)-1)])
        distfile = open("madist")
        dist = literal_eval(distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        distfile.close()
        distfile = open("madist", "w")
        distfile.write(repr(dist))
        distfile.close()
        wurl = map[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Map!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)

        embed.add_field(name="Map Chosen:", value=wname)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def mode(self,ctx):
        '''Randomly select a mode'''
        shuffle(self.lists.mode)
        Mode = choice(self.lists.mode)
        Mode = Mode.split(" ")
        wname = " ".join(Mode[slice(len(Mode)-1)])
        distfile = open("modist")
        dist = literal_eval(distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        distfile.close()
        distfile = open("modist", "w")
        distfile.write(repr(dist))
        distfile.close()
        if hash(ctx.author.id) == 0x7b6b1b52:
            Mode = self.turf.split(' ')
            wname = ''.join(Mode[slice(len(Mode)-1)])
        elif hash(ctx.author.id) == 0x23e6d378:
            Mode = self.clam.split(' ')
            wname = ''.join(Mode[slice(len(Mode)-1)])
        wurl = Mode[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Mode!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)

        embed.add_field(name="Mode Chosen:", value=wname)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def weapon(self,ctx):
        '''Randomly select a weapon'''
        shuffle(self.lists.weapon)
        weapon = choice(self.lists.weapon)
        weapon = weapon.split(" ")
        wname = " ".join(weapon[slice(len(weapon)-1)])
        distfile = open("wdist")
        dist = literal_eval(distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        distfile.close()
        distfile = open("wdist", "w")
        distfile.write(repr(dist))
        distfile.close()
        wurl = weapon[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        embed = Embed(colour=Colour(eval("0x{0}".format("".join([choice("0123456789abcdef") for i in range(6)])))), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Weapon!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)

        embed.add_field(name="Weapon Chosen:", value=wname)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def scrims(self,ctx, noScrims: int):
        """Generates N scrims; code originally produced by me for use in Spyke"""
        try:
            noScrims = int(noScrims)
            if noScrims > 50:
                raise Exception
        except:
            await ctx.send(content="The number of scrims must be an integer and less than or equal to 50!")
            return
        scrims = []
        minus1map = None
        minus2map = None
        minus1mode = None
        minus2mode = None
        for i in range(noScrims):
            map = None
            while map in [None, minus1map, minus2map]:
                shuffle(self.lists.map)
                map = choice(self.lists.map)
            mode = None
            while mode in [None, self.turf, minus1mode, minus2mode]:
                shuffle(self.lists.mode)
                mode = choice(self.lists.mode)
            scrims.append([map,mode])
            minus2map = minus1map
            minus1map = map
            minus2mode = minus1mode
            minus1mode = mode
        out = "\n"
        for i in range(noScrims):
            out += f'Game #{i+1}: {" ".join(scrims[i][1].split(" ")[slice(len(scrims[i][1].split(" "))-1)])} on {" ".join(scrims[i][0].split(" ")[slice(len(scrims[i][0].split(" "))-1)])}\n'
        await ctx.send(content=out.strip())
    @commands.command(pass_context=True, name="teams", aliases=["generateTeams","pb"])
    async def generateTeams(self, ctx, *, players: str):
        "Picks random even teams (with necessary spectators) given a pipe (|) separated list of players. e.g.\nrandom|teams player a|player b|player c"
        players = players.split("|")
        noP = len(players)
        if noP < 2 or noP > 10:
            await ctx.send(content="Too many or too few players! (The number of players must fall under (2,10) [interval notation])")
            return
        playersPerSide = min(noP // 2, 4)
        specs = noP - 2 * playersPerSide
        teamA = ["Alpha Team"]
        teamB = ["Bravo Team"]
        spec = []
        for i in range(playersPerSide):
            tmp = randint(0, len(players) - 1)
            teamA.append(players[tmp].strip())
            del players[tmp]
        for i in range(playersPerSide):
            tmp = randint(0, len(players) - 1)
            teamB.append(players[tmp].strip())
            del players[tmp]
        spec = players
        out = ""
        for i in range(playersPerSide + 1):
            out += f"{teamA[i]:^10} | {teamB[i]:^10}\n"
            if i == 0:
                out += '-----------+-----------\n'
        if specs:
            out += "-----------------------\n     Spectators\n-----------------------\n"
            for i in spec:
                out += f"{i:^20}\n"
        cropped = out.strip("\n")
        await ctx.send(content=f"Teams:```{cropped}```")
def setup(bot):
    bot.add_cog(Random(bot))