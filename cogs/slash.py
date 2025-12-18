import discord
from discord.ext import commands
from discord import app_commands

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="你好", description="打招呼")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"你好，{interaction.user.display_name}!")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
