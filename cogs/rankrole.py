from discord.ext import commands
import discord
import datetime

class RankRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 時間解析
    def parse_times(self, args):

        times = set()

        for arg in args:

            # 20-22
            if "-" in arg:

                start, end = arg.split("-")

                start = int(start)
                end = int(end)

                for t in range(start, end + 1):
                    times.add(str(t))

            # 単体
            else:
                times.add(arg)

        return sorted(times, key=int)

    # 参加
    @commands.command()
    async def c(self, ctx, *args):

        times = self.parse_times(args)

        lines = []

        for time in times:

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

            # タイムスタンプ
            now = datetime.datetime.now()

            hour = int(time)

            target = now.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            timestamp =

int(target.timestamp())

            # メンバー
            members = [
                m.mention
                for m in role.members
                if not m.bot
            ]

            text = " ".join(members)

            lines.append(
                f"<t:{timestamp}:t>　{len(members)}人\n{text}"
            )

        await ctx.send("\n\n".join(lines))

    # 離脱
    @commands.command()
    async def d(self, ctx, *args):

        times = self.parse_times(args)

        lines = []

        for time in times:

            role_name = time

            role = discord.utils.get(
                ctx.guild.roles,
                name=role_name
            )

            if role is None:
                continue

            # ロール削除
            await ctx.author.remove_roles(role)

            # タイムスタンプ
            now = datetime.datetime.now()

            hour = int(time)

            target = now.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            timestamp = int(target.timestamp())

            # メンバー
            members = [
                m.mention
                for m in role.members
                if not m.bot
            ]

            text = " ".join(members)

            lines.append(
                f"<t:{timestamp}:t>　{len(members)}人\n{text}"
            )

        await ctx.send("\n\n".join(lines))

async def setup(bot):
    await bot.add_cog(RankRole(bot))
