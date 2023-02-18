from asyncio import sleep
import discord
import utils

offensive_memes = None
current_messages: dict[discord.Message, int] = {}


def increment_count(reaction: discord.Reaction, invert: bool) -> bool:
    count = current_messages.get(reaction.message)

    if count == None:
        return False

    increment = 0
    if reaction.emoji == "🪝":
        increment = -2
    elif reaction.emoji == "😠":
        increment = 1

    if invert:
        increment = -increment

    current_messages[reaction.message] = count + increment

    return True


def handle_reaction_add(
    reaction: discord.Reaction,
    user: discord.Member | discord.User
) -> bool:
    return increment_count(reaction, False)


def handle_reaction_remove(
    reaction: discord.Reaction,
    user: discord.Member | discord.User
) -> bool:
    return increment_count(reaction, True)


def get_offensive_memes() -> list[str]:
    global offensive_memes

    if offensive_memes != None:
        return offensive_memes

    with open("offensive_memes.txt", "r") as f:
        offensive_memes = f.readlines()
        return offensive_memes


def remove_file(filename: str) -> None:
    get_offensive_memes().append(filename)

    with open("offensive_memes.txt", "a") as f:
        f.write(f"\n{filename}")


async def command(channel: discord.abc.Messageable) -> None:
    async with channel.typing():
        file_path = utils.random_file(
            "/data/memes",
            banned=get_offensive_memes()
        )

        file = discord.File(file_path)

        message = await channel.send(file=file)

    try:
        current_messages[message] = 0
        await message.add_reaction("🪝")
        await message.add_reaction("😠")

        await sleep(30)

        count = current_messages.get(message)
        if count != None and count >= 0:
            remove_file(message.attachments[0].filename)
            await message.delete()
        else:
            await message.clear_reactions()
    except discord.Forbidden:
        pass
    finally:
        current_messages.pop(message)
