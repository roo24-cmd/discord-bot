import discord

# -- Webhook select specific user --

async def get_webhook(channel):

    webhooks = await channel.webhooks()

    for wh in webhooks:
        if wh.name == "TranslatorWebhook":
            return wh

    return await channel.create_webhook(
        name="TranslatorWebhook"
    )