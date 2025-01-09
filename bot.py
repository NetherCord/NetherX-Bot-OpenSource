import os

import disnake
from disnake.ext import commands
from disnake.ui import button
import random
import asyncio

from cacher import CacheableDict
from operations.cards import format_card_number
from operations.config import get_config, get_from_config, get_bank_setting
from operations.db import load_bank_accounts, load_products_data, load_seller_data, save_bank_account, \
    save_seller_data, save_product, load_bills_data, load_api_tokens
from views.buy_item_view import BuyItemView
from views.card_view import CardView
from views.confirm_topup_view import ConfirmTopupView
from views.confirm_withdraw_view import ConfirmWithdrawView
from views.my_card_view import MyCardView
from views.pay_bill_view import PayBillView
from views.seller_zone_view import SellerZoneView

BASE_DIR = os.environ["NETHERX_BASE_DIR"]


intents = disnake.Intents.all()

promocodes = get_bank_setting("promocodes")

bank_accounts = CacheableDict("bank_accounts", {})
token_data = CacheableDict("token_data", {})
products_data = CacheableDict("products_data", {})
seller_data = CacheableDict("seller_data", {})
api_tokens = CacheableDict("api_tokens", {})
bills_data = CacheableDict("bills_data", {})
account_types = get_bank_setting("account_types")
debug = None
config = None


def is_admin(ctx):
    return ctx.author.guild_permissions.administrator


def update_cache():
    global bank_accounts, products_data, seller_data, config
    load_bank_accounts()
    load_products_data()
    load_seller_data()
    load_api_tokens()
    load_bills_data()
    config = get_config()


async def updating_cache() -> None:
    while True:
        update_cache()
        if debug:
            print("DEBUG | Updated cache ")
        await asyncio.sleep(10)


def load_modules():
    modules_folder = os.path.join(BASE_DIR, "modules")
    modules = map(lambda a: "modules." + a[:-3], [file for file in os.listdir(modules_folder) if file.endswith('.py')])
    for module in modules:
        try:
            bot.load_extension(module)
        except Exception as e:
            print(f"Exception on loading {module} exception {e}")


class NetherXBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents, test_guilds=[1094023387866726593])
        self.persistent_views_added = False

    async def on_ready(self):
        global bank_accounts, products_data, seller_data, debug, config
        if not self.persistent_views_added:
            self.add_view(BuyItemView())
            self.persistent_views_added = True
        print('''NetherX 2.0 release - Запущен!''')
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
        print('Loading data...')
        config = get_config()
        bank_accounts = load_bank_accounts()
        products_data = load_products_data()
        seller_data = load_seller_data()
        debug = bool(config["debug"])
        print('Data loaded.')
        print("Loading Modules")
        try:
            load_modules()
        except Exception as e:
            print(e)
        print('- NetherX - = - = - = -')
        task: asyncio.Task = asyncio.create_task(updating_cache())
        if debug:
            print("-=-=-=-= Warning -=-=-=-=-=")
            print("NetherX Bot")
            print("Enabled a debug mode")
            print("The bot may be unstable and not suitable for the logic of its use")
        await task


bot = NetherXBot()


@bot.slash_command(name='моя_карта', description='Открывает меню с вашей картой.')
async def my_card(inter: disnake.ApplicationCommandInteraction):
    user_id = str(inter.author.id)
    if user_id in bank_accounts:
        balance = bank_accounts[user_id]["balance"]
        number = format_card_number(bank_accounts[user_id]["card_number"])
        embed = disnake.Embed(title='Меню вашей карты.',
                              description=f'**Баланс:** {balance} алм.\n**Номер:** {number}',
                              color=disnake.Color.red()
                              )
        view = MyCardView()
        await inter.response.send_message(embed=embed, view=view)
    else:
        view = CardView()
        embed = disnake.Embed(title='У вас нету банковской карты.',
                              description=f'Здравствуйте, <@{user_id}>, у вас нету банковской карты. Нажмите кнопку '
                                          f'"Оформить карту", чтобы получить банковскую карту.',
                              color=disnake.Color.red())
        await inter.response.send_message(embed=embed, view=view)


@bot.slash_command(name='купить_премиум', description='Купить премиум за 64 алм.')
async def send_message_channel(ctx, promocode: str):
    premium_price = 64
    if promocode in promocodes:
        sale = promocodes[promocode]
        si = sale / 100
        m = premium_price * si
        premium_price = premium_price - m
        premium_price = int(premium_price)
    user = ctx.author
    user_id = user.id
    role = ctx.guild.get_role(1260352618367160392)
    if str(user_id) in bank_accounts:
        balance = bank_accounts[str(user_id)]["balance"]
        if balance < premium_price:
            await ctx.response.send_message(f'Недостаточно алмазов.', ephemeral=True)
        else:
            if ctx.author.guild.get_role(1260352618367160392) in ctx.author.roles:
                await ctx.response.send_message(f'У вас уже есть премиум.', ephemeral=True)
            else:
                balance -= premium_price
                bank_accounts[str(user_id)]["balance"] = balance
                save_bank_account(str(user_id), bank_accounts[str(user_id)]["username"], balance, bank_accounts[str(user_id)]["card_type"],
                                  bank_accounts[str(user_id)]["card_number"], bank_accounts[str(user_id)]["channel_id"])
                await user.add_roles(role)
                await ctx.response.send_message(f'Вы успешно купили премиум!')
                logs = ctx.guild.get_channel(1094230193234776114)
                await logs.send(f"<@{user_id}> купил премиум.")

    else:
        await ctx.response.send_message(f'Вы не имеете банковского аккаунта!', ephemeral=True)


@bot.slash_command(name="оплатить_счёт")
async def pay_bill(inter: disnake.ApplicationCommandInteraction, bill_number: str):
    bill_name = bills_data[bill_number]["bill_name"]
    amount = bills_data[bill_number]["amount"]

    if bank_accounts[str(inter.author.id)]["balance"] < int(amount):
        await inter.response.send_message("Недостаточно средств на счету.", ephemeral=True)
        return

    message = (f"Вы собираетесь оплатить счёт:\n\n"
               f"**{ bill_name }**\n\n"
               f"На сумму { amount } алмазов.\n"
               f"Пожалуйста, подтвердите оплату.")

    view = PayBillView(bill_number)
    await inter.response.send_message(message, view=view)


@bot.slash_command(name='написать_сообщение')
@commands.has_role(1094231021907623967)
async def send_message_channel(ctx, description: str, title: str, image: str, color: str):
    description = description.replace("\\n", "\n")  # Это заменяет \n на переносы строк
    embed = disnake.Embed(title=title, description=description)

    if image:
        embed.set_image(url=image)
    if color:
        embed.colour = disnake.Colour(int(color.strip('"'), 16))  # Удаляем кавычки и преобразуем hex строку в число

    await ctx.channel.send(embed=embed)


if __name__ == "__main__":
    try:
        bot.run(get_from_config("discord_token"))
    except Exception as e:
        # logs.send(e)
        print(e)
