import discord
from discord.ext import commands
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_URL = "https://cryptoaim-streamer-discord-bot.hf.space/api/predict"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

channel_history = {}

@bot.event
async def on_ready():
    print(f"✅ Bot online als {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        channel_id = message.channel.id
        user_input = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        
        history = "\n".join(channel_history.get(channel_id, [])[-20:])
        
        async with message.channel.typing():
            try:
                response = requests.post(HF_API_URL, json={"data": [user_input, history]}, timeout=30)
                answer = response.json()["data"][0]
                
                channel_history[channel_id] = channel_history.get(channel_id, []) + [f"User: {user_input}", f"Bot: {answer}"]
                channel_history[channel_id] = channel_history[channel_id][-20:]
                
                await message.reply(answer[:2000])
            except Exception as e:
                print(f"Fehler: {e}")
                await message.reply("Sekunde, bin grad am buffern...")

bot.run(DISCORD_TOKEN)