from discord import Forbidden
from discord.ext.commands import Cog

from ..db import db


class Greetings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("greet")
        await self.bot.stdout.send('[INFO: `Greetings` cog loaded...]')

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserId) VALUES (?)", str(member.id))
        await self.bot.greetchannel.send(f"Welcome to **{member.guild.name}**, {member.mention}!")

        try:
            await member.send("Welcome to **{member.guild.name}**. Enjoy, your Stay!")
        except Forbidden:
            pass

        # await member.add_roles(member.guild.get_role(id), member.guild.get_role(id))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserId = ?", member.id)
        await self.bot.welcome_channel.send(f"{member.display_name} has left {member.guild.name}")


def setup(bot):
    bot.add_cog(Greetings(bot))
