from os import path
from enum import Enum
from io import BytesIO
from subprocess import PIPE, Popen
import discord

class JavaFormatterFile(Enum):
    ReplaceUtf8 = "ReplaceUtf8.jar"
    ReplaceTabs = "ReplaceTabs.jar"
    MakeCursed = "MakeCursed.jar"

def strip_backticks(input: str) -> str:
    if not input.startswith("```"):
        return input

    return "\n".join(input.splitlines()[1:-1])


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


async def send_message_or_file(
    channel: discord.abc.Messageable,
    message: str,
) -> None:
    async with channel.typing():
        if len(message) <= 2000:
            await channel.send(f"```java\n{message}\n```")
            return

        file = discord.File(BytesIO(message.encode()), filename="cursed.java")
        await channel.send(file=file)


async def replace_tabs(channel: discord.abc.Messageable, message: str) -> None:
    message = strip_backticks(message)
    message = java_formatter(message, JavaFormatterFile.ReplaceTabs)

    await send_message_or_file(
        channel,
        message
    )

async def escape(channel: discord.abc.Messageable, message: str) -> None:
    # message = strip_backticks(message)
    message = java_formatter(message, JavaFormatterFile.ReplaceUtf8)

    await send_message_or_file(
        channel,
        message
    )

async def make_cursed(channel: discord.abc.Messageable, message: str) -> None:
    message = strip_backticks(message)
    message = java_formatter(message, JavaFormatterFile.ReplaceTabs)
    message = java_formatter(message, JavaFormatterFile.ReplaceUtf8)
    message = java_formatter(message, JavaFormatterFile.MakeCursed)

    await send_message_or_file(
        channel,
        message
    )
