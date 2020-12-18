from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions

from ..db import db


class Conf(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 7:
            await ctx.send('Prefix can-not be of more than 7 characters...')

        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, str(ctx.guild.id))
            await ctx.send(f"The Prefix has been sent to {new}")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You need Manage Server permissions to do that")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("conf")
        await self.bot.stdout.send('[INFO: `Config` cog loaded...]')


def setup(bot):
    bot.add_cog(Conf(bot))
