import discord, asyncio, sys, re, inspect, itertools, traceback
from discord.ext import commands
from discord.ext.commands import formatter
from cogs.lib import uni
import random
empty = '\u200b'
orig_help = None
class Help(formatter.HelpFormatter):
    '''Formats help'''
    def __init__(self,bot,*args,**kwargs):
        self.bot = bot
        global orig_help
        orig_help = bot.get_command('help')
        self.bot.remove_command('help')
        self.bot.formatter = self
        self.bot.help_formatter = self
        super().__init__(*args,**kwargs)
    @commands.command(help='help.help')
    async def help(self,ctx,*cmds:str):
        """Shows help documentation.
        [p]help: Shows the help manual.
        [p]help <command>: Show help for a command
        [p]help <category>: Show commands and description for a category"""
        self.context = ctx
        async def addsub(commands):
            list_entries = []
            entries = ''
            for name,command in commands:
                if name in command.aliases:
                    continue
                new_short_doc = (await uni.translate(ctx,command.short_doc)).replace('[p]',self.bot.command_prefix(self.bot, ctx)[0])
                if self.is_cog() or self.is_bot():
                    name = '{0}{1}'.format(self.bot.command_prefix(self.bot,ctx)[0],name)
                if len(entries+'**{0}**  -  {1}\n'.format(name,new_short_doc)) > 1000:
                    list_entries.append(entries)
                    entries = ''
                entries += '**{0}**  -  {1}\n'.format(name, new_short_doc)
            list_entries.append(entries)
            return list_entries
        if len(cmds) == 0:
            self.command = self.bot
            emb = {
                'embed': {
                    'title': '',
                    'description': await uni.translate(ctx, 'help.desc')
                },
                'footer': {
                    'text': (await uni.translate(ctx,'help.footer')).format(self.bot.command_prefix(self.bot, ctx)[0])
                },
                'fields': []
            }
            nocat = await uni.translate(ctx,'help.no_category')
            def category(tup):
                cog = tup[1].cog_name
                return '**__{0}__**'.format(cog) if cog is not None else f'**__{nocat}__**'
            filtered = await self.filter_command_list()
            data = sorted(filtered,key=category)
            for category, commands in itertools.groupby(data, key=category):
                commands = sorted(commands)
                if len(commands) > 0:
                    for count,subcommands in enumerate(await addsub(commands)):
                        field = {
                            'inline': False
                        }
                        if count > 0:
                            field['name'] = category + ' {} {}'.format(await uni.translate(ctx, 'help.part'),count+1)
                        else:
                            field['name'] = category
                        field['value'] = subcommands
                        print(repr(subcommands))
                        emb['fields'].append(field)
            embeds = []
            random.shuffle(uni.squid_colors)
            embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
            embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(1), icon_url=ctx.me.avatar_url)
            embed.set_footer(**emb['footer'])
            txt = ''
            for field in emb['fields']:
                txt += field['name'] + field['value']
                if len(txt) > 1000:
                    embeds.append(embed)
                    txt = field['name'] + field['value']
                    del embed
                    random.shuffle(uni.squid_colors)
                    embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
                    embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(len(embeds)+1), icon_url=ctx.me.avatar_url)
                    embed.set_footer(**emb['footer'])
                embed.add_field(**field)
            embed.set_footer(**emb['footer'])
            embeds.append(embed)
            if len(embeds) == 1:
                embed = embeds[0]
                embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                await ctx.send(embed=embed)
                return
            help_msg = await ctx.send(embed = embeds[0])
            if ctx.channel.permissions_for(ctx.me).value & 65600 == 65600:
                home, back, forward, end = '⏮', '◀', '▶', '⏭'
                stop = '⏹'
                valid_r = [home,back,forward,end,stop]
                page = 0
                max_page = len(embeds)
                for i in valid_r:
                    await help_msg.add_reaction(i)
                await asyncio.sleep(0.1)
                #try:
                if True:
                    while True:
                        reaction,user = await self.bot.wait_for('reaction_add',timeout=120)
                        print(reaction.emoji)
                        try:
                            await help_msg.remove_reaction(reaction, user)
                        except:
                            pass
                        if reaction.emoji == home:
                            page = 0
                        elif reaction.emoji == back:
                            page -= 1
                        elif reaction.emoji == forward:
                            page += 1
                        elif reaction.emoji == end:
                            page = max_page - 1
                        elif reaction.emoji == stop:
                            break
                        page %= max_page
                        await help_msg.edit(embed=embeds[page])
                #except:
                #    pass
                await help_msg.delete()
            else:
                page_msg = await ctx.send((await uni.translate(self.context, 'help.page_msg')).format(len(embeds)))
                def is_not_me(msg):
                    if msg.author.id != self.bot.user.id and msg.channel == ctx.channel:
                        return True
                while True:
                    reply = await self.bot.wait_for('message', check=is_not_me)
                    try:
                        page_number = int(reply.content) - 1
                        if page_number < 0:
                            page_number = 0
                        elif page_number >= len(embeds):
                            page_number = len(embeds)-1
                        await help_msg.edit(embed=embeds[page_number])
                        try:
                            await reply.delete()
                        except:
                            pass
                    except ValueError:
                        await page_msg.edit(content=await uni.translate(self.context, 'help.quit'))
                        break
        elif len(cmds) == 1:
            name = cmds[0]
            command = None
            if name in self.bot.cogs:
                command = self.bot.cogs[name]
            else:
                command = self.bot.all_commands.get(name)
                if command is None:
                    random.shuffle(uni.squid_colors)
                    embed = discord.Embed(colour=random.choice(uni.squid_colors), title=(await uni.translate(ctx,'help.no_command')).format(name), description=await uni.translate(ctx,'help.command_not_found'))
                    embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                    await ctx.send(embed=embed)
                    return
                self.command = command
