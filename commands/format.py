import discord
from os import path
from enum import Enum
from io import BytesIO
from asyncio import gather
from typing import Optional
from subprocess import PIPE, Popen

group = discord.app_commands.Group(
    name="format",
    description="code formatting tools"
)

class JavaFormatterFile(Enum):
    ReplaceUtf8 = "ReplaceUtf8.jar"
    ReplaceTabs = "ReplaceTabs.jar"
    MakeCursed = "MakeCursed.jar"


def java_formatter(input: str, file: JavaFormatterFile) -> str:
    jar_file = path.join(
        path.dirname(__file__),
        f"../JavaFormatter/bin/{file.value}"
    )

    output, _ = Popen(
        ["java", "-jar", jar_file],
        text=True,
        stdin=PIPE,
        stdout=PIPE
    ).communicate(input=input)

    return output.removesuffix("\n")


def format_utf8(input: tuple[str, str]) -> tuple[str, str]:
    return (java_formatter(input[0], JavaFormatterFile.ReplaceUtf8), input[1])


def format_tabs(input: tuple[str, str]) -> tuple[str, str]:
    return (java_formatter(input[0], JavaFormatterFile.ReplaceTabs), input[1])


def format_cursed(input: tuple[str, str]) -> tuple[str, str]:
    return (java_formatter(input[0], JavaFormatterFile.MakeCursed), input[1])


def strip_backticks(input: str) -> str:
    if not input.startswith("```"):
        return input

    return "\n".join(input.splitlines()[1:-1])


async def read_attachment(file: discord.Attachment) -> tuple[str, str]:
    file_content = await file.read()
    return (file_content.decode(), file.filename)


async def get_content(
    interaction: discord.Interaction,
    message: str
) -> list[tuple[str, str]]:
    content = []

    if message != "":
        content.append((strip_backticks(message), "message"))

    if interaction.message == None:
        return content
        
    content.extend(await gather(*(
        read_attachment(file)
        for file in interaction.message.attachments
    ), return_exceptions=False))

    return content


async def send_message_or_file(
    interaction: discord.Interaction,
    message: str,
    filename: Optional[str] = None
) -> None:
    if len(message) <= 2000:
        await interaction.response.send_message(
            content=f"```\n{message}\n```"
        )

        return

    file = discord.File(BytesIO(message.encode()), filename=filename)
    await interaction.response.send_message(file=file)


@group.command(description="escape utf-8 characters")
@discord.app_commands.describe(message="the code to format")
async def utf8(interaction: discord.Interaction, message: str) -> None:
    content = await get_content(interaction, message)
    if len(content) == 0:
        return

    content = map(format_utf8, content)
    await gather(*(
        send_message_or_file(interaction, file[0], file[1])
        for file in content
    ))


@group.command(description="replace tabs with spaces")
@discord.app_commands.describe(message="the code to format")
async def tabs(interaction: discord.Interaction, message: str) -> None:
    content = await get_content(interaction, message)
    if len(content) == 0:
        return

    content = map(format_tabs, content)
    await gather(*(
        send_message_or_file(interaction, file[0], file[1])
        for file in content
    ))


@group.command(description="make code cursed")
@discord.app_commands.describe(message="the code to format")
async def cursed(interaction: discord.Interaction, message: str) -> None:
    content = await get_content(interaction, message)
    if len(content) == 0:
        return

    content = map(format_tabs, content)
    content = map(format_cursed, content)
    await gather(*(
        send_message_or_file(interaction, file[0], file[1])
        for file in content
    ))
