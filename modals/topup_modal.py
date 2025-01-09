from disnake import ui, ModalInteraction, Embed

from cacher import CacheableDict
from views.confirm_topup_view import ConfirmTopupView

bank_accounts = CacheableDict("bank_accounts", {}, True)


class TopupModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Кол-во алм.", placeholder="Введите любое количество алм.", custom_id="count"),
            ui.TextInput(label="Номер банкомата", placeholder="Введите номер банкомата", custom_id="atm")
        ]
        super().__init__(title="Пополнить карту", components=components, custom_id="popolnit")

    async def callback(self, interaction: ModalInteraction) -> None:
        user_id = str(interaction.author.id)
        if user_id in bank_accounts:
            count = interaction.text_values["count"]
            atm = interaction.text_values["atm"]
            if int(count) < 1:
                await interaction.response.send_message(f'Некорректное число.', ephemeral=True)
            else:
                await interaction.response.send_message(f'Ожидайте работы банкиров.')
                channel = interaction.guild.get_channel(1216476734153560235)
                embed = Embed(title="ПОПОЛНЕНИЕ",
                              description=f"<@&1094232452362420254>\nКОЛ-ВО АЛМ: {count}\nБАНКОМАТ: {atm}")
                view = ConfirmTopupView(count, user_id, atm)
                await channel.send(embed=embed, view=view)
        else:
            await interaction.response.send_message(f'Вы не имеете банковского аккаунта!', ephemeral=True)
