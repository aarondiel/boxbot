import discord
from os import environ

from commands.meme import command as meme
from commands.elotrix import command as elotrix
from commands.play import command as play
from commands.format import escape, replace_tabs, make_cursed
import utils

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

    if command == "elotrix":
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
