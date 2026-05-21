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
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()

# ===== Discord Bot =====
intents = discord.Intents.default()

# ロールメンバー取得用
intents.members = True

# !c 20 みたいな通常コマンド用
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    case_insensitive=True
)

# ===== Cog Load =====
async def load():

    # 参加募集
    await bot.load_extension("cogs.rankrole")

    # MMR関連
    await bot.load_extension("cogs.player")

    # サイコロ
    await bot.load_extension("cogs.dice")

    # stats
    await bot.load_extension("cogs.stats")

    # uso
    await bot.load_extension("cogs.uso")

# ===== Ready =====
@bot.event
async def on_ready():

    print(f"ログイン成功: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")

    except Exception as e:
        print(e)

# ===== Main =====
async def main():

    async with bot:

        await load()

        await bot.start(TOKEN)

# ===== Run =====
asyncio.run(main())
