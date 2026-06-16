# import os
# import discord
# from discord.ext import commands
# from dotenv import load_dotenv
# import requests

# load_dotenv()

# # =====================
# # 1. ENV
# # =====================

# TOKEN = os.getenv("DISCORD_TOKEN")
# XAI_API_KEY = os.getenv("XAI_API_KEY")

# # =====================
# # 2. BOT SETUP
# # =====================

# intents = discord.Intents.default()
# intents.message_content = True  # 必须，否则 command 可能失效

# bot = commands.Bot(command_prefix="!", intents=intents)

# # =====================
# # 3. GROK TRANSLATION
# # =====================

# def translate_with_grok(text, target_language):

#     url = "https://api.x.ai/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {XAI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "grok-4.3",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     f"You are a high-quality social media translation engine like X (Twitter). "
#                     f"Translate everything into {target_language}. "
#                     "Keep tone, slang, emotion. "
#                     "Output ONLY the translation, no explanation."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": f"Translate into {target_language}:\n\n{text}"
#             }
#         ],
#         "temperature": 0.3
#     }

#     res = requests.post(url, headers=headers, json=data)

#     if res.status_code != 200:
#         print("ERROR:", res.text)
#         return "Translation failed."

#     return res.json()["choices"][0]["message"]["content"]


# # =====================
# # 4. BUTTON (Show Original)
# # =====================

# class TranslateView(discord.ui.View):
#     def __init__(self, original_text):
#         super().__init__(timeout=300)
#         self.original_text = original_text

#     @discord.ui.button(label="Show Original", style=discord.ButtonStyle.secondary)
#     async def show_original(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.send_message(
#             f"**Original:** {self.original_text}",
#             ephemeral=True
#         )


# # =====================
# # 5. COMMAND
# # =====================

# @bot.command()
# async def t(ctx, lang, *, text):

#     lang_map = {
#         "en": "English",
#         "zh": "Chinese (Simplified)",
#         "c": "Chinese (Simplified)",
#         "ja": "Japanese",
#         "jp": "Japanese",
#         "fr": "French"
#     }

#     target = lang_map.get(lang, "English")

#     async with ctx.typing():
#         try:
#             result = translate_with_grok(text, target)

#             # ====== Embed UI（核心升级点） ======
#             embed = discord.Embed(
#                 description=f"**{result}**",
#                 color=0x00ffcc
#             )

#             embed.set_footer(text="Translation bot · Click button to view original")

#             await ctx.send(
#                 embed=embed,
#                 view=TranslateView(text)
#             )

#         except Exception as e:
#             await ctx.send(f"Error: {e}")


# # =====================
# # 6. READY EVENT
# # =====================

# @bot.event
# async def on_ready():
#     print(f"Logged in as {bot.user}")


# # =====================
# # RUN
# # =====================

# bot.run(TOKEN)



# ----------------------------------------------------------------------------------------------------



import os
import discord
from discord.ext import commands
#from dotenv import load_dotenv
import requests

#load_dotenv()

# =====================
# 1. ENV
# =====================

TOKEN = os.getenv("DISCORD_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# =====================
# 2. BOT SETUP
# =====================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =====================
# 3. GROK TRANSLATION
# =====================

def translate_with_grok(text, target_language):

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-4.3",
        "messages": [
            {
                "role": "system",
                "content": f"""
                You are a professional multilingual SNS translation engine.

                Your job:
                - Translate SNS content accurately into {target_language}
                - Preserve tone, slang, emojis, and formatting
                - Do NOT over-translate or explain anything
                - Output ONLY translated text

                =====================
                STRICT RULES
                =====================

                1. For Ensemble Stars (あんさんぶるスターズ！！ / Enstars):
                - DO NOT perform literal machine translation of names or game terms.
                - DO NOT invent new translations.
                - Instead, use commonly accepted fandom / SNS / official community naming conventions.
                - If multiple translations exist, prefer the one most widely used on X (Twitter) and fan communities.

                2. SNS behavior rules:
                - Preserve slang, memes, abbreviations
                - Preserve emotional tone (anger, excitement, sarcasm)
                - Preserve emojis and hashtags
                - Do not formalize casual speech

                3. Translation style:
                - Prefer community-accepted fandom translations
                - If unsure, KEEP original term instead of guessing
                - Do not add explanations or footnotes

                4. Output format:
                - ONLY translated text
                - No commentary
                - No notes
                """
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.3
    }

    res = requests.post(url, headers=headers, json=data)

    if res.status_code != 200:
        print("ERROR:", res.text)
        return "Translation failed."

    return res.json()["choices"][0]["message"]["content"]


# =====================
# 4. COMMAND (REPLY VERSION)
# =====================

@bot.command()
async def t(ctx, lang, *, text):

    lang_map = {
        "en": "English",
        "zh": "Chinese (Simplified)",
        "c": "Chinese (Simplified)",
        "ja": "Japanese",
        "jp": "Japanese",
        "fr": "French"
    }

    target = lang_map.get(lang, "English")

    async with ctx.typing():
        try:
            result = translate_with_grok(text, target)

            # ⭐ 核心变化：reply 原消息 + 只发翻译结果
            await ctx.reply(result)

        except Exception as e:
            await ctx.reply(f"Error: {e}")


# =====================
# 5. READY EVENT
# =====================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# =====================
# RUN
# =====================

bot.run(TOKEN)
