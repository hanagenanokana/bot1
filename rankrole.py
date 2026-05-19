from discord.ext import commands
import discord
import datetime

class RankRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 参加
    @commands.command()
    async def c(self, ctx, time: str):

        # ロール名
        role_name = time

        # ロール取得
        role = discord.utils.get(
            ctx.guild.roles,
            name=role_name
        )

        # 無ければ作成
        if role is None:
            role = await ctx.guild.create_role(
                name=role_name
            )

        # ロール付与
        await ctx.author.add_roles(role)

        # 現在時刻
        now = datetime.datetime.now()

        # 入力時間
        hour = int(time)

        # 今日のその時間
        target = now.replace(
            hour=hour,
            minute=0,
            second=0,
            microsecond=0
        )

        # UnixTime
        timestamp = int(target.timestamp())

        # 人間メンバー取得
        members = [
            m.mention
            for m in role.members
            if not m.bot
        ]

        # 表示
        text = " ".join(members)

        await ctx.send(
            f"<t:{timestamp}:t>　{len(members)}人\n{text}"
        )

    # 離脱
    @commands.command()
    async def d(self, ctx, time: str):

        role_name = time

        # ロール取得
        role = discord.utils.get(
            ctx.guild.roles,
            name=role_name
        )

        if role is None:
            return

        # ロール削除
        await ctx.author.remove_roles(role)

        # 現在時刻
        now = datetime.datetime.now()

        # 入力時間
        hour = int(time)

        # 今日のその時間
        target = now.replace(
            hour=hour,
            minute=0,
            second=0,
            microsecond=0
        )

        # UnixTime
        timestamp = int(target.timestamp())

        # 人間メンバー取得
        members = [
            m.mention
            for m in role.members
            if not m.bot
        ]

        # 表示
        text = " ".join(members)

        await ctx.send(
            f"<t:{timestamp}:t>　{len(members)}人\n{text}"
        )

async def setup(bot):
    await bot.add_cog(RankRole(bot))