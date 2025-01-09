from disnake import ui, ButtonStyle, MessageInteraction

from modals.buy_item_modal import BuyItemModal


class BuyItemView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Купить", style=ButtonStyle.success, custom_id="BuyProduct")
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(BuyItemModal())
