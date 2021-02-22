from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")
        await self.bot.stdout.send('[INFO: `Log` cog loaded...]')

    @Cog.listener()
    async def on_member_update(self, before, after):
        pass

    @Cog.listener()
    async def on_message_edit(self, before, after):
        pass

    @Cog.listener()
    async def on_message_delete(self, before, after):
        pass


def setup(bot):
    bot.add_cog(Log(bot))