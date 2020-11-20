from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

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

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(778704923553693746)
            print('Bot Ready...')

            channel = self.get_channel(779383905798193193)
            await channel.send("Now Online")
        else:
            print('Bot reconnected...')

    async def on_message(self, message):
        pass


bot = Bot()
