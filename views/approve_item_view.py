from disnake import ui, ButtonStyle, MessageInteraction

from cacher import CacheableDict
from operations.db import save_seller_data

bank_accounts = CacheableDict("bank_accounts", {}, True)
seller_data = CacheableDict("seller_data", {}, True)


class ApproveItemView(ui.View):
    def __init__(self, seller, result_price, product_count, buyer, cell, product_quantity):
        super().__init__()
        self.seller = seller
        self.result_price = result_price
        self.product_count = product_count
        self.buyer = buyer
        self.cell = cell
        self.product_quantity = product_quantity

    @ui.button(label="Товар доставлен", style=ButtonStyle.success)
    async def button1(self, button: ui.Button, interaction: MessageInteraction):
        income = seller_data[self.seller]["income"]
        revenue = seller_data[self.seller]["revenue"]
        total_revenue = seller_data[self.seller]["total_revenue"]

        channel = interaction.guild.get_channel(int(bank_accounts[str(self.buyer.id)]["channel_id"]))

        income += int(self.result_price)
        seller_data[self.seller]["income"] = income
        revenue += int(self.product_count)
        seller_data[self.seller]["revenue"] = revenue
        total_revenue += int(self.product_count)
        seller_data[self.seller]["total_revenue"] = total_revenue

        save_seller_data(self.seller, income, revenue, total_revenue)  # Save seller data

        await channel.send(
            f"<@{self.buyer.id}> Товар доставлен! Приходите к ячейке {self.cell}, чтобы забрать товар. Ваш курьер: <@{interaction.author.id}>")
        await interaction.response.send_message(
            f'<@{interaction.author.id}>, вы успешно доставили товар. NSB благодарит вас за выполненную работу.',
            ephemeral=True)

        logs = interaction.guild.get_channel(1094230193234776114)
        await logs.send(
            f"<@{self.buyer.id}> купил товар номер {self.product_quantity} в количестве {self.product_count}x за {self.result_price} алм. Продавец: <@{self.seller}>. Курьер: <@{interaction.author.id}>")

