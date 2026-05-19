from discord.ext import commands
from discord import app_commands
import discord
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dice", description="サイコロを振ります")
    async def dice(self, interaction: discord.Interaction):
        number = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 {number}")

async def setup(bot):
    await bot.add_cog(Dice(bot))