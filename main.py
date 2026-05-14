import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import discord
from discord import app_commands

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
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("同期完了")

client = MyClient()

@client.tree.command(name="uso", description="餅")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("噓つきは餅の始まり")

@client.tree.command(name="stats", description="stats")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("雑魚！wwwwwwwwwww")


client.run(TOKEN)
