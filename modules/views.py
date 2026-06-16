import discord

# -- Show original text button --

class OriginalView(discord.ui.View):

    def __init__(self, original_text: str):
        super().__init__(timeout=None)
        self.original_text = original_text

    @discord.ui.button(
        label="Show Original",
        style=discord.ButtonStyle.secondary
    )
    async def show_original(self, interaction, button):

        await interaction.response.send_message(
            f"原文：\n{self.original_text}",
            ephemeral=True
        )