###################################################################################################
                emb = {
                    'embed': {
                        'description': await uni.translate(ctx, 'help.desc')
                    },
                    'footer': {
                        'text': (await uni.translate(ctx,'help.footer')).format(self.bot.command_prefix(self.bot, ctx)[0])
                    },
                    'fields': []
                }
                emb['embed']['description'] = '{1} {0}'.format(self.get_command_signature(),await uni.translate(ctx,'help.syntax'))
                if command.help:
                    name = (await uni.translate(ctx, command.help)).split('\n\n')[0]
                    name_length = len(name)
                    name = name.replace('[p]',self.bot.command_prefix(self.bot,ctx)[0])
                    value = (await uni.translate(ctx, command.help))[name_length:].replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])
                    if value == '':
                        name = '{0}'.format((await uni.translate(ctx, command.help)).replace('[p]',self.bot.command_prefix(self.bot,self.context)[0]).split('\n')[0])
                        name_length = len(name)
                        value = (await uni.translate(ctx, command.help))[name_length:].replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])
                    if value == '':
                        value = empty
                    if len(value) > 1024:
                        first = value[:1024].rsplit('\n', 1)[0]
                        list_values = [first, value[len(first):]]
                        while len(list_values[-1]) > 1024:
                            next_val = list_values[-1][:1024].rsplit('\n', 1)[0]
                            remaining = [next_val, list_values[-1][len(next_val):]]
                            list_values = list_values[:-1] + remaining
                        for new_val in list_values:
                            field = {
                                'name': name,
                                'value': new_val,
                                'inline': False
                            }
                            emb['fields'].append(field)
                    else:
                        field = {
                            'name': name,
                            'value': value,
                            'inline': False
                        }
                        emb['fields'].append(field)

                # end it here if it's just a regular command
                if not self.has_subcommands():
                    return emb
            filtered = sorted(await self.filter_command_list())
            if filtered:
                async def _add_subcommands(cmds):
                    list_entries = []
                    entries = ''
                    for name, command in cmds:
                        if name in command.aliases:
                            # skip aliases
                            continue
                        new_short_doc = (await uni.translate(self.context, command.short_doc)).replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])

                        if self.is_cog() or self.is_bot():
                            name = '{0}{1}'.format(self.bot.command_prefix(self.bot,self.context)[0], name)

                        if len(entries + '**{0}**  -  {1}\n'.format(name, new_short_doc)) > 1000:
                            list_entries.append(entries)
                            entries = ''
                        entries += '**{0}**  -  {1}\n'.format(name, new_short_doc)
                    list_entries.append(entries)
                    return list_entries
                for subcommands in await _add_subcommands(filtered):
                    field = {
                        'name': '**__{}:__**'.format(await uni.translate(ctx, 'help.commands')) if not self.is_bot() and self.is_cog() else '**__{}:__**'.format(await uni.translate(ctx, 'help.subcommands')),
                        'value': subcommands,
                        'inline': False
                    }
                    emb['fields'].append(field)
            embeds = []
            random.shuffle(uni.squid_colors)
            embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
            embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(1), icon_url=ctx.me.avatar_url)
            embed.set_footer(**emb['footer'])
            txt = ""
            for field in emb['fields']:
                txt += field["name"] + field["value"]
                if len(txt) > 1000:
                    embeds.append(embed)
                    txt = field["name"] + field["value"]
                    del embed
                    random.shuffle(uni.squid_colors)
                    embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
                    embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(len(embeds)+1), icon_url=ctx.me.avatar_url)
                    embed.set_footer(**emb['footer'])
                embed.add_field(**field)
            embed.set_footer(**emb['footer'])
            embeds.append(embed)
            if len(embeds) == 1:
                embed = embeds[0]
                embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                await ctx.send(embed=embed)
                return
            help_msg = await ctx.send(embed = embeds[0])
            if ctx.channel.permissions_for(ctx.me).value & 65600 == 65600:
                home, back, forward, end = '⏮', '◀', '▶', '⏭'
                stop = '⏹'
                valid_r = [home,back,forward,end,stop]
                page = 0
                max_page = len(embeds)
                for i in valid_r:
                    await help_msg.add_reaction(i)
                await asyncio.sleep(0.1)
                try:
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add',timeout=120)
                        try:
                            await help_msg.remove_reaction(reaction, user)
                        except:
                            pass
                        if reaction.emoji == home:
                            page = 0
                        elif reaction.emoji == back:
                            page -= 1
                        elif reaction.emoji == forward:
                            page += 1
                        elif reaction.emoji == end:
                            page = max_page - 1
                        elif reaction.emoji == stop:
                            break
                        page %= max_page
                        await help_msg.edit(embed = embeds[page])
                except:
                    pass
                await help_msg.delete()
            else:
                page_msg = await ctx.send((await uni.translate(self.context, 'help.page_msg')).format(len(embeds)))
                def is_not_me(msg):
                    if msg.author.id != self.bot.user.id and msg.channel == ctx.channel:
                        return True
                while True:
                    reply = await self.bot.wait_for('message', check=is_not_me)
                    try:
                        page_number = int(reply.content) - 1
                        if page_number < 0:
                            page_number = 0
                        elif page_number >= len(embeds):
                            page_number = len(embeds)-1
                        await help_msg.edit(embed=embeds[page_number])
                        try:
                            await reply.delete()
                        except:
                            pass
                    except ValueError:
                        await page_msg.edit(content=await uni.translate(self.context, 'help.quit'))
                        break
        else:
            name = cmds[0]
            command = self.bot.all_commands.get(name)
            if command is None:
                random.shuffle(uni.squid_colors)
                embed = discord.Embed(colour=random.choice(uni.squid_colors), title=(await uni.translate(ctx,'help.no_command')).format(name), description=await uni.translate(ctx,'help.command_not_found'))
                embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                await ctx.send(embed=embed)
                return
            for name in cmds[1:]:
                try:
                    command = self.bot.all_commands.get(name)
                    if command is None:
                        random.shuffle(uni.squid_colors)
                        embed = discord.Embed(colour=random.choice(uni.squid_colors), title=(await uni.translate(ctx,'help.no_command')).format(name), description=await uni.translate(ctx,'help.command_not_found'))
                        embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                        await ctx.send(embed=embed)
                        return
                except AttributeError:
                    random.shuffle(uni.squid_colors)
                    embed = discord.Embed(colour=random.choice(uni.squid_colors), title=(await uni.translate(ctx,'help.no_subcommands')).format(name), description=await uni.translate(ctx,'help.command_not_found'))
                    embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                    await ctx.send(embed=embed)
                    return
                self.command = command
                emb = {
                    'embed': {
                        'description': await uni.translate(ctx, 'help.desc')
                    },
                    'footer': {
                        'text': (await uni.translate(ctx,'help.footer')).format(self.bot.command_prefix(self.bot, ctx)[0])
                    },
                    'fields': []
                }
                emb['embed']['description'] = '{1} {0}'.format(self.get_command_signature(),await uni.translate(ctx,'help.syntax'))
                if command.help:
                    name = (await uni.translate(ctx, command.help)).split('\n\n')[0]
                    name_length = len(name)
                    name = name.replace('[p]',self.bot.command_prefix(self.bot,ctx)[0])
                    value = (await uni.translate(ctx, command.help))[name_length:].replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])
                    if value == '':
                        name = '{0}'.format((await uni.translate(ctx, command.help)).replace('[p]',self.bot.command_prefix(self.bot,self.context)[0]).split('\n')[0])
                        name_length = len(name)
                        value = (await uni.translate(ctx, command.help))[name_length:].replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])
                    if value == '':
                        value = empty
                    if len(value) > 1024:
                        first = value[:1024].rsplit('\n', 1)[0]
                        list_values = [first, value[len(first):]]
                        while len(list_values[-1]) > 1024:
                            next_val = list_values[-1][:1024].rsplit('\n', 1)[0]
                            remaining = [next_val, list_values[-1][len(next_val):]]
                            list_values = list_values[:-1] + remaining
                        for new_val in list_values:
                            field = {
                                'name': name,
                                'value': new_val,
                                'inline': False
                            }
                            emb['fields'].append(field)
                    else:
                        field = {
                            'name': name,
                            'value': value,
                            'inline': False
                        }
                        emb['fields'].append(field)
                # end it here if it's just a regular command
                if not self.has_subcommands():
                    return emb
            filtered = sorted(await self.filter_command_list())
            if filtered:
                async def _add_subcommands(cmds):
                    list_entries = []
                    entries = ''
                    for name, command in cmds:
                        if name in command.aliases:
                            # skip aliases
                            continue
                        new_short_doc = (await uni.translate(self.context, command.short_doc)).replace('[p]', self.bot.command_prefix(self.bot,self.context)[0])

                        if self.is_cog() or self.is_bot():
                            name = '{0}{1}'.format(self.bot.command_prefix(self.bot,self.context)[0], name)

                        if len(entries + '**{0}**  -  {1}\n'.format(name, new_short_doc)) > 1000:
                            list_entries.append(entries)
                            entries = ''
                        entries += '**{0}**  -  {1}\n'.format(name, new_short_doc)
                    list_entries.append(entries)
                    return list_entries
                for subcommands in await _add_subcommands(filtered):
                    field = {
                        'name': '**__{}:__**'.format(await uni.translate(ctx, 'help.commands')) if not self.is_bot() and self.is_cog() else '**__{}:__**'.format(await uni.translate(ctx, 'help.subcommands')),
                        'value': subcommands,
                        'inline': False
                    }
                    emb['fields'].append(field)
            embeds = []
            random.shuffle(uni.squid_colors)
            embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
            embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(1), icon_url=ctx.me.avatar_url)
            embed.set_footer(**emb['footer'])
            txt = ""
            for field in emb['fields']:
                txt += field["name"] + field["value"]
                if len(txt) > 1000:
                    embeds.append(embed)
                    txt = field["name"] + field["value"]
                    del embed
                    random.shuffle(uni.squid_colors)
                    embed = discord.Embed(colour=random.choice(uni.squid_colors), **emb['embed'])
                    embed.set_author(name=(await uni.translate(ctx, 'help.page')).format(len(embeds)+1), icon_url=ctx.me.avatar_url)
                    embed.set_footer(**emb['footer'])
                embed.add_field(**field)
            embed.set_footer(**emb['footer'])
            embeds.append(embed)
            if len(embeds) == 1:
                embed = embeds[0]
                embed.set_author(name=await uni.translate(ctx,'help.manual'),icon_url=ctx.me.avatar_url)
                await ctx.send(embed=embed)
                return
            help_msg = await ctx.send(embed = embeds[0])
            if ctx.channel.permissions_for(ctx.me).value & 65600 == 65600:
                home, back, forward, end = '⏮', '◀', '▶', '⏭'
                stop = '⏹'
                valid_r = [home,back,forward,end,stop]
                page = 0
                max_page = len(embeds)
                for i in valid_r:
                    await help_msg.add_reaction(i)
                await asyncio.sleep(0.1)
                try:
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add',timeout=120)
                        try:
                            await help_msg.remove_reaction(reaction, user)
                        except:
                            pass
                        if reaction.emoji == home:
                            page = 0
                        elif reaction.emoji == back:
                            page -= 1
                        elif reaction.emoji == forward:
                            page += 1
                        elif reaction.emoji == end:
                            page = max_page - 1
                        elif reaction.emoji == stop:
                            break
                        
                        page %= max_page
                        await help_msg.edit(embed=embeds[page])
                except:
                    pass
                await help_msg.delete()
            else:
                page_msg = await ctx.send((await uni.translate(self.context, 'help.page_msg')).format(len(embeds)))
                def is_not_me(msg):
                    if msg.author.id != self.bot.user.id and msg.channel == ctx.channel:
                        return True
                while True:
                    reply = await self.bot.wait_for('message', check=is_not_me)
                    try:
                        page_number = int(reply.content) - 1
                        if page_number < 0:
                            page_number = 0
                        elif page_number >= len(embeds):
                            page_number = len(embeds)-1
                        await help_msg.edit(embed=embeds[page_number])
                        try:
                            await reply.delete()
                        except:
                            pass
                    except ValueError:
                        await page_msg.edit(content=await uni.translate(self.context, 'help.quit'))
                        break
    def __unload(self):
        self.bot.formatter = formatter.HelpFormatter()
        self.bot.add_command(orig_help)
def setup(bot):
    bot.add_cog(Help(bot))