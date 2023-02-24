import discord
from os import listdir, path
from random import choice
from asyncio import Future

connections: dict[int, discord.VoiceClient] = {}

def get_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    return discord.Client(
        intents=intents,
        activity=discord.Game(name="Doki Doki Literature Club")
    )


def get_client_id(client: discord.Client) -> int:
    if client.user == None:
        raise Exception("client is not connected")

    return client.user.id


async def get_voice_connection(
        channel: discord.channel.VocalGuildChannel
    ) -> discord.VoiceClient:
    global connections

    if channel.guild.id in connections:
        return connections[channel.guild.id]

    return await channel.connect()


def random_file(folder: str, banned: list[str] | None = None) -> str:
    while True:
        random_file = choice(listdir(folder))

        if banned == None or random_file not in banned:
            break

    file_path = path.join(folder, random_file)

    return file_path


async def play(voice: discord.VoiceClient, source: discord.AudioSource):
    result = Future()
    voice.play(
        source,
        after=lambda err: result.set_result(err)
    )

    return await result
