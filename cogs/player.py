from discord.ext import commands
from discord import app_commands
import discord
import asyncio
import statistics

from services.lounge_api import fetch_mmr
from services.lounge_api import fetch_peak

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ===== 共通処理 =====
    async def _average_mmr_command(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        fetch_func,
        title_suffix: str,
        mode: str
    ):

        await interaction.response.defer()

        members = [
            m for m in role.members
            if not m.bot
        ]

        if not members:

            await interaction.followup.send(
                "そのロールにメンバーがいません。"
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
        skipped = 0

        for member, value in zip(members, results):

            if value is None:
                skipped += 1
                continue

            values.append(value)

            lines.append(
                f"{member.display_name}: **{value}**"
            )

        if not values:

            await interaction.followup.send(
                "取得できるデータがありません。"
            )

            return

        avg = int(statistics.mean(values))

        embed = discord.Embed(
            title=(
                f"{role.name} の "
                f"{mode}P {title_suffix}"
            ),
            description="\n".join(lines[:20]),
            color=discord.Color.green()
        )

        embed.add_field(
            name="Average",
            value=f"**{avg}**",
            inline=False
        )

        embed.set_footer(
            text=(
                f"{len(values)}人分 | "
                f"placement {skipped}人"
            )
        )

        await interaction.followup.send(
            embed=embed
        )

    # ===== /team_mmr =====
    @app_commands.command(
        name="team_mmr",
        description="MMR一覧"
    )
    @app_commands.describe(
        role="対象ロール",
        mode="12Pか24Pを選択"
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(
                name="24P",
                value="24"
            ),
            app_commands.Choice(
                name="12P",
                value="12"
            )
        ]
    )
    async def team_mmr(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        mode: app_commands.Choice[str]
    ):

        await self._average_mmr_command(
            interaction,
            role,
            fetch_mmr,
            "MMR",
            mode.value
        )

    # ===== /team_peak =====
    @app_commands.command(
        name="team_peak",
        description="Peak一覧"
    )
    @app_commands.describe(
        role="対象ロール",
        mode="12Pか24Pを選択"
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(
                name="24P",
                value="24"
            ),
            app_commands.Choice(
                name="12P",
                value="12"
            )
        ]
    )
    async def team_peak(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        mode: app_commands.Choice[str]
    ):

        await self._average_mmr_command(
            interaction,
            role,
            fetch_peak,
            "Peak MMR",
            mode.value
        )

async def setup(bot):
    await bot.add_cog(Player(bot))
