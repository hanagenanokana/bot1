import discord
from discord.ext import commands
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("TOKEN")

# ===== Web Server =====
class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():

    server = HTTPServer(
        ("0.0.0.0", 8000),
        Handler
    )

    server.serve_forever()

threading.Thread(
    target=run_web,
    daemon=True
).start()

# ===== Discord Intents =====
intents = discord.Intents.default()

# メンバー取得
intents.members = True

# !c 20 用
intents.message_content = True

# ===== Bot =====
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    case_insensitive=True
)

# ===== Load Extensions =====
async def load_extensions():

    # RankRole
    await bot.load_extension(
        "cogs.rankrole"
    )

    # Player
    await bot.load_extension(
        "cogs.player"
    )

    # Lounge API
    await bot.load_extension(
        "services.lounge_api"
    )

    # Dice
    await bot.load_extension(
        "cogs.dice"
    )

    # Stats
    await bot.load_extension(
        "cogs.stats"
    )

    # Uso
    await bot.load_extension(
        "cogs.uso"
    )

# ===== Ready =====
@bot.event
async def on_ready():

    print(
        f"ログイン成功: {bot.user}"
    )

    try:

        # スラッシュコマンド同期
        synced = await bot.tree.sync()

        print(
            f"{len(synced)}個のコマンドを同期しました"
        )

    except Exception as e:

        print(e)

# ===== Main =====
async def main():

    async with bot:

        # Cog読込
        await load_extensions()

        # 起動
        await bot.start(TOKEN)

# ===== Run =====
asyncio.run(main())
