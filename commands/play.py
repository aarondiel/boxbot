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

@discord.app_commands.command(description="play the audio from a given url")
@discord.app_commands.describe(url="url to source")
async def command(interaction: discord.Interaction, url: str) -> None:
    if isinstance(interaction.user, discord.User):
        await interaction.response.send_message(content="cannot play from this context")
        return

    voice = interaction.user.voice
    if voice == None or voice.channel == None:
        await interaction.response.send_message(content="you are not connected to any voice channel")
        return

    voice_connection = await utils.get_voice_connection(voice.channel)
    
    for url in get_urls(url):
        source = discord.FFmpegOpusAudio(url, options="-vn")
        await utils.play(voice_connection, source)

    await voice_connection.disconnect()
