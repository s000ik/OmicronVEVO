import discord
from discord.ext import commands
import os
import youtube_dl
import requests
intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents)

@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))


@client.command()
async def join(ctx):
  if ctx.author.voice is None:
    await ctx.send("Please join a voice chat first")
  voice_channel = ctx.author.voice.channel
  if ctx.voice_client is None:
    await voice_channel.connect()
  else:
    await ctx.voice_client.move_to(voice_channel)

@client.command()
async def leave(ctx):
  await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, url):
  ctx.voice_client.stop()
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  YDL_OPTIONS = {'format':"bestaudio"}
  vc = ctx.voice_client

  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    vc.play(source)



@client.command()
async def pause(ctx):
  await ctx.voice_client.pause()
  await ctx.send("Playback Paused")

@client.command()
async def resume(ctx):
  await ctx.voice_client.resume()
  await ctx.send("Playback Resumed")

@client.command()
async def loop(ctx , url):
  await ctx.voice_client.loop()
  await ctx.send("Now Looping")

client.run(os.getenv("token"))