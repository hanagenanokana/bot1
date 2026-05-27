from discord.ext import commands
import discord
import aiohttp

class LoungeAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ===== プレイヤー検索 =====
    @commands.command(
        name="mmr",
        aliases=["lounge"]
    )
    async def mmr(self, ctx, *, player_name):

        url = (
            "https://www.mk8dx-lounge.com/api/player?"
            f"name={player_name}"
        )

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                # API失敗
                if response.status != 200:

                    await ctx.send("プレイヤーが見つかりません")
                    return

                data = await response.json()

        # データ無し
        if not data:

            await ctx.send("プレイヤーが見つかりません")
            return

        # ===== プレイヤーデータ =====
        player = data[0]

        name = player.get("name", "Unknown")

        # MMR
        mmr24 = player.get("mmr_24p", "なし")
        mmr12 = player.get("mmr_12p", "なし")

        # Discord名
        discord_name = player.get("discordName", "なし")

        # FC
        fc = player.get("fc", "なし")

        # 国
        country = player.get("countryCode", "なし")

        # ランク
        rank = player.get("rank", "なし")

        # ===== Embed =====
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
            name="Rank",
            value=rank,
            inline=True
        )

        embed.add_field(
            name="FC",
            value=fc,
            inline=False
        )

        embed.add_field(
            name="Discord",
            value=discord_name,
            inline=False
        )

        embed.add_field(
            name="Country",
            value=country,
            inline=True
        )

        embed.set_footer(
            text="MK8DX Lounge API"
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LoungeAPI(bot))
