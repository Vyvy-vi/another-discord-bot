import discord
from datetime import datetime
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed
from discord.ext.commands import CommandNotFound
PREFIX = '.'
OWNER_IDS = [558192816308617227]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def run(self, version):
        self.VERSION = version

        with open("./src/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print('Running Bot...')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot connected....")

    async def on_disconnect(self):
        print("Bot disconnected...")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        channel = self.get_channel(779383905798193193)
        await channel.send(f"```An Error Occured-\n{err}```")
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
            self.ready = True
            self.guild = self.get_guild(778704923553693746)
            print('Bot Ready...')

            channel = self.get_channel(779383905798193193)
            await channel.send("Now Online")

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

            await channel.send(embed=embed)
        else:
            print('Bot reconnected...')

    async def on_message(self, message):
        pass


bot = Bot()
