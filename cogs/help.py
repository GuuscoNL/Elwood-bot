import discord
from discord import app_commands
from discord.ext import commands


SERVER_ID = 543042771070484491
ADMIN_ROLE_ID = 701895569060135005

class help(commands.Cog):

   def __init__(self, bot : commands.Bot) -> None:
      self.bot  = bot
   
   @app_commands.command(
      name = "help",
      description = "Gives a list with all the commands are and what they do")
    
   @app_commands.checks.has_any_role(ADMIN_ROLE_ID)
   async def help(self, interaction : discord.Interaction) -> None:

      em = discord.Embed(title="Elwood commands:")
      em = await self.help_admin(em)
      em = await self.help_public(em)
      await interaction.response.send_message(embed=em, ephemeral=True)
      
   @help.error
   async def permission(self, interaction : discord.Interaction, error : app_commands.AppCommandError) -> None:  
      if isinstance(error, app_commands.MissingAnyRole):
         if interaction.user.id == 397046303378505729:
            em = discord.Embed(title="Elwood commands:")
            em = await self.help_admin(em)
            await interaction.response.send_message(embed= await self.help_public(em), ephemeral=True)
         else:
            em = discord.Embed(title="Elwood commands:")
            await interaction.response.send_message(embed= await self.help_public(em), ephemeral=True)
   
   async def help_public(self, em : discord.Embed):
      public_help = '''`/help`
      Gives a list with all the commands and what they do
      
      `/content`
      Gives a link to Steam Workshop collection with all the content packs you need for the TBN server
      
      `/roll`
      Rolls between 0 and 100
      
      `/invite`
      Sends an invite link that you can share with people
      
      `/guus`
      Gives an explanation and a video on how to pronounce Guus correctly
      '''
      em.add_field(name="Public commands:", value=public_help)
      return em
   
   async def help_admin(self, em : discord.Embed):
      admin_help = '''`/help`
      If the user has the admin role it will show the admin commands
      
      `/ping`
      Pings the bot
      
      `/restart`
      Restarts the bot
      
     `!send_server_info`
      Shows what the variable send_server_info is set to (if True the bot will update the message)
      
      `!toggle_server`
      Toggles the send_server_info variable
      '''
      em.add_field(name="Admin commands:", value=admin_help)
      return em

async def setup(bot : commands.Bot) -> None:
   await bot.add_cog(
      help(bot),
      guilds = [discord.Object(id = SERVER_ID)]
   )