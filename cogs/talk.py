import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import utils

load_dotenv() # load all the variables from the env file
SERVER_ID = os.getenv('SERVER_ID')
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))
class talk(commands.Cog):

    def __init__(self, bot : commands.Bot) -> None:
        self.bot  = bot
        self.logger = bot.cog_loggers[self.__class__.__name__]
    
    @app_commands.command(
        name = "talk",
        description = "Makes the bot talk")
    @app_commands.describe(
        text = "text"
    )
    
    #@app_commands.checks.has_any_role(ADMIN_ROLE_ID) # Check if the author has the admin role. If not go to @talk.error
    async def talk(self, interaction : discord.Interaction, text : str) -> None:
        utils.set_debug_level(self.logger)
        if interaction.user.id == 397046303378505729 or await self.check_permission(interaction.user.roles,ADMIN_ROLE_ID):
            text = text.replace("\\n", "\n")
            await interaction.response.send_message(content=f"**Saying:**\n{text}", ephemeral=True)
            await interaction.channel.send(content=text)
            self.logger.info(f"{interaction.user.name} used the talk command and said: '{text}'")
        else:
            await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
            self.logger.warning(f"{interaction.user.name} tried to use `/talk`")
  
    async def check_permission(self, user_perms, needed_perm_id) -> bool: # Check if the user has a specific role
        for i in range(len(user_perms)):
            if user_perms[i].id == needed_perm_id:
                return True
        return False


async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        talk(bot),
        guilds = [discord.Object(id = SERVER_ID)]
    )