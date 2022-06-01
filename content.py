import discord
from discord import app_commands
from discord.ext import commands

SERVER_ID = 543042771070484491

class content(commands.Cog):

    def __init__(self, bot : commands.Bot) -> None:
        self.bot  = bot
    
    @app_commands.command(
        name = "content",
        description = "Gives a link to Steam Workshop collection with all the content packs you need for the TBN server")

    async def content(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message(f"https://steamcommunity.com/workshop/filedetails/?id=2566173658", ephemeral=True)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(
        content(bot),
        guilds = [discord.Object(id = SERVER_ID)]
    )