from disnake import ui, ModalInteraction

from cacher import CacheableDict
from operations.cards import parse_card_number
from operations.db import save_bank_account, get_id_by_card_number

bank_accounts = CacheableDict("bank_accounts", {}, True)


class TransferModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Кол-во алм.", placeholder="Введите любое количество алм.", custom_id="count"),
            ui.TextInput(label="Карта получателя",
                         placeholder="Введите номер карты игрока, которому хотите перевести алмазы.",
                         custom_id="receiver")
        ]
        super().__init__(title="Перевод", components=components, custom_id="perevod")

    async def callback(self, interaction: ModalInteraction) -> None:
        if str(interaction.author.id) in bank_accounts:
            count = int(interaction.text_values["count"])
            user = str(interaction.author.id)
            receiver = interaction.text_values["receiver"]
            if not parse_card_number(receiver):
                await interaction.response.send_message(f'Неправильный номер карты.', ephemeral=True)
                return

            receiver_id = get_id_by_card_number(receiver)
            if receiver_id is None:
                await interaction.response.send_message(f'Получатель не найден.', ephemeral=True)
                return
            else:
                receiver_id = receiver_id[0]

            balance = int(bank_accounts[user]["balance"])
            receiver_balance = int(bank_accounts[receiver_id]["balance"])
            if balance < count:
                await interaction.response.send_message(f'Недостаточно алмазов.', ephemeral=True)
            else:
                if count < 1:
                    await interaction.response.send_message(f'Некорректное число.', ephemeral=True)
                else:
                    if interaction.author == interaction.guild.get_member(receiver_id):
                        await interaction.response.send_message(f'Вы пытаетесь перевести самому себе.', ephemeral=True)
                    else:
                        balance -= count
                        receiver_balance += count
                        bank_accounts[user]["balance"] = balance
                        bank_accounts[receiver_id]["balance"] = receiver_balance
                        save_bank_account(user, bank_accounts[user]["username"], balance, bank_accounts[user]["card_type"],
                                          bank_accounts[user]["card_number"], bank_accounts[user]["channel_id"])
                        save_bank_account(receiver_id, bank_accounts[receiver_id]["username"], receiver_balance, bank_accounts[receiver_id]["card_type"],
                                          bank_accounts[receiver_id]["card_number"],
                                          bank_accounts[receiver_id]["channel_id"])
                        await interaction.response.send_message(f'Перевод проведён успешно.', ephemeral=True)
                        logs = interaction.guild.get_channel(1094230193234776114)
                        await logs.send(f"<@{user}> перевёл {count} алм. игроку <@{receiver_id}>")
        else:
            await interaction.response.send_message(f'Вы не имеете банковского аккаунта!', ephemeral=True)
