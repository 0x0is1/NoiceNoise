import discord

def listenEmbed(data, ptype, limit):
    embed = discord.Embed(title="Select podcast to listen:", color=0x552E12)
    embed.set_author(name="*NoiceNoise: Listen to your heart*")
    for i in data[-limit:][:5]:embed.add_field(name=i[2], value=i[1], inline=False)
    embed.set_footer(text=f"PDLS-{ptype}-{limit}")
    return embed

def podcastinfoEmbed(data, podcastindex):
    embed = discord.Embed(title="Podcast details", color=0x552E12)
    embed.set_author(name="*NoiceNoise: Listen to your heart*")
    embed.add_field(name=data[1], value=data[2], inline=False)
    socialmedValue = ""
    for i in data[4:]:socialmedValue += f"[{i[0]}]({i[1]})|"
    if socialmedValue != "":
        embed.add_field(name="Follow Us:", value=socialmedValue)
    embed.set_thumbnail(url=data[3])
    embed.set_footer(text=f"PCI-{podcastindex}")
    return embed

def episodesinfoEmbed(data, podcastindex, limit):
    embed = discord.Embed(title="Select episode to listen:", color=0x552E12)
    for i in data[-limit:][:5]:embed.add_field(name=i[2], value=f"{i[4]}\n*{i[5]}*  **{i[3]}**", inline=False)
    embed.set_author(name="Listen to your heart")
    embed.set_footer(text=f"EPLS-{podcastindex}-{limit}")
    return embed

def episodeEmbed(data, episodeindex):
    embed = discord.Embed(title="You are listening to", color=0x552E12)
    data=data[0]
    embed.add_field(name=data[2], value=f"{data[4]}\n*{data[5]}*  **{data[3]}**", inline=False)
    embed.set_thumbnail(url=data[6])
    embed.set_author(name="Listen to your heart")
    embed.set_footer(text=f"EPI-{episodeindex}")
    return embed

def genreEmbed(data, limit, category):
    embed = discord.Embed(title="Select genre:", color=0x552E12)
    embed.set_author(name="*NoiceNoise: Listen to your heart*")
    Value = ""
    for i in data[-limit:][:5]:Value += f"{i[0]}\n"
    embed.add_field(name="Categories", value=Value, inline=False)
    embed.set_footer(text=f"GNLS-{category}-{limit}")
    return embed

def genreinfoEmbed(data, genreindex, limit):
    embed = discord.Embed(title="Select episode to listen:", color=0x552E12)
    for i in data[1][-limit:][:5]:embed.add_field(name=i[1], value=f"{i[2]}\n*{i[4]}*", inline=False)
    embed.set_author(name=data[0])
    embed.set_footer(text=f"GNI-{genreindex}-{limit}")
    return embed
