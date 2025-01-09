import random

from disnake import ui, ButtonStyle, MessageInteraction

from cacher import CacheableDict
from operations.cards import generate_card_number, format_card_number
from operations.db import save_bank_account


bank_accounts = CacheableDict("bank_accounts", {}, True)


class RegisterView(ui.View):
    def __init__(self, user, user_id, channel, username):
        super().__init__()
        self.user = user
        self.user_id = user_id
        self.username = username
        self.channel = channel

    @ui.button(label="Оформить карту", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        user = interaction.author
        user_id = self.user_id
        user_reg = self.user
        channel = self.channel
        card_type = "free"
        if not  interaction.author.guild.get_role(1094231021907623967) in interaction.author.roles:
            await interaction.response.send_message(
                f"У вас недостаточно прав для выполнения этой команды. Пожалуйста, дождитесь администраторов.",
                ephemeral=True)
            return

        card_number = generate_card_number()
        bank_accounts[user_id] = {"balance": 0, "card_type": card_type.lower(), "card_number": card_number}
        save_bank_account(self.user_id, self.username, 0, card_type, card_number, interaction.channel_id)
        await channel.send(f'<@{user_id}>, вы успешно оформили карту.')

        logs = interaction.guild.get_channel(1094230193234776114)
        await logs.send(f"<@{user_id}> оформил {card_type} карту с номером {format_card_number(card_number)}."
                        f"Админ: <@{user.id}>")
