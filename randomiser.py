from discord import *
from discord.ext import commands
import time
from os import listdir
from os.path import isfile, join
from requests import get  # to make GET request
from ast import literal_eval
def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)
import sys, traceback
description = """A bot to randomise weapons for Splatoon 2

List of weapons created by Yosho from Ink2Death and maintained by Starwort#6129"""
cogs_dir = "cogs"
properties = open("randomiser.properties")
values = properties.readlines()
properties.close()
token = values[0].strip("\n")
pre = values[1].strip("\n")
with open('prefixes.txt') as file:
    prefixes = literal_eval(file.read())
def prefix(bot, ctx):
    global pre
    prefixes = bot.additionalprefixdata
    if type(ctx) == commands.Context:
        ctx = ctx.message
    try:
        extraprefix = prefixes[ctx.guild.id]
    except KeyError:
        extraprefix = None
    except AttributeError:
        print('we in dm')
        extraprefix = ''
    if extraprefix is not None:
        print('we adding a prefix which is '+repr(extraprefix))
        prefix = [extraprefix, pre]
    else:
        prefix = [pre]
    newpre = commands.when_mentioned_or(*prefix)(bot, ctx)
    #print(repr(newpre))
    return newpre
bot = commands.Bot(command_prefix=prefix, description=description)
bot.additionalprefixdata = prefixes
@bot.event
async def on_ready():
    print("Logged in as\n{0} ({1})\n--------------------".format(bot.user.name,bot.user.id))
    t = time.time()
    bot.startuptime = time.strftime("(UTC) %H:%M:%S on %d/%m/%Y", time.gmtime(t))
    await bot.change_presence(activity=Game(name="Doing all sorts of stuff in {2} guilds since {0}\nPrefix: {1}".format(bot.startuptime,pre,len(bot.guilds))))
@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=Game(name="Doing all sorts of stuff in {2} guilds since {0}\nPrefix: {1}".format(bot.startuptime,pre,len(bot.guilds))))
@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=Game(name="Doing all sorts of stuff in {2} guilds since {0}\nPrefix: {1}".format(bot.startuptime,pre,len(bot.guilds))))
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()
    bot.run(token, bot=True, reconnect=True)
