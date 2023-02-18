import discord
import utils
from youtube_dl import YoutubeDL

ytdl = YoutubeDL({
    "default_search": "auto",
    "format": "bestaudio/best",
    "geo_bypass": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "no_warnings": True,
    "quiet": True,
    "source_address": "0.0.0.0",
    "socket_timeout": 10
})

def get_urls(url: str) -> list[str]:
    queried = ytdl.extract_info(url, download=False, process=False)

    if queried == None:
        return []

    if "entries" not in queried:
        return [queried["formats"][0]["url"]]

    entries = (
        ytdl.extract_info(entry, download=False, process=False)
        for entry in queried["entries"]
    )

    return [
        entry["formats"][0]["url"]
        for entry in entries
        if entry != None
    ]


async def command(author: discord.User | discord.Member, url: str):
    if isinstance(author, discord.User):
        return

    voice = author.voice
    if voice == None:
        return

    channel = voice.channel
    if channel == None:
        return

    voice_connection = await utils.get_voice_connection(channel)

    urls = get_urls(url)
    for url in urls:
        source = discord.FFmpegOpusAudio(url, options="-vn")

        await utils.play(voice_connection, source)

    await voice_connection.disconnect()
