from disnake import ui, ModalInteraction, Embed

from cacher import CacheableDict
from operations.db import save_product
from views.buy_item_view import BuyItemView

products_data = CacheableDict("products_data", {}, True)


class AddItemModal(ui.Modal):
    def __init__(self, guild):
        components = [
            ui.TextInput(label="Название", placeholder="Введите название товара", custom_id="product_name"),
            ui.TextInput(label="Цена", placeholder="Введите цену товара", custom_id="price"),
            ui.TextInput(label="Описание", placeholder="Введите описание товара", custom_id="description"),
            ui.TextInput(label="Ссылка на картинку", placeholder="Введите ссылку на картинку товара",
                         custom_id="link_to_image")
        ]
        self.guild = guild
        super().__init__(title="Добавить товар", components=components, custom_id="add_product")

    async def callback(self, interaction: ModalInteraction) -> None:
        product_name = interaction.text_values["product_name"]
        price = interaction.text_values["price"]
        description = interaction.text_values["description"]
        link_to_image = interaction.text_values["link_to_image"]
        if int(price) > 0:
            product_quantity = len(products_data)
            products_data[product_quantity] = {"creator_id": interaction.author.id, "product_name": product_name,
                                               "price": price, "image": link_to_image, "description": description,
                                               "token": product_quantity}
            save_product(product_quantity, interaction.author.id, product_name, price, description, link_to_image, )
            await interaction.send(
                f'<@{interaction.author.id}>, товар "{product_name}" успешно создан! Его номер: {product_quantity}')

            channel = self.guild.get_channel(1220287252031213669)

            title = f'{product_name} - {price} алм.'
            content = f'**{product_name}** за **{price}** алм.\n**Описание:** {description}'

            embed = Embed(
                description=f'**{product_name}** за **{price}** алм.\n**Описание:** {description}\n**Айди:** {product_quantity}')

            embed.set_image(url=link_to_image)

            view = BuyItemView()

            # Создаем новое обсуждение (тему) в форуме
            await channel.create_thread(name=title, embed=embed, view=view)
