import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from utils import get_environment_variable

TOKEN = get_environment_variable("ANOTHER_BOT_TOKEN")

PREFIX = '.'

intents = discord.Intents(messages= True, guilds= True)
bot = commands.Bot(command_prefix = PREFIX, intents=intents)

# cog paths
ls_cog= ['cogs.events',
         'cogs.owner',
         'cogs.commands']
# status cyclic list
STATUS = cycle([
    "help",
    "with bots",
    "xyz",
    "with xyz"])


@bot.event
async def on_ready():
    """
    On ready event listener
    http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready
    """
    print(f'\n\nSuccessfully Logged in as: {bot.user}\n')
    # starts status_changer task
    change_status.start()


@tasks.loop(seconds=600)
async def change_status():
    """
    Task for changing the activity status.
    loops through the cycle of the STATUS list and sets that as bot presence
    """
    await bot.change_presence(activity=discord.Game(next(STATUS)))
    # NOTE- There are other methods, that can be utilised instead of just 'playing'

# Here we load our extensions(cogs) listed above in [ls_cog].
if __name__ == '__main__':
    for extension in ls_cog:
        bot.load_extension(extension)


# error_handling
@bot.event
async def on_command_error(ctx, error):
    # TODO- Error Handling
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used..... ")
    else:
        await ctx.send(error)


# runs the bot
bot.run(TOKEN)
