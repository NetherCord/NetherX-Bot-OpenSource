from disnake import ui, ModalInteraction, Embed

from cacher import CacheableDict
from operations.db import save_bank_account
from views.approve_item_view import ApproveItemView

products_data = CacheableDict("products_data", {}, True)
bank_accounts = CacheableDict("bank_accounts", {}, True)


class BuyItemModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Количество", placeholder="Введите количество товара",
                         custom_id="product_count"),
            ui.TextInput(label="Айди товара", placeholder="Введите айди товара", custom_id="product_id"),
            ui.TextInput(label="Ячейка", placeholder="Введите номер ячейки", custom_id="cell")
        ]
        super().__init__(title="Покупка товара", components=components, custom_id="buy_product")

    async def callback(self, interaction: ModalInteraction) -> None:
        product_count = interaction.text_values["product_count"]
        cell = interaction.text_values["cell"]
        product_quantity = int(interaction.text_values["product_id"])
        price = products_data[product_quantity]["price"]
        seller_id = products_data[product_quantity]["author_id"]
        seller = str(seller_id)
        result_price = int(price) * int(product_count)
        buyer = interaction.author

        if str(buyer.id) in bank_accounts:
            balance = bank_accounts[str(buyer.id)]["balance"]

            if int(product_count) > 0:
                if int(balance) < int(result_price):
                    await interaction.response.send_message(f'Недостаточно алмазов.', ephemeral=True)
                else:
                    balance -= result_price
                    bank_accounts[str(buyer.id)]["balance"] = balance

                    save_bank_account(str(buyer.id), bank_accounts[buyer.id]["username"], balance, bank_accounts[str(buyer.id)]["card_type"],
                                      bank_accounts[str(buyer.id)]["card_number"],
                                      bank_accounts[str(buyer.id)]["channel_id"])  # Save buyer's bank account

                    await interaction.response.send_message(f'Ожидайте работы курьеров.', ephemeral=True)
                    channel = interaction.guild.get_channel(1218220253117415545)
                    embed = Embed(title="ПОКУПКА ТОВАРА",
                                  description=f"<@&1094232452362420254>\nНОМЕР ТОВАРА: {product_quantity}\nКОЛИЧЕСТВО: {product_count}x\nЯЧЕЙКА: {cell}")
                    view = ApproveItemView(seller, result_price, product_count, buyer, cell, product_quantity)
                    await channel.send(embed=embed, view=view)
        else:
            await interaction.response.send_message(f'Вы не имеете банковского аккаунта!', ephemeral=True)
