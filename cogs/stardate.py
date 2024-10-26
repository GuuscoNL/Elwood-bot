import discord
import datetime
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import utils

load_dotenv() # load all the variables from the env file
SERVER_ID = os.getenv('SERVER_ID')

class stardate(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
      self.logger = bot.cog_loggers[self.__class__.__name__]
   
   @app_commands.command(
      name = "stardate",
      description = "Get the current date converted to a stardate (year 2382)")
   
   async def stardate(self, interaction : discord.Interaction) -> None:
      START_YEAR_REAL = 2022
      START_YEAR_RP   = 2382

      # Stardate Configuration.
      STARDATE_STANDARD_YEAR  = 2323
      STARDATE_START_YEAR     = 0
      MONTHTABLE = [
         0,
         31,
         59,
         90,
         120,
         151,
         181,
         212,
         243,
         273,
         304,
         334,
      ]

      dateTable = datetime.datetime.utcnow()
      # Time Offset
      y = dateTable.year + START_YEAR_RP - START_YEAR_REAL
      # Check if current year is a leap year
      n = 0
      if dateTable.year % 400 == 0 or (dateTable.year % 4 == 0 and dateTable.year % 100 != 0):
         n = 366
      else:
         n = 365
      monthOffset = MONTHTABLE[dateTable.month - 1]
      stardate = STARDATE_START_YEAR + (1000 * (y - STARDATE_STANDARD_YEAR)) + ((1000 / n) * (
         monthOffset
         + (dateTable.day - 1)
         + (dateTable.hour / 24)
         + (dateTable.minute / (24 * 60)
         + (dateTable.second / (24 * 3600)))
      ))
      stardate = format(stardate, ".3f")
      utils.set_debug_level(self.logger)
      await interaction.response.send_message(f"Current stardate is {stardate}\nTo calculate a custom stardate use this website: https://guusconl.github.io/TBN.github.io/", ephemeral=True, suppress_embeds=True)
      self.logger.info(f"{interaction.user.name} used the `/stardate` command")


async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      stardate(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )