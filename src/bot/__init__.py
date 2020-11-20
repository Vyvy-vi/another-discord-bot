from asyncio import sleep
from datetime import datetime
from glob import glob

import discord
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord import Embed
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = '.'
OWNER_IDS = [558192816308617227]
COGS = [path.split("/")[-1][:-3] for path in glob("./src/cogs/*.py")]


class Bot_Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'[INFO]: {cog} Cog Loaded')

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Bot_Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f'src.cogs.{cog}')
        print('  Setup Complete')

    def run(self, version):
        self.VERSION = version

        print('Running setup...')
        self.setup()

        with open("./src/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print('Running Bot...')
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):
        channel = self.get_channel(779383905798193193)
        await channel.send('----timed-message----')

    async def on_connect(self):
        print("  Bot connected....")

    async def on_disconnect(self):
        print("  Bot disconnected...")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        await self.stdout.send(f"```An Error Occured in {self.guild} -\n{err}```")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send('CommandNotFound')

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:

            self.guild = self.get_guild(778704923553693746)
            self.stdout = self.get_channel(779383905798193193)
            self.scheduler.add_job(self.print_message, CronTrigger(minute=0, second=0))
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Bot is Online")
            embed = Embed(title='Now Online...!',
                          description='Bot is now online',
                          colour=discord.Colour.red(),
                          timestamp=datetime.utcnow())
            fields = [("Version", f'v{self.VERSION}', True),
                      ("GUILD", self.guild.name, True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name='another-bot', icon_url=self.guild.icon_url)
            embed.set_footer(text='time to do some epic shit')
            await self.stdout.send(embed=embed)

            self.ready = True
            print('Bot Ready...')
        else:
            print('Bot reconnected...')

    async def on_message(self, message):
        pass


bot = Bot()
