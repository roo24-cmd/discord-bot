import os
import discord
from discord.ext import commands
import requests


# --1-- TOKEN / ENV

TOKEN = os.getenv("DISCORD_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")


##print("TOKEN FOUND:", TOKEN is not None)

# --2-- Discord bot

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# --3-- Grok API function

def translate_with_grok(text, target_language="English"):

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-4.3",
        "messages": [
            {
                "role": "system",
                "content": (
                   "You are a high-quality social media translation engine like X (Twitter). "
                   "Translate everything into natural English. "
                   "Keep tone, slang, emotion. "
                   "Output ONLY the translation, no explanation. "
                   f"Translate into {target_language}." )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.3
    }

    res = requests.post(url, headers=headers, json=data)

    # 看真实返回
    print("STATUS:", res.status_code)
    print("BODY:", res.text)
    
    return res.json()["choices"][0]["message"]["content"]


# --4-- Discord command

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#@bot.command()
#async def ping(ctx):
#    await ctx.send("pong")

@bot.command()
async def t(ctx, lang, *, text):
    
    lang_map = {
        "en": "English",
        "c": "Chinese (Simplified)",
        "zh": "Chinese (Simplified)",
        "ja": "Japanese",
        "fr": "French"
    }

    target = lang_map.get(lang, "English")

    async with ctx.typing():
        try:
            result = translate_with_grok(text, "English")
            await ctx.send(result)

        except Exception as e:
            await ctx.send(f"Error: {e}")

        

#@bot.command()
#async def t(ctx, *, text):
#   result = translate_with_grok(text)
#    await ctx.send(result)

#@bot.command()
#async def t(ctx, *, text):
#    await ctx.send(f"收到：{text}")
    
# --5-- Discord command

bot.run(TOKEN)


