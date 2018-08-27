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
        tmp = open('ability_list.txt')
        self.lists.ability = literal_eval(tmp.read())
        tmp.close()
        self.turf = self.lists.mode[0]
        self.tower = self.lists.mode[1]
        self.rain = self.lists.mode[2]
        self.zones = self.lists.mode[3]
        self.clam = self.lists.mode[4]
        self.trollweps = [self.lists.weapon[i] for i in [8,9,10,15,16,17,32,33,34,35,66,73]]
        self.pp = self.lists.map[18]
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
    async def updaterandom(self,ctx):
        out = 'Updating `map_list.txt`...'
        msg = await ctx.send(content=out)
        await self.download("http://starbright.dyndns.org/starwort/map_list.txt","map_list.txt")
        out += '\nDone!\nUpdating `map_list.txt`...'
        await msg.edit(content=out)
        await self.download("http://starbright.dyndns.org/starwort/mode_list.txt","mode_list.txt")
        out += '\nDone!\nUpdating `weapon_list.txt`...'
        await msg.edit(content=out)
        await self.download("http://starbright.dyndns.org/starwort/weapon_list.txt","weapon_list.txt")
        out += '\nDone!\nUpdating `ability_list.txt`...'
        await msg.edit(content=out)
        await self.download("http://starbright.dyndns.org/starwort/ability_list.txt","ability_list.txt")
        out += '\nDone!\nResetting the internal list cache...\n`map_list.txt`...'
        await msg.edit(content=out)
        async with aiofiles.open("map_list.txt") as tmp:
            self.lists.map = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\n`mode_list.txt`...'
        await msg.edit(content=out)
        async with aiofiles.open("mode_list.txt") as tmp:
            self.lists.mode = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\n`weapon_list.txt`...'
        await msg.edit(content=out)
        async with aiofiles.open("weapon_list.txt") as tmp:
            self.lists.weapon = [i.strip() for i in await tmp.readlines()]  
        out += '\nDone!\n`ability_list.txt`...'
        await msg.edit(content=out)
        async with aiofiles.open("ability_list.txt") as tmp:
            self.lists.ability = literal_eval(await tmp.read()) 
        out += '\nDone!\nResetting inherited properties...'
        await msg.edit(content=out)
        self.turf = self.lists.mode[0]
        self.tower = self.lists.mode[1]
        self.rain = self.lists.mode[2]
        self.zones = self.lists.mode[3]
        self.clam = self.lists.mode[4]
        self.trollweps = [self.lists.weapon[i] for i in [8,9,10,15,16,17,32,33,34,35,66,73]]
        self.pp = self.lists.map[18]
        out += '\nDone!'
        await msg.edit(content=out)
    @commands.command(pass_context=True,aliases=['stage'])
    async def map(self,ctx):
        '''Randomly select a map'''
        shuffle(self.lists.map)
        map = choice(self.lists.map)
        map = map.split(" ")
        wname = " ".join(map[slice(len(map)-1)])
        async with aiofiles.open("madist") as distfile:
            dist = literal_eval(await distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        async with aiofiles.open("madist", "w") as distfile:
            await distfile.write(repr(dist))
        if hash(ctx.author.id) in [0x4e6dd1e0484001c]:
            map = self.pp
            wname = " ".join(map[slice(len(map)-1)])
        wurl = map[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.squid_colours)
        embed = Embed(colour=Colour(choice(self.squid_colours)), timestamp=datetime.datetime.now())
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
        async with aiofiles.open("modist") as distfile:
            dist = literal_eval(await distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        async with aiofiles.open("modist", "w") as distfile:
            await distfile.write(repr(dist))
        if hash(ctx.author.id) in [0x3758da974800000]:
            Mode = self.turf.split(' ')
            wname = ' '.join(Mode[slice(len(Mode)-1)])
        elif hash(ctx.author.id) in [0x4f169bc1a040000,0x4e6dd1e0484001c]:
            Mode = self.clam.split(' ')
            wname = ' '.join(Mode[slice(len(Mode)-1)])
        wurl = Mode[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.squid_colours)
        embed = Embed(colour=Colour(choice(self.squid_colours)), timestamp=datetime.datetime.now()) 
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
        async with aiofiles.open("wdist") as distfile:
            dist = literal_eval(await distfile.read())
        dist[wname] = dist.get(wname, 0) + 1
        async with aiofiles.open("wdist", "w") as distfile:
            await distfile.write(repr(dist))
        if hash(ctx.author.id) in [0x4e6dd1e0484001c]:
            shuffle(self.trollweps)
            weapon = choice(self.trollweps)
            weapon = weapon.split(" ")
            wname = " ".join(weapon[slice(len(weapon)-1)])
        wurl = weapon[-1]
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.squid_colours)
        embed = Embed(colour=Colour(choice(self.squid_colours)), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Weapon!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Weapon Chosen:", value=wname)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True,aliases=['scrim'])
    async def scrims(self,ctx, noScrims: int = 1):
        """Generates N scrims; code originally produced by me for use in Spyke"""
        try:
            noScrims = int(noScrims)
            if noScrims > 50 or noScrims <= 0:
                raise Exception
        except:
            await ctx.send(content="The number of scrims must be an integer, more than 0, and less than or equal to 50!")
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
            out += f'{f"Game #{i+1}: " if noScrims > 1 else ""}{" ".join(scrims[i][1].split(" ")[slice(len(scrims[i][1].split(" "))-1)])} on {" ".join(scrims[i][0].split(" ")[slice(len(scrims[i][0].split(" "))-1)])}\n'
        await ctx.send(content=out.strip())
    @commands.command(pass_context=True, name="teams", aliases=["generateTeams","pb"])
    async def generateTeams(self, ctx, *, players: str):
        '''Picks random even teams (with necessary spectators) given a pipe (|) separated list of players. e.g.\n[p]teams player a | player b | player c'''
        players = players.split('\\|\\|\\')
        trollPlayer = int(players[1].strip())
        players = players[0].split("|")
        noP = len(players) - (1 if trollPlayer is not None else 0)
        if noP < 2 or len(players) > 10:
            await ctx.send(content="Too many or too few players! (The number of players must fall under `[2,10]` [interval notation])")
            return
        playersPerSide = min(noP // 2, 4)
        specs = noP - 2 * playersPerSide
        teamA = ["Alpha Team"]
        teamB = ["Bravo Team"]
        spec = []
        if trollPlayer is not None:
            spec += [players.pop(trollPlayer)]
        for i in range(playersPerSide):
            tmp = randint(0, noP - 1)
            teamA.append(players.pop(tmp).strip())
        for i in range(playersPerSide):
            tmp = randint(0, noP - 1)
            teamB.append(players.pop(tmp).strip())
        spec += players
        out = ""
        for i in range(playersPerSide + 1):
            out += f"{teamA[i]:^10} | {teamB[i]:^10}\n"
            if i == 0:
                out += '-----------+-----------\n'
        if specs:
            out += "-----------------------\n      Spectators\n-----------------------\n"
            for i in spec:
                out += f"{i:^20}\n"
        cropped = out.strip("\n")
        await ctx.send(content=f"Teams:```{cropped}```")
    @commands.command()
    async def gear(self,ctx,gearType:str = 'pure',displayType:str = 'both'):
        '''Randomises your gear abilities for you e.g. for PB.

Gear Types:
 - pure
  -> Assumed you have every piece of gear as having the same main and all three sub abilities
  -> Disables main-only gear abilities
  -> Default mode
 - triad
  -> Assumed all your gear has the same three sub abilities, but not necessarily the matching main
 - random
  -> This mode is completely useless, the main and sub abilities are completely random, no pattern
  -> It is highly recommended to not use this mode

Display Types:
 - name
  -> Display the gear abilities with name only
 - emoji
  -> Display the gear abilities with emoji only
 - both
  -> Display the gear abilities with both name and emoji
  -> Default mode'''
        gearType = gearType.lower()
        displayType = displayType.lower()   
        if gearType not in ['pure','triad','random']:
            await ctx.send('That isn\'t a valid gear type')
            return
        elif displayType not in ['name','emoji','both']:
            await ctx.send('That isn\'t a valid display mode')
            return
        gear = {
            'head': {
                'main': None,
                'sub1': None,
                'sub2': None,
                'sub3': None
            },
            'body': {
                'main': None,
                'sub1': None,
                'sub2': None,
                'sub3': None
            },
            'shoe': {
                'main': None,
                'sub1': None,
                'sub2': None,
                'sub3': None
            }
        }
        if gearType == 'pure':
            for i in gear.keys():
                ab = self.lists.ability['all'][choice(list(self.lists.ability['all'].keys()))]
                for j in gear[i].keys():
                    gear[i][j] = ab
        elif gearType == 'triad':
            for i in gear.keys():
                gear[i]['main'] = self.lists.ability[i][choice(list(self.lists.ability[i].keys()))]
                ab = self.lists.ability['all'][choice(list(self.lists.ability['all'].keys()))]
                gear[i]['sub1'] = ab
                gear[i]['sub2'] = ab
                gear[i]['sub3'] = ab
        elif gearType == 'random':
            for i in gear.keys():
                gear[i]['main'] = self.lists.ability[i][choice(list(self.lists.ability[i].keys()))]
                for j in range(3):
                    gear[i][f'sub{j+1}'] = self.lists.ability['all'][choice(list(self.lists.ability['all'].keys()))]
        formats = {
            'name':'{0[0]}\n\n{1[0]}\n{2[0]}\n{3[0]}',
            'emoji':'{0[1]}\n\n{1[1]}\n{2[1]}\n{3[1]}',
            'both':'{0[1]} {0[0]}\n\n{1[1]} {1[0]}\n{2[1]} {2[0]}\n{3[1]} {3[0]}'
        }
        shuffle(self.squid_colours)
        embed = Embed(title='Randomised Gear Abilities',description=f'Gear Type: {gearType.title()}',colour=Colour(choice(self.squid_colours)), timestamp=datetime.datetime.now())
        embed.add_field(name='Headgear',value=formats[displayType].format(gear["head"]["main"],gear["head"]["sub1"],gear["head"]["sub2"],gear["head"]["sub3"]),inline=True)
        embed.add_field(name='Clothes',value=formats[displayType].format(gear["body"]["main"],gear["body"]["sub1"],gear["body"]["sub2"],gear["body"]["sub3"]),inline=True)
        embed.add_field(name='Shoes',value=formats[displayType].format(gear["shoe"]["main"],gear["shoe"]["sub1"],gear["shoe"]["sub2"],gear["shoe"]["sub3"]),inline=True)
        """ abilities = {}
        for i in gear.keys():
            for j in gear[i].keys():
                abilities[gear[i][j]] = abilities.get(gear[i][j],0) + 1
                if j == 'main':
                    abilities[gear[i][j]] += 2
        embed.add_field(name='Total Power Increase (in equivalent sub-abilities)',value='\n'.join([f'{i[1]}x{abilities[i]}' for i in abilities.keys()])) """
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Random(bot))