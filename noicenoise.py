import discord, os
from discord.errors import ClientException
from discord.ext import commands, tasks
from discord.player import FFmpegPCMAudio
from embedder import embeds
from noicenoiselib import nnlib

arrows_emojis = ['⬆️', '⬇️', '➡️', '⬅️']
num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

container = {}
epinfcontainer = {}
epcontainer = {}

bot=commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    print('bot is online.')

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if not user.bot and message.author == bot.user:
        global container
        await message.remove_reaction(str(reaction), user)
        args = message.embeds[0].footer.text.split("-")
        try:limit, categorytype = int(args[2]), args[1]
        except IndexError:pass
        
        text_channel = message.channel
        guild = message.guild
        try:
            voice_channel = user.voice.channel
        except AttributeError:
            await text_channel.send("Please connect to a voice channel before using command.")
        reaction = str(reaction)

        if reaction in arrows_emojis[:2]:
            if reaction == arrows_emojis[0]:limit -= 5
            if reaction == arrows_emojis[1]:limit += 5
            if limit < 5:limit = 5
            
            if args[0] == "PDLS":
                data = nnlib.getPodcastslist(categorytype)
                embed = embeds.listenEmbed(data, categorytype, limit)
                await message.edit(embed=embed)
                
            if args[0] == "PCI":
                data = nnlib.getEpisodesInfo(categorytype) #not categorytype but episode id
                embed = embeds.episodesinfoEmbed(data, categorytype, limit)
                await message.edit(embed=embed)
            
            if args[0] == "EPLS":
                data = nnlib.getEpisodesInfo(args[1])
                embed = embeds.episodesinfoEmbed(data, args[1], limit)
                await message.edit(embed=embed)

        if reaction in arrows_emojis[2:]:
            count = int(args[1])
            if reaction == arrows_emojis[3]:count -= 1
            if reaction == arrows_emojis[2]:count += 1
            if count < 0:count = 0
            
            if args[0] == "EPI":
                eid = epinfcontainer[int(text_channel.id)][int(message.id)][count][0]
                data = nnlib.getEpisode(eid)
                embed = embeds.episodeEmbed(data, count)
                if int(text_channel.id) not in epcontainer:
                    epcontainer[int(text_channel.id)] = {}
                epcontainer[int(text_channel.id)][int(message.id)] = data
                await message.edit(embed=embed)

        if reaction == "▶️":
            if args[0] == "PCI":
                pid = container[int(text_channel.id)][int(message.id)][int(args[1])][0]
                data = nnlib.getEpisodesInfo(pid)
                embed = embeds.episodesinfoEmbed(data, args[1], 5)
                if text_channel.id not in epinfcontainer:
                    epinfcontainer[text_channel.id] = {}
                epinfcontainer[text_channel.id][message.id] = data
                await message.edit(embed=embed)
                await message.remove_reaction("▶️", bot.user)
                await message.add_reaction(arrows_emojis[0])
                for i in range(len(data[:5])):
                    await message.add_reaction(num_emojis[i+1])
                await message.add_reaction(arrows_emojis[1])
            if args[0] == "EPI":
                try:
                    vc = await voice_channel.connect()
                except ClientException:
                    vc = discord.utils.get(bot.voice_clients, guild=guild)
                    vc.stop()
                URL = epcontainer[int(text_channel.id)][int(message.id)][0][7]
                if not vc.is_playing() and URL != None:
                    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

        if reaction in num_emojis:
            await message.remove_reaction(arrows_emojis[0], bot.user)
            for i in range(len(num_emojis)-1):
                await message.remove_reaction(num_emojis[i+1], bot.user)
            await message.remove_reaction(arrows_emojis[1], bot.user)
            indx = num_emojis.index(reaction)-1
            
            if args[0] == "PDLS":
                metadata = container[int(text_channel.id)][int(message.id)]
                pid = metadata[indx][0]
                data = nnlib.getPodcastInfo(pid)
                embed = embeds.podcastinfoEmbed(data, indx)
                await message.edit(embed=embed)
                await message.add_reaction("▶️")
                
            if args[0] == "EPLS":
                metadata = epinfcontainer[int(text_channel.id)][int(message.id)]
                eid = metadata[indx][0]
                data = nnlib.getEpisode(eid)
                embed = embeds.episodeEmbed(data, indx)
                if int(text_channel.id) not in epcontainer:
                    epcontainer[int(text_channel.id)] = {}
                epcontainer[int(text_channel.id)][int(message.id)] = data
                await message.edit(embed=embed)
                await message.add_reaction(arrows_emojis[3])
                await message.add_reaction("▶️")
                await message.add_reaction(arrows_emojis[2])
                

@bot.command(aliases=["play", "start", "podcast"])
async def listen(ctx, ptype=nnlib.podcastOpts.featured):
    channel_id = ctx.message.channel.id
    data = nnlib.getPodcastslist(ptype)
    embed = embeds.listenEmbed(data, ptype, 5)
    message = await ctx.send(embed=embed)
    container[channel_id] = {}
    container[channel_id][message.id] = data
    await message.add_reaction(arrows_emojis[0])
    for i in range(len(data[:5])):
        await message.add_reaction(num_emojis[i+1])
    await message.add_reaction(arrows_emojis[1])

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
