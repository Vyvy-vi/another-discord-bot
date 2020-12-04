from aiohttp import request

from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown

from typing import Optional
from discord import Member, Embed, BucketType
from discord.ext.commands import BadArgument
from random import randint, choice


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hi','Hello','Hey','Heya'))} {ctx.author.mention}!")

    @command(name='dice', aliases=['roll'])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = list(map(int, die_string.split('d')))
        if dice <= 30:
            rolls = [randint(1, value) for _ in range(dice)]
            await ctx.send(" + ".join(list(map(str, rolls))) + f'= {sum(rolls)}')
        else:
            await ctx.send("ERROR- Can't roll that many die. Try again later")

    @command(name='slap', aliases=['hit'])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f'{ctx.author.display_name} slapped {member.mention} for {reason}')

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc.original, BadArgument):
            await ctx.send("Can't find that member...")

    @command(name='echo', aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        await self.bot.stdout.send('[INFO: `Fun` cog loaded...]')

    @command(name="fact")
    async def animal_facts(self, ctx, animal: str):
        if (animal := animal.lower()) in ('dog', 'cat', 'panda', 'fox', 'bird'):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal=='bird' else animal}"

            async with request("GET", image_url, headers=[]) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data['link']
                else:
                    image_link = None

            async with request("GET", fact_url, headers=[]) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f'{animal.title()} fact',
                                  description=data['fact'],
                                  colour=ctx.author.color)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'API returned a {response.status} status.')
        else:
            await ctx.send(f'No facts are available for {animal}')


def setup(bot):
    bot.add_cog(Fun(bot))
