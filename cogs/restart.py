import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import utils

load_dotenv() # load all the variables from the env file
SERVER_ID = os.getenv('SERVER_ID')
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))

from pathlib import Path
path_dir = Path(__file__).parent.parent.resolve()
path_json = path_dir / "data.JSON"

class restart(commands.Cog):

    def __init__(self, bot : commands.Bot) -> None:
        self.bot  = bot
        self.logger = bot.cog_loggers[self.__class__.__name__]
    
    @app_commands.command(
        name = "restart",
        description = "Restarts the bot")
    
    @app_commands.checks.has_any_role(ADMIN_ROLE_ID)
    async def restart(self, interaction : discord.Interaction) -> None:
        utils.set_debug_level(self.logger)
        # Only restarts if in cloud, otherwise it just quits
        await interaction.response.send_message("Restarting...", ephemeral=True)
        self.logger.info(f"{interaction.user.name} restarted the bot")
        quit(0)
    
    @restart.error
    async def permission(self, interaction : discord.Interaction, error : app_commands.AppCommandError) -> None:
        
        if isinstance(error, app_commands.MissingAnyRole):
            utils.set_debug_level(self.logger)
            if interaction.user.id == 397046303378505729:
                await interaction.response.send_message("Restarting...", ephemeral=True)
                self.logger.info(f"{interaction.user.name} restarted the bot")
                quit(0)
            else:
                await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
                self.logger.warning(f"{interaction.user.name} tried to use `/restart`")

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        restart(bot),
        guilds = [discord.Object(id = SERVER_ID)]
    )