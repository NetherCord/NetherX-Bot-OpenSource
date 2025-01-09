import disnake
import mysql.connector

from cacher import CacheableDict
from operations.config import get_db_data, get_request_string


def connectable(func):
    def wrapper(*args, **kwargs):
        db_data = get_db_data()
        connection = mysql.connector.connect(
            host=db_data["host"],
            user=db_data["user"],
            password=db_data["password"],
            database=db_data["database"]
        )
        result = func(connection, *args, **kwargs)
        connection.close()
        return result
    return wrapper


@connectable
def load_bank_accounts(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_request_string("load_bank_accounts"))
    bank_accounts = CacheableDict("bank_accounts", {row['user_id']: row for row in cursor.fetchall()})
    return bank_accounts


@connectable
def load_products_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_request_string("load_products_data"))
    products_data = CacheableDict("products_data", {row['product_quantity']: row for row in cursor.fetchall()})
    return products_data


@connectable
def load_seller_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_request_string("load_seller_data"))
    seller_data = CacheableDict("seller_data", {row['seller_id']: row for row in cursor.fetchall()})
    return seller_data


@connectable
def load_api_tokens(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_request_string("load_api_tokens"))
    api_tokens = CacheableDict("api_tokens", {row['api_token']: row for row in cursor.fetchall()})
    return api_tokens


@connectable
def load_bills_data(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(get_request_string("load_bills_data"))
    bills_data = CacheableDict("bills_data", {row['bill_number']: row for row in cursor.fetchall()})
    return bills_data


@connectable
def save_bank_account(connection, user_id, username, balance, card_type, card_number, channel_id):
    if isinstance(user_id, disnake.User):
        member = user_id
        user_id = str(member.id)
    cursor = connection.cursor()
    cursor.execute(get_request_string("save_bank_account") % (user_id, username, balance, card_type, card_number, channel_id))
    connection.commit()


@connectable
def save_product(connection, product_quantity, author_id, product_name, price, description, link_to_image):
    if isinstance(author_id, disnake.Member):
        member = author_id
        user_id = member.id
    cursor = connection.cursor()
    cursor.execute(get_request_string("save_product") % (product_quantity, author_id, product_name, price, description, link_to_image))
    connection.commit()


@connectable
def save_seller_data(connection, seller_id, income, revenue, total_revenue):
    if isinstance(seller_id, disnake.Member):
        member = seller_id
        user_id = member.id
    cursor = connection.cursor()
    cursor.execute(get_request_string("save_seller_data") % (seller_id, income, revenue, total_revenue))
    connection.commit()


@connectable
def save_api_tokens(connection, api_token, user_id, card_number):
    cursor = connection.cursor()
    cursor.execute(get_request_string("save_api_tokens") % (api_token, user_id, card_number))
    connection.commit()


@connectable
def save_bills_data(connection, bill_number, bill_name, amount, card_to, paid):
    cursor = connection.cursor()
    cursor.execute(get_request_string("save_bills_data") % (bill_number, bill_name, amount, card_to, paid))
    connection.commit()


@connectable
def get_id_by_card_number(connection, card_number):
    cursor = connection.cursor()
    cursor.execute(get_request_string("get_id_by_card_number") % card_number)
    result = cursor.fetchone()
    return result
