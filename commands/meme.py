from mimetypes import guess_type
from asyncio import sleep
from typing import Optional
from os import path
import discord
import utils


offensive_memes = None
current_messages: dict[discord.Message, int] = {}


class MemeVote(discord.ui.View):
    ok_reactions: set[discord.User | discord.Member]
    offensive_reactions: set[discord.User | discord.Member]

    
    def __init__(self, timeout: Optional[float] = 30):
        super().__init__(timeout=timeout)

        self.ok_reactions = set()
        self.offensive_reactions = set()


    @discord.ui.button(emoji="🪝", label="ok")
    async def ok(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        if interaction.user in self.offensive_reactions:
            self.offensive_reactions.remove(interaction.user)

        self.ok_reactions.add(interaction.user)
        await interaction.response.defer()


    @discord.ui.button(emoji="😠", label="offensive")
    async def offensive(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        if interaction.user in self.ok_reactions:
            self.ok_reactions.remove(interaction.user)

        self.offensive_reactions.add(interaction.user)
        await interaction.response.defer()


def get_offensive_memes() -> list[str]:
    global offensive_memes

    if offensive_memes != None:
        return offensive_memes

    with open("/data/offensive_memes.txt", "r") as f:
        offensive_memes = f.readlines()
        return offensive_memes


def remove_file(filename: str) -> None:
    get_offensive_memes().append(filename)

    with open("/data/offensive_memes.txt", "a") as f:
        f.write(f"{filename}\n")


@discord.app_commands.command(name="meme", description="send a random meme")
async def command(interaction: discord.Interaction) -> None:
    file = utils.random_file(
        "/data/memes",
        banned=get_offensive_memes()
    )

    mime_type = guess_type(file)[0]
    embed_type = ""

    if mime_type == None:
        print(f"unknown file type: {file}")
        await interaction.response.send_message(content="an error occured")
        return
    elif mime_type.startswith("image"):
        embed_type = "image"
    elif mime_type.startswith("video"):
        embed_type = "video"
    else:
        print(f"unknown file type: {file}")
        await interaction.response.send_message(content="an error occured")
        return

    filename = path.basename(file).replace(" ", "_")
    embed = discord.Embed(color=discord.Color.brand_red(), type=embed_type)
    embed.set_image(url=f"attachment://{filename}")

    view = MemeVote()

    await interaction.response.send_message(
        file=discord.File(file, filename=filename),
        embed=embed,
        view=view
    )

    await sleep(30)

    ok = len(view.ok_reactions)
    offensive = len(view.offensive_reactions)

    if 3 * offensive >= 2 * (ok + offensive):
        remove_file(file)
        await interaction.response.edit_message(content="im sorry ")
