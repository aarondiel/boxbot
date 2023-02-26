import discord
from os import listdir, path
from random import choice
from asyncio import Future
from queue import LifoQueue

connections: dict[int, discord.VoiceClient] = {}
playing_queue: dict[discord.VoiceClient, LifoQueue] = {}

def get_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    return discord.Client(
        intents=intents,
        activity=discord.Game(name="Doki Doki Literature Club")
    )


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


async def play_many(voice: discord.VoiceClient, sources: list[discord.AudioSource]) -> None:
    global playing_queue

    if not voice in playing_queue:
        playing_queue[voice] = LifoQueue(maxsize=100)
        [ playing_queue[voice].put_nowait(source) for source in sources ]
    else:
        [ playing_queue[voice].put_nowait(source) for source in sources ]
        return

    while not playing_queue[voice].empty():
        source = playing_queue[voice].get_nowait()

        result = Future()
        voice.play(
            source,
            after=lambda err: result.set_result(err)
        )

        await result

    playing_queue.pop(voice)


async def play(voice: discord.VoiceClient, source: discord.AudioSource) -> None:
    await play_many(voice, [ source ])
