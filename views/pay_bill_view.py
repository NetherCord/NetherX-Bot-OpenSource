from disnake import ui, ButtonStyle, MessageInteraction

from cacher import CacheableDict
from modals.buy_item_modal import BuyItemModal
from operations.db import get_id_by_card_number, save_bills_data, save_bank_account

bank_accounts = CacheableDict("bank_accounts", {}, True)
bills_data = CacheableDict("bills_data", {}, True)


class PayBillView(ui.View):
    def __init__(self, bill_number):
        super().__init__(timeout=None)
        self.bill_number = bill_number

    @ui.button(label="Подтвердить оплату", style=ButtonStyle.success, custom_id="ConfirmPayment")
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        user_id = str(interaction.user.id)
        amount = int(bills_data[self.bill_number]["amount"])
        receiver = get_id_by_card_number(bills_data[self.bill_number]["card_to"])[0]    
        from_balance = bank_accounts[user_id]["balance"]
        to_balance = bank_accounts[receiver]["balance"]
        from_balance -= amount
        to_balance += amount
        await interaction.send(f"Счёт успешно оплачен!\n\nОставшаяся сумма на вашем счёте: { from_balance }")
        save_bank_account(user_id, bank_accounts[user_id]["username"],  from_balance, bank_accounts[user_id]['card_type'],
                          bank_accounts[user_id]['card_number'], bank_accounts[user_id]['channel_id'])
        save_bank_account(receiver, bank_accounts[user_id]["username"], to_balance, bank_accounts[receiver]['card_type'],
                          bank_accounts[receiver]['card_number'], bank_accounts[receiver]['channel_id'])
        save_bills_data(self.bill_number, bills_data[self.bill_number]["name"], amount,
                        bills_data[self.bill_number]["card_to"], 1)
