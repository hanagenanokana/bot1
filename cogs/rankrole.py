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

            # 20-22
            if "-" in arg:

                start, end = arg.split("-")

                start = int(start)
                end = int(end)

                for t in range(start, end + 1):
                    times.add(str(t))

            else:
                times.add(arg)

        return sorted(times, key=int)

    # ===== 一覧生成 =====
    def build_message(self, guild):

        lines = []

        roles = []

        # 数字ロールだけ取得
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
                hour = int(role.name)

            except:
                continue

            target = now.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

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

            text = "\n".join(members)

            notice = ""

            # 6人以上
            if len(members) >= 6:
                notice = f"\n\n{hour}時生存確認"

            lines.append(
                f"<t:{timestamp}:t>　{len(members)}人\n{text}{notice}"
            )

        # 誰もいない
        if not lines:
            return "現在挙手なし"

        return "\n\n".join(lines)

    # ===== 一覧更新 =====
    async def update_message(self, ctx):

        message_text = self.build_message(ctx.guild)

        target_message = None

        # BOTの最新一覧を探す
        async for message in ctx.channel.history(limit=20):

            if (
                message.author == self.bot.user
                and (
                    "現在挙手なし" in message.content
                    or "人" in message.content
                )
            ):
                target_message = message
                break

        # 編集
        if target_message:

            try:
                await target_message.edit(
                    content=message_text
                )
                return

            except:
                pass

        # 無ければ新規送信
        await ctx.send(message_text)

    # ===== 参加 =====
    @commands.command(
        name="can",
        aliases=["c"],
        case_insensitive=True
    )
    async def can(self, ctx, *args):

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

            # ロール付与
            await ctx.author.add_roles(role)

        await self.update_message(ctx)

    # ===== 離脱 =====
    @commands.command(
        name="drop",
        aliases=["d"],
        case_insensitive=True
    )
    async def drop(self, ctx, *args):

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

                # ロール削除
                await ctx.author.remove_roles(role)

                # BOT除外
                members = [
                    m for m in role.members
                    if not m.bot
                ]

                # 0人ならロール削除
                if len(members) == 0:

                    try:
                        await role.delete()

                    except:
                        pass

        await self.update_message(ctx)

    # ===== 現在一覧 =====
    @commands.command(
        name="now",
        case_insensitive=True
    )
    async def now(self, ctx):

        await self.update_message(ctx)

    # ===== 全削除 =====
    @commands.command(
        name="clear",
        case_insensitive=True
    )
    async def clear(self, ctx):

        roles = []

        # 数字ロール取得
        for role in ctx.guild.roles:

            if role.name.isdigit():
                roles.append(role)

        for role in roles:

            # 全員からロール削除
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
