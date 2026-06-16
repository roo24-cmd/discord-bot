from modules.grok import translate_with_grok
from modules.webhook import get_webhook
from modules.views import OriginalView

# -- Router decides if to translate user text--

async def handle_t_command(ctx, lang, text):

    LANG_MAP = {
    "en": "English",
    "cn": "Chinese (Simplified)",
    "zh": "Chinese (Simplified)",
    "ja": "Japanese",
    "fr": "French"
    }

    target = LANG_MAP.get(lang, "English")

    if not target:
        await ctx.send("Unknown language")
        return

    translated = translate_with_grok(text, target)

    try:
        await ctx.message.delete()
    except:
        pass

    webhook = await get_webhook(ctx.channel)

    view = OriginalView(text)

    await webhook.send(
        content=translated,
        username=ctx.author.display_name,
        avatar_url=ctx.author.display_avatar.url,
        view=view
    )

    