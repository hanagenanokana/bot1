from discord.ext import commands
from discord import app_commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="stats")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("雑魚！wwwwwwwwwww")

async def setup(bot):
    await bot.add_cog(stats(bot))