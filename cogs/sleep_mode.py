import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import os
import json

load_dotenv() # load the variables needed from the .env file
SERVER_ID =os.getenv('SERVER_ID')
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))

from pathlib import Path
path_dir = Path(__file__).parent.parent.resolve()
path_json = path_dir / "data.JSON"

class sleep_mode(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
   
   @app_commands.command(
      name = "sleep_mode",
      description = "Toggles the mode to sleep_mode or back to normal mode")

   @app_commands.checks.has_any_role(ADMIN_ROLE_ID) # Check if the author has the admin role. If not go to @toggle_server.error
   async def debug(self, interaction : discord.Interaction) -> None:
      mode = await self.update_json()
      msg = f"Mode is set to to {mode}"
      await interaction.response.send_message(msg, ephemeral=True)
      print(f"[{await self.current_time()}] {interaction.user.name} changed mode to {mode}")
      
   @debug.error
   async def permission(self, interaction : discord.Interaction, error : app_commands.AppCommandError) -> None:
      if isinstance(error, app_commands.MissingAnyRole): # Check if the error is because of an missing role
         if interaction.user.id == 397046303378505729:# Check if the author is me (GuuscoNL)
            mode = await self.update_json()
            msg = f"Mode is set to {mode}"
            await interaction.response.send_message(msg, ephemeral=True)
            print(f"[{await self.current_time()}] {interaction.user.name} changed mode to {mode}")
         else:
            await interaction.response.send_message("You do not have the permission!", ephemeral=True)
            print(f"[{await self.current_time()}] {interaction.user.name} tried to use the `/sleep_mode` command") # Log it
   
   async def update_json(self):
      with path_json.open(mode="r+") as file:
         json_data = json.loads(file.read())
         if json_data["mode"] == 0:
            json_data["mode"] = 1
         else:
            json_data["mode"] = 0
         file.seek(0)
         temp = json.dumps(json_data, indent=3)
         file.truncate(0)
         file.write(temp)
      return json_data["mode"]
   
   async def current_time(self): # Get current time
      now = datetime.datetime.utcnow()
      return now.strftime("%d/%m/%Y %H:%M:%S UTC")

async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      sleep_mode(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )