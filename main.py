import discord
from os import environ

import utils
from commands.ping import ping
from commands.meme import meme
from commands.format import format
from commands.play import play
from commands.elotrix import elotrix

client = utils.get_client()
command_tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready() -> None:
    await command_tree.sync()


command_tree.add_command(ping)
command_tree.add_command(meme)
command_tree.add_command(format)
command_tree.add_command(play)
command_tree.add_command(elotrix)


if __name__ == "__main__":
    client.run(environ["TOKEN"])
