from discord.ext import commands
import discord
import datetime

class RankRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ===== 時間解析 =====
    def parse_times(self, args):

        times = set()

        for arg in args:

            arg = arg.strip()

            # 範囲指定
            if "-" in arg:

                try:

                    start, end = arg.split("-", 1)

                    start = int(start)
                    end = int(end)

                    # 逆対応
                    if start > end:
                        start, end = end, start

                    for t in range(start, end + 1):

                        # 0〜48対応
                        if 0 <= t <= 48:
                            times.add(str(t))

                except:
                    continue

            # 単体
            else:

                try:

                    t = int(arg)

                    if 0 <= t <= 48:
                        times.add(str(t))

                except:
                    continue

        return sorted(times, key=int)

    # ===== 一覧生成 =====
    def build_message(self, guild):

        lines = []

        roles = []

        # 数字ロールのみ取得
        for role in guild.roles:

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

            try:

                raw_hour = int(role.name)

            except:
                continue

            # 24超え対応
            display_hour = raw_hour % 24

            # 翌日判定
            day_offset = raw_hour // 24

            target = now.replace(
                hour=display_hour,
                minute=0,
                second=0,
                microsecond=0
            )

            # 翌日加算
            target += datetime.timedelta(days=day_offset)

            timestamp = int(target.timestamp())

            # BOT除外
            members = [
                m.display_name
                for m in role.members
                if not m.bot
            ]

            # 0人なら表示しない
            if len(members) == 0:
                continue

            # 横並び
            text = "　".join(members)

            notice = ""

            # 6人以上
            if len(members) >= 6:
                notice = f"\n\n{raw_hour}時生存確認"

            lines.append(
                f"<t:{timestamp}:t>　{len(members)}人\n{text}{notice}"
            )

        # 誰もいない
        if not lines:
            return "誰もいないよ"

        return "\n\n".join(lines)

    # ===== 一覧更新 =====
    async def update_message(self, ctx):

        message_text = self.build_message(ctx.guild)

        # BOTの古い一覧を削除
        async for message in ctx.channel.history(limit=20):

            if (
                message.author == self.bot.user
                and (
                    "誰もいないよ" in message.content
                    or "人" in message.content
                )
            ):

                try:
                    await message.delete()

                except:
                    pass

        # 新しい一覧送信
        await ctx.send(message_text)

    # ===== 参加 =====
    @commands.command(
        name="can",
        aliases=["c"]
    )
    async def can(
        self,
        ctx,
        members: commands.Greedy[discord.Member],
        *args
    ):

        # メンション無しなら自分
        if not members:
            members = [ctx.author]

        # 引数無し
        if not args:
            await self.update_message(ctx)
            return

        times = self.parse_times(args)

        for time in times:

            role = discord.utils.get(
                ctx.guild.roles,
                name=time
            )

            # 無ければ作成
            if role is None:

                role = await ctx.guild.create_role(
                    name=time
                )

            # 全員付与
            for member in members:
                await member.add_roles(role)

        await self.update_message(ctx)

    # ===== 離脱 =====
    @commands.command(
        name="drop",
        aliases=["d"]
    )
    async def drop(
        self,
        ctx,
        members: commands.Greedy[discord.Member],
        *args
    ):

        # メンション無しなら自分
        if not members:
            members = [ctx.author]

        # 引数無し
        if not args:
            await self.update_message(ctx)
            return

        times = self.parse_times(args)

        for time in times:

            role = discord.utils.get(
                ctx.guild.roles,
                name=time
            )

            if role:

                # 全員削除
                for member in members:
                    await member.remove_roles(role)

                # BOT除外
                remain_members = [
                    m for m in role.members
                    if not m.bot
                ]

                # 0人ならロール削除
                if len(remain_members) == 0:

                    try:
                        await role.delete()

                    except:
                        pass

        await self.update_message(ctx)

    # ===== 現在一覧 =====
    @commands.command(
        name="now"
    )
    async def now(self, ctx):

        await self.update_message(ctx)

    # ===== 全削除 =====
    @commands.command(
        name="clear"
    )
    async def clear(self, ctx):

        roles = []

        # 数字ロール取得
        for role in ctx.guild.roles:

            if role.name.isdigit():
                roles.append(role)

        for role in roles:

            # 全員から削除
            for member in role.members:

                try:
                    await member.remove_roles(role)

                except:
                    pass

            # ロール削除
            try:
                await role.delete()

            except:
                pass

        await self.update_message(ctx)

async def setup(bot):
    await bot.add_cog(RankRole(bot))
