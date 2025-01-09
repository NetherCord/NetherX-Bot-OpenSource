from disnake import Embed, ModalInteraction, ui

from cacher import CacheableDict
from views.confirm_withdraw_view import ConfirmWithdrawView

bank_accounts = CacheableDict("bank_accounts", {}, True)


class WithdrawModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Кол-во алм.", placeholder="Введите любое количество алм.", custom_id="count"),
            ui.TextInput(label="Номер банкомата", placeholder="Введите номер банкомата", custom_id="atm")
        ]
        super().__init__(title="Вывод с карты", components=components, custom_id="vivod")

    async def callback(self, interaction: ModalInteraction) -> None:
        if str(interaction.author.id) in bank_accounts:
            count = interaction.text_values["count"]
            atm = interaction.text_values["atm"]
            user = str(interaction.author.id)
            balance = int(bank_accounts[user]["balance"])
            if int(count) < 1:
                await interaction.response.send_message(f'Некорректное число.', ephemeral=True)
            else:
                if balance < int(count):
                    await interaction.response.send_message(f'Недостаточно алмазов.', ephemeral=True)
                else:
                    await interaction.response.send_message(f'Ожидайте работы банкиров.', ephemeral=True)
                    channel = interaction.guild.get_channel(1216476734153560235)
                    embed = Embed(title="ВЫВОД",
                                  description=f"<@&1094232452362420254>\nКОЛ-ВО АЛМ: {count}\nБАНКОМАТ: {atm}")
                    view = ConfirmWithdrawView(count, user, atm)
                    await channel.send(embed=embed, view=view)
        else:
            await interaction.response.send_message(f'Вы не имеете банковского аккаунта!', ephemeral=True)
