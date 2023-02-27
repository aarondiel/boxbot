import discord

@discord.app_commands.command(description="test if the bot is online")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(content="pong")
