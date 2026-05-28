from discord.ext import commands
from discord import app_commands
import discord
import asyncio
import statistics

from services.lounge_api import (
    fetch_mmr,
    fetch_peak
)

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ===== 共通 =====
    async def average_command(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        fetch_func,
        title: str,
        mode: str
    ):

        await interaction.response.defer()

        members = [
            m for m in role.members
            if not m.bot
        ]

        if not members:

            await interaction.followup.send(
                "メンバーがいません"
            )

            return

        results = await asyncio.gather(
            *[
                fetch_func(
                    m.id,
                    mode
                )
                for m in members
            ]
        )

        values = []
        lines = []

        for member, value in zip(
            members,
            results
        ):

            if value is None:
                continue

            values.append(value)

            lines.append(
                f"{member.display_name}: {value}"
            )

        if not values:

            await interaction.followup.send(
                "データ取得失敗"
            )

            return

        avg = int(
            statistics.mean(values)
        )

        embed = discord.Embed(
            title=(
                f"{role.name} "
                f"{mode}P "
                f"{title}"
            ),
            description="\n".join(lines),
            color=0x000000
        )

        embed.add_field(
            name="Average",
            value=str(avg),
            inline=False
        )

        await interaction.followup.send(
            embed=embed
        )

    # ===== /team_mmr =====
    @app_commands.command(
        name="team_mmr",
        description="チーム平均MMR"
    )
    @app_commands.describe(
        role="対象ロール",
        game_mode="ゲームモード"
    )
    @app_commands.choices(
        game_mode=[
            app_commands.Choice(
                name="24p",
                value="24"
            ),
            app_commands.Choice(
                name="12p",
                value="12"
            )
        ]
    )
    async def team_mmr(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        season: int,
        game_mode: app_commands.Choice[str]
    ):

        await self.average_command(
            interaction,
            role,
            fetch_mmr,
            "MMR",
            game_mode.value
        )

    # ===== /team_peak =====
    @app_commands.command(
        name="team_peak",
        description="チームPeak"
    )
    @app_commands.describe(
        role="対象ロール",
        game_mode="ゲームモード"
    )
    @app_commands.choices(
        game_mode=[
            app_commands.Choice(
                name="24p",
                value="24"
            ),
            app_commands.Choice(
                name="12p",
                value="12"
            )
        ]
    )
    async def team_peak(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        game_mode: app_commands.Choice[str]
    ):

        await self.average_command(
            interaction,
            role,
            fetch_peak,
            "Peak",
            game_mode.value
        )

async def setup(bot):

    await bot.add_cog(
        Player(bot)
    )
