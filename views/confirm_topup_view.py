from disnake import ui, ButtonStyle, MessageInteraction

from cacher import CacheableDict
from operations.db import save_bank_account

bank_accounts = CacheableDict("bank_accounts", {}, True)


class ConfirmTopupView(ui.View):
    def __init__(self, count, user, atm):
        super().__init__()
        self.count = count
        self.user = user
        self.atm = atm

    @ui.button(label="Подтвердить пополнение", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        commission = 0.2
        balance = bank_accounts[self.user]["balance"]
        channel = interaction.guild.get_channel(int(bank_accounts[self.user]["channel_id"]))
        if interaction.author.guild.get_role(1260352618367160392) in interaction.author.roles:
            balance += int(self.count)
        else:
            balance += round(int(self.count) - (int(self.count) * 0.2))
        bank_accounts[self.user]["balance"] = balance
        await channel.send(
            f"<@{self.user}> Пополнение на карту успешно проведено! Теперь вы можете проверить карту на наличие "
            f"алмазов. Ваш банкир: <@{interaction.author.id}>")
        await interaction.response.send_message(
            f'<@{interaction.author.id}>, вы успешно подтвердили пополнение. NSB благодарит вас за выполненую работу.',
            ephemeral=True)
        save_bank_account(self.user, bank_accounts[self.user]["username"], balance, bank_accounts[self.user]["card_type"],
                          bank_accounts[self.user]["card_number"], bank_accounts[self.user]["channel_id"])
        logs = interaction.guild.get_channel(1094230193234776114)
        await logs.send(
            f"<@{self.user}> пополнил {self.count} алм. в банкомате {self.atm}. Банкир: <@{interaction.author.id}>")
