import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
import json
import logging
import utils

load_dotenv() # load all the variables from the env file
SERVER_ID =os.getenv('SERVER_ID')

from pathlib import Path
path_dir = Path(__file__).parent.parent.resolve()
path_json = path_dir / "data.JSON"

#logging
logger = logging.getLogger("invite")

formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s:%(name)-12s: %(message)s",
                              "%d-%m-%Y %H:%M:%S")
formatter.converter = time.gmtime

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class invite(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
   
   @app_commands.command(
      name = "invite",
      description = "Sends an invite link that you can share with people")
   
   async def invite(self, interaction : discord.Interaction) -> None:
      utils.set_debug_level(logger)
      await interaction.response.send_message(f"Send this link to people you would like to invite to this server: https://discord.com/invite/5zTdXs4yJu", ephemeral=True)
      logger.info(f"{interaction.user.name} used the `/invite` command")


async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      invite(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )