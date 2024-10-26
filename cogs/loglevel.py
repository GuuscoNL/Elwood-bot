import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import utils

load_dotenv() # load the variables needed from the .env file
SERVER_ID =os.getenv('SERVER_ID')
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))

from pathlib import Path
path_dir = Path(__file__).parent.parent.resolve()
path_json = path_dir / "data.JSON"

class loglevel(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
      self.logger = bot.cog_loggers[self.__class__.__name__]
   
   @app_commands.command(
      name = "loglevel",
      description = "Toggles the loglevel variable")
   @app_commands.describe(
      loglevel = "Set loglevel"
    )
   @app_commands.choices(loglevel=[
      Choice(name="DEBUG", value="DEBUG"),
      Choice(name="INFO", value="INFO"),
      Choice(name="WARNING", value="WARNING"),
      Choice(name="ERROR", value="ERROR"),
      Choice(name="CRITICAL", value="CRITICAL")
   ])
   

   async def loglevel(self, interaction : discord.Interaction, loglevel : str) -> None:
      utils.set_debug_level(self.logger)
      loglevel = loglevel.upper()
      if interaction.user.id == 397046303378505729 or await self.check_permission(interaction.user.roles,ADMIN_ROLE_ID):
         if await self.update_json(loglevel):
            msg = f"The `loglevel` variable is set to {loglevel}"
            self.logger.info(f"{interaction.user.name} changed loglevel to `{loglevel}`")
         else:
            msg = f"`{loglevel}` is not a valid option, please choose out: `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`"
            
         await interaction.response.send_message(msg, ephemeral=True)
      else:
         await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
         self.logger.warning(f"{interaction.user.name} tried to use `/loglevel`")
   
   async def update_json(self, loglevel : str):
      with path_json.open(mode="r+") as file:
         json_data = json.loads(file.read())
         if loglevel == "DEBUG" or loglevel == "INFO" or loglevel == "WARNING" or loglevel == "ERROR" or loglevel == "CRITICAL":
            json_data["loglevel"] = loglevel
         else:
            return False
        
         file.seek(0)
         temp = json.dumps(json_data, indent=3)
         file.truncate(0)
         file.write(temp)
         return True
         
         
   async def check_permission(self, user_perms, needed_perm_id) -> bool: # Check if the user has a specific role
      for i in range(len(user_perms)):
         if user_perms[i].id == needed_perm_id:
               return True
      return False

async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      loglevel(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )