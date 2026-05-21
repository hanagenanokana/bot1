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
    @commands.command(
        name="can",
        aliases=["c"]
    )
    async def can(self, ctx, *args):

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

            # JST
            jst = datetime.timezone(
                datetime.timedelta(hours=9)
            )

            # 現在時刻
            now = datetime.datetime.now(jst)

            # 入力時間
            hour = int(time)

            # JSTの指定時間
            target = now.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            # UnixTime
            timestamp = int(target.timestamp())

            # メンバー
            members = [
                m.display_name
                for m in role.members
                if not m.bot
            ]

            text = " ".join(members)

            notice = ""

            # 6人以上
            if len(members) >= 6:
                notice = f"\n\n{time}時生存確認"

            # ===== 全時間表示 =====

lines = []

# 数字ロールだけ取得
roles = []

for role in ctx.guild.roles:

    if role.name.isdigit():
        roles.append(role)

# 時間順
roles.sort(key=lambda r: int(r.name))

# JST
jst = datetime.timezone(
    datetime.timedelta(hours=9)
)

now = datetime.datetime.now(jst)

for role in roles:

    hour = int(role.name)

    target = now.replace(
        hour=hour,
        minute=0,
        second=0,
        microsecond=0
    )

    timestamp = int(target.timestamp())

    members = [
        m.display_name
        for m in role.members
        if not m.bot
    ]

    text = " ".join(members)

    notice = ""

    if len(members) >= 6:
        notice = f"\n{hour}時生存確認"

    lines.append(
        f"<t:{timestamp}:t>　{len(members)}人\n{text}{notice}"
    )

await ctx.send("\n\n".join(lines))

    # 離脱
    @commands.command(
        name="drop",
        aliases=["d"]
    )
    async def drop(self, ctx, *args):

        times = self.parse_times(args)

        lines = []

        for time in times:

            role_name = time

            # ロール取得
            role = discord.utils.get(
                ctx.guild.roles,
                name=role_name
            )

            if role is None:
                continue

            # ロール削除
            await ctx.author.remove_roles(role)

            # JST
            jst = datetime.timezone(
                datetime.timedelta(hours=9)
            )

            # 現在時刻
            now = datetime.datetime.now(jst)

            # 入力時間
            hour = int(time)

            # JSTの指定時間
            target = now.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            # UnixTime
            timestamp = int(target.timestamp())

            # メンバー
            members = [
                m.mention
                for m in role.members
                if not m.bot
            ]

            text = " ".join(members)

            notice = ""

            # 6人以上
            if len(members) >= 6:
                notice = f"\n\n{time}時生存確認"

            # ===== 全時間表示 =====

lines = []

# 数字ロールだけ取得
roles = []

for role in ctx.guild.roles:

    if role.name.isdigit():
        roles.append(role)

# 時間順
roles.sort(key=lambda r: int(r.name))

# JST
jst = datetime.timezone(
    datetime.timedelta(hours=9)
)

now = datetime.datetime.now(jst)

for role in roles:

    hour = int(role.name)

    target = now.replace(
        hour=hour,
        minute=0,
        second=0,
        microsecond=0
    )

    timestamp = int(target.timestamp())

    members = [
        m.display_name
        for m in role.members
        if not m.bot
    ]

    text = " ".join(members)

    notice = ""

    if len(members) >= 6:
        notice = f"\n{hour}時生存確認"

    lines.append(
        f"<t:{timestamp}:t>　{len(members)}人\n{text}{notice}"
    )

await ctx.send("\n\n".join(lines))

async def setup(bot):
    await bot.add_cog(RankRole(bot))
