##required libraries
import asyncio
import time
import youtube_dl
import discord
from discord.ext import commands
from discord import voice_client
import shutil
import os
from discord.utils import get



##youtube_dl and ffmpeg settings
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#url importation for youtube

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


  
#main class for the bot
class dailyfriendschatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
        
    ### plays audio files
    @commands.command()
    async def "#yourfunctionhere"(self, ctx):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(r"#insert path here"))
        ctx.voice_client.play(source, after=lambda e: print('oynatıcı hatası: %s' % e) if e else None)
    
        await ctx.send('your text here')
        time.sleep(3.5)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def "#yourfunctionhere"(self, ctx):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(r"#insert path here"))
        ctx.voice_client.play(source, after=lambda e: print('oynatıcı hatası: %s' % e) if e else None)

        await ctx.send('your text here')
        time.sleep(3)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def "#yourfunctionhere"(self, ctx):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(r"#insert path here"))
        ctx.voice_client.play(source, after=lambda e: print('oynatıcı hatası: %s' % e) if e else None)

        await ctx.send('your text here')
        time.sleep(5)
        await ctx.voice_client.disconnect()
    
    #in order to play urlS from youtube

    @commands.command()
    async def yt(self, ctx, *, url):
        """yutup urlsi gir"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url,loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('oynatıcı hatası: %s' % e) if e else None)

        await ctx.send('çalıyor: {}'.format(player.title))
    
    #in order to adjust your volume
    @commands.command()
    async def ses(self, ctx, volume: int):

        if ctx.voice_client is None:
            return await ctx.send("you need to get in to the channel first")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("volume has changed to {}%".format(volume))
    #in order to make bot quit from the voice channel
    @commands.command()
    async def "#durdur,stop"(self, ctx):

        await ctx.voice_client.disconnect()
    
    #text functions
    @commands.command()
    async def "#yourfunction"(self,ctx):
     await ctx.send("#yourtext")
     await ctx.voice_client.disconnect()
     

    @commands.command()
    async def "#yourfunction"(self,ctx):
     await ctx.send("#yourtext")
     await ctx.voice_client.disconnect()
     
    "YOUR FUNCTIONS NAMES HERE,THEN .before_invoke"
    #@yarra.before_invoke 
    #@olr.before_invoke
    #@peh.before_invoke
    #@yt.before_invoke
    #@enockim.before_invoke
    #@annen.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("you need to be in a voice channel")
                raise commands.CommandError("where are you")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            ctx.author.voice.channel.disconnect()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."),
                   description=('for any questions: ulkerkadrican@gmail.com, AUTHOR KADRI CAN ULKER')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(dailyfriendschatbot(bot))
bot.run('YOUR BOT TOKEN HERE')
