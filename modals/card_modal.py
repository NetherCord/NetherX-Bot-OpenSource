from disnake import ui, ModalInteraction, PermissionOverwrite, utils, Embed

from views.register_view import RegisterView


class CardModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(label="Ваш никнейм", placeholder="Введите ваш никнейм на НС4", custom_id="user"),
            ui.TextInput(label="Ваш город", placeholder="Введите город в котором вы считаетесь жителем",
                                 custom_id="city")
        ]
        super().__init__(title="Оформление карты", components=components, custom_id="create_card")

    async def callback(self, interaction: ModalInteraction) -> None:
        guild = interaction.guild
        user_minecraft = interaction.text_values["user"]
        city = interaction.text_values["city"]
        user = interaction.author

        user_id = user.id
        guild = interaction.guild
        member = guild.get_member(user_id)
        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            member: PermissionOverwrite(read_messages=True)
        }

        category = utils.get(guild.categories, id=1260365108178063400)

        channel = await guild.create_text_channel(name=f"account-{user}", overwrites=overwrites, category=category)

        embed = Embed()
        embed.add_field(name='Ваш никнейм', value=user_minecraft, inline=False)
        embed.add_field(name='Ваш город', value=city, inline=False)
        embed.set_footer(text="Создано NetherX'ом.",
                         icon_url='https://cdn.discordapp.com/attachments/887281401160941618/1260359132184186880/choo.png?ex=668f0869&is=668db6e9&hm=361ca9f83d2f9c2f6c16013cecb09494270825a11d6d18e54fe9d12a52c3903e&')

        view = RegisterView(user, user_id, channel, user_minecraft)

        message = await channel.send(embed=embed, view=view)
        await message.pin()
        await interaction.response.send_message("Карта успешно создана.", ephemeral=True)


