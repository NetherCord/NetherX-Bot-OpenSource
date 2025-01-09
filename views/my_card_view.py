from disnake import ui, ButtonStyle, MessageInteraction

from modals.topup_modal import TopupModal
from modals.transfer_modal import TransferModal
from modals.withdraw_modal import WithdrawModal


class MyCardView(ui.View):
    @ui.button(label="Пополнить", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(TopupModal())

    @ui.button(label="Вывести", style=ButtonStyle.danger)
    async def button2(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(WithdrawModal())

    @ui.button(label="Перевести", style=ButtonStyle.primary)
    async def button3(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(TransferModal())
