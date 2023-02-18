import discord
import utils

async def command(author: discord.User | discord.Member):
    if isinstance(author, discord.User):
        return

    voice = author.voice
    if voice == None:
        return

    channel = voice.channel
    if channel == None:
        return

    voice_connection = await utils.get_voice_connection(channel)

    file_path = utils.random_file("/data/elotrix")
    source = discord.FFmpegOpusAudio(file_path)

    await utils.play(voice_connection, source)

    await voice_connection.disconnect()
