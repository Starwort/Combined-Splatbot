from discord import *
from discord.ext import commands
import datetime
from random import choice, shuffle
from ast import literal_eval
import pygal
import aiofiles
class Miscellaneous():
    def __init__(self,bot):
        self.bot = bot
        self.yoshi_colours = [
            0x23c503, #green
            0x00b3e3, #light blue
            0x000000, #black
            0xff0000, #red
            0xf2dd00, #yellow
            0xffffff, #white
            0x0c0f63, #blue
            0xff9fc7, #pink
            0xd56000  #orange
        ]
        self.characters = [i.split(' | ') for i in '''Mario | https://vignette.wikia.nocookie.net/mariokart/images/d/d9/MK8_Mario_Icon.png/revision/latest?cb=20151225134138
Luigi | https://vignette.wikia.nocookie.net/mariokart/images/5/51/MK8_Luigi_Icon.png/revision/latest?cb=20151225134157
Peach | https://vignette.wikia.nocookie.net/mariokart/images/c/c2/MK8_Peach_Icon.png/revision/latest?cb=20151225134245
Daisy | https://vignette.wikia.nocookie.net/mariokart/images/3/32/MK8_Daisy_Icon.png/revision/latest?cb=20151225134324
Rosalina | https://vignette.wikia.nocookie.net/mariokart/images/8/89/MK8_Rosalina_Icon.png/revision/latest?cb=20151225134406
Tanooki Mario | https://vignette.wikia.nocookie.net/mariokart/images/a/a2/MK8_Tanooki_Mario_Icon.png/revision/latest?cb=20151225142802
Cat Peach | https://vignette.wikia.nocookie.net/mariokart/images/a/ad/MK8_Cat_Peach_Icon.png/revision/latest?cb=20151225142826
Yoshi | https://vignette.wikia.nocookie.net/mariokart/images/9/91/MK8_Yoshi_Icon.png/revision/latest?cb=20151225134454
Toad | https://vignette.wikia.nocookie.net/mariokart/images/4/45/MK8_Toad_Icon.png/revision/latest?cb=20151225140622
Koopa Troopa | https://vignette.wikia.nocookie.net/mariokart/images/b/bc/MK8_Koopa_Icon.png/revision/latest?cb=20151225140714
Shy Guy | https://vignette.wikia.nocookie.net/mariokart/images/7/7f/MK8_ShyGuy_Icon.png/revision/latest?cb=20151225140739
Lakitu | https://vignette.wikia.nocookie.net/mariokart/images/7/7d/MK8_Lakitu_Icon.png/revision/latest?cb=20151225141102
Toadette | https://vignette.wikia.nocookie.net/mariokart/images/8/8e/MK8_Toadette_Icon.png/revision/latest?cb=20151225141117
King Boo | https://vignette.wikia.nocookie.net/mariokart/images/1/1d/MK8DX_King_Boo_Icon.png/revision/latest?cb=20170525051418
Baby Mario | https://vignette.wikia.nocookie.net/mariokart/images/d/d2/MK8_BabyMario_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225141200
Baby Luigi | https://www.mariowiki.com/images/thumb/a/aa/MK8_BabyLuigi_Icon.png/120px-MK8_BabyLuigi_Icon.png
Baby Peach | http://www.mariowiki.com/images/thumb/3/3d/MK8_BabyPeach_Icon.png/120px-MK8_BabyPeach_Icon.png
Baby Daisy | https://www.mariowiki.com/images/thumb/4/43/MK8_BabyDaisy_Icon.png/120px-MK8_BabyDaisy_Icon.pnghttps://www.mariowiki.com/images/thumb/4/43/MK8_BabyDaisy_Icon.png/120px-MK8_BabyDaisy_Icon.png
Baby Rosalina | https://vignette.wikia.nocookie.net/mariokart/images/0/09/MK8_BabyRosalina_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225141356
Metal Mario / Gold Mario | https://vignette.wikia.nocookie.net/mariokart/images/c/c8/MK8DX_Gold_Mario_Icon.png/revision/latest/scale-to-width-down/42?cb=20170525053735
Pink Gold Peach | https://vignette.wikia.nocookie.net/mariokart/images/0/0d/MK8_PGPeach_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225141420
Wario | https://vignette.wikia.nocookie.net/mariokart/images/c/c2/MK8_Wario_Icon.png/revision/latest?cb=20151225141554
Waluigi | https://vignette.wikia.nocookie.net/mariokart/images/7/78/MK8_Waluigi_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225141627
Donkey Kong | https://vignette.wikia.nocookie.net/mariokart/images/0/08/MK8_DKong_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225141527
Bowser | https://vignette.wikia.nocookie.net/mariokart/images/4/47/MK8_Bowser_Icon.png/revision/latest/scale-to-width-down/40?cb=20151225141439
Dry Bones | https://vignette.wikia.nocookie.net/mariokart/images/3/3f/MK8DX_Dry_Bones_Icon.png/revision/latest/scale-to-width-down/42?cb=20170703120057
Bowser Jr. | https://vignette.wikia.nocookie.net/mariokart/images/2/26/MK8_Bowser_Jr_Icon.png/revision/latest/scale-to-width-down/42?cb=20170703120055
Dry Bowser | https://vignette.wikia.nocookie.net/mariokart/images/2/29/MK8_Dry_Bowser_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225143926
Lemmy | https://vignette.wikia.nocookie.net/mariokart/images/f/fc/MK8_Lemmy_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225142353
Larry | https://vignette.wikia.nocookie.net/mariokart/images/c/c2/MK8_Larry_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225142411
Wendy | https://vignette.wikia.nocookie.net/mariokart/images/d/d9/MK8_Wendy_Icon.png/revision/latest?cb=20151225142511
Ludwig | https://vignette.wikia.nocookie.net/mariokart/images/a/a8/MK8_Ludwig_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225142550
Iggy | https://vignette.wikia.nocookie.net/mariokart/images/d/dd/MK8_Iggy_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225142154JC 
Roy | https://vignette.wikia.nocookie.net/mariokart/images/3/3e/MK8_Roy_Icon.png/revision/latest?cb=20151225142325
Morton | https://vignette.wikia.nocookie.net/mariokart/images/7/72/MK8_Morton_Icon.png/revision/latest?cb=20151225142630
Inkling Girl | https://vignette.wikia.nocookie.net/mariokart/images/b/b9/MK8DX_Female_Inkling_Icon.png/revision/latest/scale-to-width-down/42?cb=20170525053712
Inkling Boy | https://vignette.wikia.nocookie.net/mariokart/images/3/3c/MK8DX_Male_Inkling_Icon.png/revision/latest/scale-to-width-down/42?cb=20170525053533
Link | https://vignette.wikia.nocookie.net/mariokart/images/e/e8/MK8_Link_Icon.png/revision/latest?cb=20151225143739
Villager (male) | https://vignette.wikia.nocookie.net/mariokart/images/1/16/VillagerMale-Icon-MK8.png/revision/latest/scale-to-width-down/42?cb=20151225143753
Villager (female) | https://vignette.wikia.nocookie.net/mariokart/images/c/c3/VillagerFemale-Icon-MK8.png/revision/latest/scale-to-width-down/42?cb=20151225143821
Isabelle | https://vignette.wikia.nocookie.net/mariokart/images/2/20/MK8_Isabelle_Icon.png/revision/latest/scale-to-width-down/42?cb=20151225143846
Mii | https://vignette.wikia.nocookie.net/mariokart/images/b/bb/Mii_MK8.png/revision/latest/scale-to-width-down/42?cb=20170703120057'''.split('\n')]
        self.battle_courses = [i.split(' | ') for i in '''Battle Course | https://vignette.wikia.nocookie.net/mariokart/images/1/10/MK8D-BattleStadium-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083848
Sweet Sweet Kingdom | https://vignette.wikia.nocookie.net/mariokart/images/8/8c/MK8D-SweetSweetKingdom-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083850
Dragon Palace | https://vignette.wikia.nocookie.net/mariokart/images/0/09/MK8D-DragonPalace-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083848
Lunar Colony | https://vignette.wikia.nocookie.net/mariokart/images/d/dc/MK8D-LunarColony-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083849
3DS Wuhu Town | https://vignette.wikia.nocookie.net/mariokart/images/2/21/MK8D-3DS-WuhuTown-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083847
GCN Luigi's Mansion | https://vignette.wikia.nocookie.net/mariokart/images/3/34/MK8D-GCN-LuigisMansion-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083849
SNES Battle Course 1 | https://vignette.wikia.nocookie.net/mariokart/images/1/1c/MK8D-SNES-BattleCourse1-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083849
Urchin Underpass | https://vignette.wikia.nocookie.net/mariokart/images/6/63/MK8D-UrchinUnderpass-icon.png/revision/latest/scale-to-width-down/160?cb=20170703083850'''.split('\n')]
        self.body_parts = [i.split(' | ')[0] for i in '''Standard Kart | https://www.mariowiki.com/images/0/05/StandardKartBodyMK8.png
Pipe Frame | https://www.mariowiki.com/images/d/d1/PipeFrameBodyMK8.png
Mach 8 | https://www.mariowiki.com/images/d/df/Mach8BodyMK8.png
Steel Driver | https://www.mariowiki.com/images/9/94/Steel_Driver.png
Cat Cruiser | https://www.mariowiki.com/images/f/f4/CatCruiserBodyMK8.png
Circuit Special | https://www.mariowiki.com/images/6/6c/CircuitSpecialBodyMK8.png
Tri-Speeder | https://vignette.wikia.nocookie.net/mariokart/images/5/56/TrispeederBodyMK8.png/revision/latest?cb=20141102123217
Badwagon | https://www.mariowiki.com/images/c/c2/BadwagonBodyMK8.png
Prancer | https://vignette.wikia.nocookie.net/mariokart/images/f/ff/PrancerBodyMK8.png/revision/latest?cb=20141102123333
Buggybud | https://www.mariowiki.com/images/4/45/BiddybuggyBodyMK8.png
Landship | https://www.mariowiki.com/images/6/6d/LandshipBodyMK8.png
Bounder | https://vignette.wikia.nocookie.net/mariokart/images/4/47/SneakerBodyMK8.png/revision/latest?cb=20141102123617
Sports Coupé | https://vignette.wikia.nocookie.net/mariokart/images/f/f8/SportsCoupeMK8.png/revision/latest?cb=20141102123625
Gold Kart | https://www.mariowiki.com/images/f/fe/Gold_Standard.png
GLA | https://www.mariowiki.com/images/c/c2/GLA-MK8.png
W 25 Silver Arrow | https://www.mariowiki.com/images/2/25/W25SilverArrow-MK8.png
300 SL Roadster | https://vignette.wikia.nocookie.net/mariokart/images/1/17/300SLRoadster-MK8.png/revision/latest?cb=20160102140332
Blue Falcon | https://www.mariowiki.com/images/f/f6/MK8BlueFalcon.png
Tanooki Kart | https://www.mariowiki.com/images/1/17/Tanooki-Buggy.png
B Dasher | https://www.mariowiki.com/images/1/15/ZeldaMK8Bdasher.png
Streetle | https://www.mariowiki.com/images/c/cf/MK8Streetle.png
P-Wing | https://www.mariowiki.com/images/c/cd/MK8PWing.png
Koopa Clown | https://vignette.wikia.nocookie.net/mariokart/images/7/70/MK8DX_Koopa_Clown.png/revision/latest?cb=20170704061052
Standard Bike | https://vignette.wikia.nocookie.net/mariokart/images/8/84/StandardBikeBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123849
The Duke | https://vignette.wikia.nocookie.net/mariokart/images/8/8a/TheDukeBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141001105819
Flame Rider | https://vignette.wikia.nocookie.net/mariokart/images/3/31/FlameRiderBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123942
Varmint | https://vignette.wikia.nocookie.net/mariokart/images/d/d0/VarmintBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123951
Mr Scooty | https://vignette.wikia.nocookie.net/mariokart/images/1/18/MrScootyBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123925
Master Cycle Zero | https://d1u5p3l4wpay3k.cloudfront.net/zelda_gamepedia_en/f/f4/MK8D_Master_Cycle_Zero_Icon.png?version=c0a0af5de5d50566b919ebcaf6362b68
City Tripper | https://vignette.wikia.nocookie.net/mariokart/images/9/90/MK8CityTripper.png/revision/latest/scale-to-width-down/100?cb=20150426175601
Comet [Inside drifter] | https://vignette.wikia.nocookie.net/mariokart/images/0/0e/CometBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124024
Sport Bike [Inside drifter] | https://vignette.wikia.nocookie.net/mariokart/images/f/fe/SportBikeBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123857
Jet Bike [Inside drifter] | https://vignette.wikia.nocookie.net/mariokart/images/1/12/JetBikeBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102123928
Yoshi Bike [Inside drifter] | https://vignette.wikia.nocookie.net/mariokart/images/6/62/YoshiBikeBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124032
Master Cycle [Inside drifter] | https://vignette.wikia.nocookie.net/mariokart/images/5/52/MK8_MasterCycle.png/revision/latest/scale-to-width-down/100?cb=20150331231734
Standard Quad | https://vignette.wikia.nocookie.net/mariokart/images/2/23/StandardATVBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124111
Wild Wiggler | https://vignette.wikia.nocookie.net/mariokart/images/a/aa/WildWigglerBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124116
Teddy Buggy | https://vignette.wikia.nocookie.net/mariokart/images/f/fa/TeddyBuggyBodyMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124120
Bone Rattler | https://vignette.wikia.nocookie.net/mariokart/images/0/0a/MK8BoneRattler.png/revision/latest/scale-to-width-down/100?cb=20150426180108
Splat Buggy | https://vignette.wikia.nocookie.net/mariokart/images/6/63/MK8DX_Splat_Buggy.png/revision/latest/scale-to-width-down/100?cb=20170706064814
Inkstriker | https://vignette.wikia.nocookie.net/mariokart/images/e/eb/MK8DX_Inkstriker.png/revision/latest/scale-to-width-down/100?cb=20170706065507'''.split('\n')]
        self.wheel_parts = [i.split(' | ')[0] for i in '''Normal / Normal Blue | https://vignette.wikia.nocookie.net/mariokart/images/a/a8/StandardTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102125545
Monster / Funky Monster | https://vignette.wikia.nocookie.net/mariokart/images/2/29/MonsterTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102125541
Roller / Azure Roller | https://vignette.wikia.nocookie.net/mariokart/images/7/76/RollerTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102125539
Slim / Crimson Slim | https://vignette.wikia.nocookie.net/mariokart/images/f/f8/SlimTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102125536
Slick / Cyber Slick | https://vignette.wikia.nocookie.net/mariokart/images/d/dd/SlickTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102125542
Metal | https://vignette.wikia.nocookie.net/mariokart/images/9/96/MetalTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124533
Button | https://vignette.wikia.nocookie.net/mariokart/images/0/07/ButtonTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124541
Off-Road / Retro Off-Road | https://vignette.wikia.nocookie.net/mariokart/images/2/25/Off-Road.png/revision/latest/scale-to-width-down/100?cb=20141102124559
Sponge | https://vignette.wikia.nocookie.net/mariokart/images/4/4c/SpongeTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124549
Wooden | https://vignette.wikia.nocookie.net/mariokart/images/0/03/WoodTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124724
Cushion | https://vignette.wikia.nocookie.net/mariokart/images/9/92/CushionTiresMK8.png/revision/latest/scale-to-width-down/100?cb=20141102124817
Gold Wheels | https://vignette.wikia.nocookie.net/mariokart/images/5/52/Gold_Tires_MK8.png/revision/latest/scale-to-width-down/100?cb=20141102125630
GLA Wheels | https://vignette.wikia.nocookie.net/mariokart/images/b/ba/GLATires-MK8.png/revision/latest/scale-to-width-down/100?cb=20150426180539
Triforce Tyres | https://vignette.wikia.nocookie.net/mariokart/images/0/09/MK8_TriforceTires.png/revision/latest/scale-to-width-down/100?cb=20150331233357
Ancient Tyres | https://d1u5p3l4wpay3k.cloudfront.net/zelda_gamepedia_en/9/94/MK8D_Ancient_Tires_Icon.png?version=6257042aa4235d03145a05e7a30bcc98
Leaf Tyres | https://vignette.wikia.nocookie.net/mariokart/images/f/f9/Leaf_Tires_MK8.png/revision/latest/scale-to-width-down/100?cb=20150426180810'''.split('\n')]
        self.glider_parts = '''Super Glider
Waddle Wing
Hylian Kite
Cloud Glider
Flower Glider
Paper Glider
Parachute
Wario Wing
Plane Glider
Peach Parasol
Parafoil
Bowser Kite
MKTV Parafoil
Gold Glider
Paraglider'''.split('\n')
        self.courses = {
            'Mushroom Cup':['Mario Kart Stadium', 'Water Park', 'Sweet Sweet Canyon', 'Thwomp Ruins'],
            'Flower Cup':['Mario Circuit','Toad Harbour','Twisted Mansion','Shy Guy Falls'],
            'Star Cup':['Sunshine Airport','Dolphin Shoals','Electrodrome','Mount Wario'],
            'Special Cup':['Cloudtop Cruise','Bone Dry Dunes','Bowser\'s Castle','Rainbow Road'],
            'Shell Cup':['Wii Moo Moo Meadows','GBA Mario Circuit','DS Cheep Cheep Beach','N64 Toad\'s Turnpike'],
            'Banana Cup':['GCN Dry Dry Desert','SNES Donut Plains 3','N64 Royal Raceway','3DS DK Jungle'],
            'Leaf Cup':['DS Wario Stadium','GCN Sherbet Land','3DS Melody Motorway','N64 Yoshi Valley'],
            'Lightning Cup':['DS Tick-Tock Clock','3DS Piranha Plant Pipeway','Wii Grumble Volcano','N64 Rainbow Road'],
            'Egg Cup':['GCN Yoshi Circuit','Excitebike Arena','Dragon Driftway','Mute City'],
            'Crossing Cup':['GCN Baby Park','GBA Cheese Land','Wild Woods','Animal Crossing'],
            'Triforce Cup':['Wii Wario\'s Gold Mine','SNES Rainbow Road','Ice Ice Outpost','Hyrule Circuit'],
            'Bell Cup':['3DS Koopa City','GBA Ribbon Road','Super Bell Subway','Big Blue']
        }
        self.cups = list(self.courses.keys())
    @commands.group(pass_context=True,aliases=['distribution'])
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
        shuffle(self.yoshi_colours)
        embed = Embed(description=f"Ping time: {round(self.bot.latency * 1000,3)}ms", colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_author(name="Pong!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def invite(self, ctx):
        '''Link to invite the bot'''
        shuffle(self.yoshi_colours)
        embed = Embed(description="To invite the bot to your server, click [here](https://discordapp.com/oauth2/authorize?client_id=424540163579052043&scope=bot&permissions=122944)", colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(pass_context=True, aliases=["suggestion"])
    async def support(self,ctx):
        '''Link to the support server'''
        shuffle(self.yoshi_colours)
        embed = Embed(description="If you need support or have a suggestion for the bot, click [here](https://discord.gg/3xuDR3G)", colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)))
        await ctx.send(embed=embed)
    @commands.command(aliases=['credit'])
    async def credits(self,ctx):
        '''Display credits for the bot's lists and other data'''
        credits = f'''Original weapon, mode and map lists (and the MK8D lists) created by {self.bot.get_user(196685856466010112)} at my request (he was very helpful when making the three bots that preceded this one)
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
    @commands.group(aliases=['mk','mk8','mariokart','mariokart8','mariokart8deluxe'])
    async def mk8d(self,ctx):
        '''Mario Kart 8 Deluxe randomiser commands'''
        if not ctx.invoked_subcommand:
            await ctx.send('You need to provide a subcommand! `{}help mk8d` for more information.'.format(self.bot.command_prefix(self.bot,ctx)[0]))
    @mk8d.command()
    async def character(self,ctx):
        '''Randomise your character'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.characters)
        char = choice(self.characters)
        wname = char[0]
        wurl = char[1]
        shuffle(self.yoshi_colours)
        embed = Embed(colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Character!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Character Chosen:", value=wname)
        await ctx.send(embed=embed)
    @mk8d.command()
    async def kart(self,ctx):
        '''Randomise your kart'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.body_parts)
        body = choice(self.body_parts)
        shuffle(self.wheel_parts)
        wheel = choice(self.wheel_parts)
        shuffle(self.glider_parts)
        glider = choice(self.glider_parts)
        wname = '\n'.join([body,wheel,glider])
        shuffle(self.yoshi_colours)
        embed = Embed(colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_author(name="Randomised Kart!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Kart Combination Chosen:", value=wname)
        await ctx.send(embed=embed)
    @mk8d.command()
    async def course(self,ctx):
        '''Randomise your course'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.cups)
        cup = choice(self.cups)
        shuffle(self.courses[cup])
        wname = choice(self.courses[cup])
        shuffle(self.yoshi_colours)
        embed = Embed(colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_author(name="Random Course!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Course Chosen:", value=wname)
        await ctx.send(embed=embed)
    @mk8d.command()
    async def cup(self,ctx):
        '''Randomise your cup'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.cups)
        wname = choice(self.cups)
        shuffle(self.yoshi_colours)
        embed = Embed(colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_author(name="Random Cup!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Cup Chosen:", value=wname)
        await ctx.send(embed=embed)
    @mk8d.command()
    async def battlecourse(self,ctx):
        '''Randomise your battle course'''
        url = ctx.author.avatar_url
        avatar = ctx.author.default_avatar_url if url == "" else url
        shuffle(self.battle_courses)
        char = choice(self.battle_courses)
        wname = char[0]
        wurl = char[1]
        shuffle(self.yoshi_colours)
        embed = Embed(colour=Colour(choice(self.yoshi_colours)), timestamp=datetime.datetime.now())
        embed.set_image(url=wurl)
        embed.set_author(name="Random Battle Course!", icon_url=ctx.me.avatar_url)
        embed.set_footer(text="Requested by {0}".format(str(ctx.author)), icon_url=avatar)
        embed.add_field(name="Battle Course Chosen:", value=wname)
        await ctx.send(embed=embed)
    @commands.command(aliases=['didthanoskillme','didthanoskill.me','didthanoskillme?','amidead','amidead?','didthanoskill'])
    async def thanos(self,ctx,target:Member=None):
        '''Did Thanos kill you?'''
        if not target: target = ctx.author
#        await ctx.send(f'Thanos {"killed" if ((not bool(target.id % 2)) or (HypeSquadHouse["balance"] not in target.hypesquad_houses)) else "spared"} {target.mention}.')
        await ctx.send(f'Thanos {"killed" if ((not bool(target.id % 2))) else "spared"} {target.mention}.')
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
