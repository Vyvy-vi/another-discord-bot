from asyncio import sleep
from datetime import datetime
from glob import glob

import discord
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord import Embed
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import (CommandNotFound,
                                  BadArgument,
                                  MissingRequiredArgument,
                                  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or

from ..db import db

OWNER_IDS = [558192816308617227]
COGS = [path.split("/")[-1][:-3] for path in glob("./src/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", str(message.guild.id))
    return when_mentioned_or(prefix)(bot, message)


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
        self.ready = False
        self.cogs_ready = Bot_Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f'src.cogs.{cog}')
        self.load_extension('jishaku')
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

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send('I\'m not ready to recieve commands. Please wait a few seconds...')

    async def on_connect(self):
        print("  Bot connected....")

    async def on_disconnect(self):
        print("  Bot disconnected...")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        await self.stdout.send(f"```An Error Occured in {self.guild} -\n{err}```")
        raise err

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send('Required Arguments are missing...')

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"The command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")
        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send message...")
            elif isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permissions to do that...")
            else:
                return exc.original

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

            await self.stdout.send("[INFO]: Bot is Online")
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
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
