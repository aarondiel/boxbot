import discord
from os import environ

import utils
from commands.meme import command as meme
from commands.format import group as format

from commands.play import command as play
from commands.elotrix import command as elotrix

client = utils.get_client()
command_prefix = environ["COMMAND_PREFIX"]
command_tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready() -> None:
    await command_tree.sync()


@command_tree.command(name="ping", description="test if the bot is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")


command_tree.add_command(meme)
command_tree.add_command(format)
command_tree.add_command(play)

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if not message.content.startswith(command_prefix):
        return

    content = message.content[len(command_prefix):]
    split = content.split(" ", 1)
    command = split[0]

    if command == "elotrix":
        await elotrix(message.author)


if __name__ == "__main__":
    client.run(environ["TOKEN"])
