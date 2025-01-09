from disnake import ui, MessageInteraction, ButtonStyle

from modals.card_modal import CardModal


class CardView(ui.View):
    @ui.button(label="Оформить карту", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(CardModal())
