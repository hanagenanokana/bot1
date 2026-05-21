from discord.ext import commands
import discord
import datetime

class RankRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # サーバーごとの一覧メッセージ保存
        self.status_messages = {}

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
                f"## <t:{timestamp}:t>　{len(members)}人\n{text}{notice}"
            )

        # 誰もいない
        if not lines:
            return "現在挙手なし"

        return "\n\n".join(lines)

    # ===== 一覧更新 =====
    async def update_message(self, ctx):

        message_text = self.build_message(ctx.guild)

        old_message = self.status_messages.get(ctx.guild.id)

        # 既存メッセージ編集
        if old_message:

            try:
                await old_message.edit(
                    content=message_text
                )
                return

            except:
                pass

        # 新規送信
        new_message = await ctx.send(message_text)

        self.status_messages[ctx.guild.id] = new_message

    # ===== 参加 =====
    @commands.command(
        name="can",
        aliases=["c"]
    )
    async def can(self, ctx, *args):

        # 引数なしなら一覧
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
        aliases=["d"]
    )
    async def drop(self, ctx, *args):

        # 引数なしなら一覧
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

                # 人間だけ取得
                human_members = [
                    m for m in role.members
                    if not m.bot
                ]

                # 0人ならロール削除
                if len(human_members) == 0:

                    await role.delete()

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
