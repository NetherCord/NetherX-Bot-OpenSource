from disnake import ui, ButtonStyle, MessageInteraction

from cacher import CacheableDict
from modals.add_item_modal import AddItemModal
from operations.db import save_bank_account

seller_data = CacheableDict("seller_data", {})
bank_accounts = CacheableDict("bank_accounts", {}, True)

class SellerZoneView(ui.View):
    @ui.button(label="Добавить товар", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_modal(AddItemModal(interaction.guild))

    @ui.button(label="Вывести", style=ButtonStyle.danger)
    async def button2(self, button: ui.Button, interaction: MessageInteraction):
        user_id = interaction.author.id
        str_id = str(user_id)

        if str_id not in seller_data:
            seller_data[str_id] = {"sales": 0}

        sales = seller_data[str_id].get("sales", 0)
        income = seller_data[str_id].get("income", 0)
        revenue = seller_data[str_id].get("revenue", 0) - (income * 0.2)

        if income >= 10:
            if str_id in ["611966852003790861", "718716985042665532"]:
                print('mixate!')
                bank_accounts[str_id]["balance"] += income
                await interaction.response.send_message(f'Вы успешно вывели {income} алм.! Комиссия для вас отсутствует.')
                seller_data[str_id]["income"] = 0
                seller_data[str_id]["revenue"] = 0

                save_bank_account(
                    str_id, 
                    bank_accounts[str_id]["username"], 
                    bank_accounts[str_id]["balance"],
                    bank_accounts[str_id]["card_type"], 
                    bank_accounts[str_id]["card_number"],
                    bank_accounts[str_id]["channel_id"]
                )

                logs = interaction.guild.get_channel(1094230193234776114)
                await logs.send(f"<@{str_id}> снял {income} алм. с панели продавца.")
            else:
                print('no mixate')
                bank_accounts[str_id]["balance"] += round(revenue)
                await interaction.response.send_message(f'Вы успешно вывели {round(revenue)} алм.!')
                seller_data[str_id]["income"] = 0
                seller_data[str_id]["revenue"] = 0
                
                save_bank_account(
                    str_id, 
                    bank_accounts[str_id]["username"], 
                    bank_accounts[str_id]["balance"],
                    bank_accounts[str_id]["card_type"], 
                    bank_accounts[str_id]["card_number"],
                    bank_accounts[str_id]["channel_id"]
                )

                logs = interaction.guild.get_channel(1094230193234776114)
                await logs.send(f"<@{str_id}> снял {round(revenue)} алм. с панели продавца.")
        else:
            await interaction.response.send_message(f'Минимальная сумма вывода: 10 алм.')

    @ui.button(label="Удалить товар", style=ButtonStyle.primary)
    async def button3(self, button: ui.Button, interaction: MessageInteraction):
        await interaction.response.send_message(f'Для удаления товара обращайтесь к <@611966852003790861>')
