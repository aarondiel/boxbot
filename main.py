import discord
from os import environ
from typing import Callable

from commands.meme import command as meme, \
    handle_reaction_add as meme_reaction_add, \
    handle_reaction_remove as meme_reaction_remove
from commands.elotrix import command as elotrix
from commands.play import command as play
from commands.format import escape, replace_tabs, make_cursed
import utils

client = utils.get_client()
command_prefix = environ["COMMAND_PREFIX"]
command_tree = discord.app_commands.CommandTree(client)

reaction_add_commands: list[Callable[[discord.Reaction, discord.Member | discord.User], bool]] = [
    meme_reaction_add
]

reaction_remove_commands: list[Callable[[discord.Reaction, discord.Member | discord.User], bool]] = [
    meme_reaction_remove
]


@command_tree.command(name="ping", description="test if the bot is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")


@client.event
async def on_ready() -> None:
    await command_tree.sync()


@client.event
async def on_reaction_add(
    reaction: discord.Reaction,
    user: discord.Member | discord.User
) -> None:
    for fn in reaction_add_commands:
        if fn(reaction, user):
            return


async def on_reaction_remove(
    reaction: discord.Reaction,
    user: discord.Member | discord.User
) -> None:
    for fn in reaction_remove_commands:
        if fn(reaction, user):
            return


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if message.content == "/ping":
        await message.channel.send("pong")
        return

    if not message.content.startswith(command_prefix):
        return

    content = message.content[len(command_prefix):]
    split = content.split(" ", 1)
    command = split[0]

    if command == "meme":
        await meme(message.channel)
    elif command == "elotrix":
        await elotrix(message.author)
    elif command == "play":
        if not len(split) > 1:
            await message.channel.send("invlid number of arguments")
            return

        await play(message.author, split[1])
    elif command == "escape":
        await escape(message.channel, split[1])
    elif command == "replace_tabs":
        await replace_tabs(message.channel, split[1])
    elif command == "cursed":
        await make_cursed(message.channel, split[1])


if __name__ == "__main__":
    client.run(environ["TOKEN"])
