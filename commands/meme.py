from asyncio import sleep
import discord
import utils

offensive_memes = None

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

    await message.add_reaction(":hook:")
    await message.add_reaction(":angry:")
    await sleep(30)

    hook_reaction = message.reactions[0]
    angry_reaction = message.reactions[1]

    total_reactions = (angry_reaction.count + hook_reaction.count)

    if (total_reactions != 0) and (angry_reaction.count / total_reactions > 2 / 3):
        remove_file(message.attachments[0].filename)

    await hook_reaction.clear()
    await angry_reaction.clear()
