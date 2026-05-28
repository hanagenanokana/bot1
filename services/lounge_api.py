from discord.ext import commands
import discord
import aiohttp

# ===== MMR取得 =====
async def fetch_mmr(
    discord_id,
    mode,
    season
):

    url = (
        "https://www.mk8dx-lounge.com/api/player?"
        f"discordId={discord_id}"
    )

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as response:

            if response.status != 200:
                return None

            data = await response.json()

    if not data:
        return None

    player = data[0]

    # 12P / 24P
    if mode == "12":

        return player.get(
            "mmr_12p"
        )

    else:

        return player.get(
            "mmr_24p"
        )

# ===== Peak取得 =====
async def fetch_peak(
    discord_id,
    mode,
    season
):

    url = (
        "https://www.mk8dx-lounge.com/api/player?"
        f"discordId={discord_id}"
    )

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as response:

            if response.status != 200:
                return None

            data = await response.json()

    if not data:
        return None

    player = data[0]

    # 12P / 24P
    if mode == "12":

        return player.get(
            "maxMmr_12p"
        )

    else:

        return player.get(
            "maxMmr_24p"
        )

# ===== Cog =====
class LoungeAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ===== /mmr =====
    @commands.command(
        name="mmr",
        aliases=["lounge"]
    )
    async def mmr(
        self,
        ctx,
        *,
        player_name
    ):

        url = (
            "https://www.mk8dx-lounge.com/api/player?"
            f"name={player_name}"
        )

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                if response.status != 200:

                    await ctx.send(
                        "プレイヤーが見つかりません"
                    )

                    return

                data = await response.json()

        if not data:

            await ctx.send(
                "プレイヤーが見つかりません"
            )

            return

        player = data[0]

        name = player.get(
            "name",
            "Unknown"
        )

        mmr24 = player.get(
            "mmr_24p",
            "なし"
        )

        mmr12 = player.get(
            "mmr_12p",
            "なし"
        )

        peak24 = player.get(
            "maxMmr_24p",
            "なし"
        )

        peak12 = player.get(
            "maxMmr_12p",
            "なし"
        )

        fc = player.get(
            "fc",
            "なし"
        )

        rank = player.get(
            "rank",
            "なし"
        )

        embed = discord.Embed(
            title=f"{name} の Lounge情報",
            color=0x000000
        )

        embed.add_field(
            name="24P MMR",
            value=mmr24,
            inline=True
        )

        embed.add_field(
            name="12P MMR",
            value=mmr12,
            inline=True
        )

        embed.add_field(
            name="24P Peak",
            value=peak24,
            inline=True
        )

        embed.add_field(
            name="12P Peak",
            value=peak12,
            inline=True
        )

        embed.add_field(
            name="Rank",
            value=rank,
            inline=True
        )

        embed.add_field(
            name="FC",
            value=fc,
            inline=False
        )

        await ctx.send(embed=embed)

# ===== Setup =====
async def setup(bot):

    await bot.add_cog(
        LoungeAPI(bot)
    )
