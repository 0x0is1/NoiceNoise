from discord.ext import commands, tasks
from embedder import embeds
from noicenoiselib import nnlib
import os

arrows_emojis = ['⬆️', '⬇️', '➡️', '⬅️']
num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

container = {}

bot=commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    print('bot is online.')

@bot.event
async def on_reaction_add(reaction, user):
    print('bot is online.')

@bot.command(aliases=["play", "start", "podcast"])
async def listen(ctx, ptype=nnlib.podcastOpts.popular):
    channel_id = ctx.message.channel.id
    data = nnlib.getPodcastslist(ptype)
    embed = embeds.listenEmbed(data, ptype, 5)
    message = await ctx.send(embed=embed)
    embed[channel_id] = {}
    embed[channel_id][ctx.message.id] = data
    await message.add_reaction(arrows_emojis[0])
    for i in range(len(data[:5])):
        await message.add_reaction(num_emojis[i+1])
    await message.add_reaction(arrows_emojis[1])

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
