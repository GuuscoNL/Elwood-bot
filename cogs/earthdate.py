import discord
import datetime
import time
from dateutil.relativedelta import relativedelta
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import utils

load_dotenv() # load all the variables from the env file
SERVER_ID = os.getenv('SERVER_ID')

class earthdate(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
      self.logger = bot.cog_loggers[self.__class__.__name__]
   
   @app_commands.command(
      name = "earthdate",
      description = "Convert a stardate to a normal date")
   @app_commands.describe(
        stardate = "earthdate"
    )
   async def stardate(self, interaction : discord.Interaction, stardate : str) -> None:
      utils.set_debug_level(self.logger)
      try:
         stardate = float(stardate)
         date = await stardate_to_date(stardate)
         unix_time = time.mktime(date.timetuple())
         await interaction.response.send_message(f"The date on that stardate is <t:{int(unix_time)}:D>\nTo calculate a custom stardate use this website: https://guusconl.github.io/TBN.github.io/", ephemeral=True, suppress_embeds=True)
         self.logger.info(f"{interaction.user.name} used the `/earthdate` command")
      except ValueError:
         await interaction.response.send_message(f"Please put a stardate as input, like: `59947.891`", ephemeral=True, suppress_embeds=True)
         self.logger.info(f"{interaction.user.name} Tried to use the `/earthdate` command")

# Algorithm taken from https://www.hillschmidt.de/gbr/sternenzeit.htm
async def stardate_to_date(stardate) -> datetime:
   StarTime = stardate
   
   earthdate = (StarTime / 1000) + 2323
   earthdates = str(earthdate) + ".0"
   vector = earthdates.split(".")
   year = int(vector[0])
   frag_year = float("0." + vector[1])
   if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
       xday = 366
   else:
       xday = 365
   if (frag_year == 0):
       return datetime.datetime(year=year, month=1, day=1, hour=0, minute=0, second=0)
   else:
      days = int((frag_year * xday) % xday)
      hour = int((frag_year * 24 * xday) % 24)
      min = int((frag_year * 1440 * xday) % 60)
      sec = int((frag_year * 86400 * xday) % 60)
      date = datetime.datetime(year=year, month=1, day=1, hour=hour, minute=min, second=sec)
      date = date + relativedelta(days=days)
      return date

async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      earthdate(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )