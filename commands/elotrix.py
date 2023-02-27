import discord
import utils

@discord.app_commands.command(description="scream at me")
async def elotrix(interaction: discord.Interaction):
    if isinstance(interaction.user, discord.User):
        await interaction.response.send_message(content="cannot play from this context")
        return

    voice = interaction.user.voice
    if voice == None or voice.channel == None:
        await interaction.response.send_message(content="you are not connect to any voice channel")
        return

    voice_connection = await utils.get_voice_connection(voice.channel)

    file_path = utils.random_file("/data/elotrix")
    source = discord.FFmpegOpusAudio(file_path)

    await utils.play(voice_connection, source)

    await voice_connection.disconnect()
