from discord.ext.commands import Cog
from discord.ext.commands import command
from typing import Optional


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @command(name="Help")
    async def show_help(self, ctx, cmd: Optional[str]):
        if cmd is None:
            pass
        else:
            pass

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
