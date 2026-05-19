from discord.ext import commands
from discord import app_commands
import discord

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="uso", description="餅")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("噓つきは餅の始まり")

async def setup(bot):
    await bot.add_cog(uso(bot))