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

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ===== Cog Load =====
async def load():
    await bot.load_extension("cogs.dice")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"ログイン成功: {bot.user}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())
