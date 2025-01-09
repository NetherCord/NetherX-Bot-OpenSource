from disnake import ui

from cacher import CacheableDict
from operations.db import *


bank_accounts = CacheableDict("bank_accounts", {}, True)


class ConfirmWithdrawView(ui.View):
    def __init__(self, count, user, atm):
        super().__init__()
        self.count = count
        self.user = user
        self.atm = atm

    @ui.button(label="Подтвердить вывод", style=disnake.ButtonStyle.success)
    async def button1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        balance = bank_accounts[self.user]["balance"]
        channel = interaction.guild.get_channel(int(bank_accounts[self.user]["channel_id"]))
        balance -= int(self.count)
        bank_accounts[self.user]["balance"] = balance
        await channel.send(
            f"<@{self.user}> Вывод с карты успешно проведён! Приходите к банкомату {self.atm}, чтобы забрать алмазы. "
            f"Ваш банкир: <@{interaction.author.id}>")
        await interaction.response.send_message(
            f'<@{interaction.author.id}>, вы успешно подтвердили вывод. NSB благодарит вас за выполненую работу.',
            ephemeral=True)
        save_bank_account(
            self.user, 
            bank_accounts[self.user]["username"],
            balance, 
            bank_accounts[self.user]["card_type"],
            bank_accounts[self.user]["card_number"], 
            bank_accounts[self.user]["channel_id"]
        )
        logs = interaction.guild.get_channel(1094230193234776114)
        await logs.send(
            f"<@{self.user}> снял {self.count} алм. в банкомате {self.atm}. Банкир: <@{interaction.author.id}>")
