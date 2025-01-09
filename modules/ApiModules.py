import base64
import threading
from time import time
from typing import Optional

import disnake
import uvicorn
from disnake.ext import commands
from fastapi import FastAPI, HTTPException, Depends, Header

from cacher import CacheableDict
from operations import config
from operations.bills import generate_bill_number
from operations.config import get_from_config
from operations.db import save_api_tokens, load_api_tokens, save_bills_data
from operations.vigenere import encrypt_text

bank_accounts = CacheableDict("bank_accounts", {}, True)
api_tokens = CacheableDict("api_tokens", {})
bills_data = CacheableDict("bills_data", {})


class ApiModules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = FastAPI()
        self.config_section = config.get_from_config("api")

        def verify_token(token: Optional[str] = Header(None)):
            if token is None:
                raise HTTPException(status_code=401, detail="Authorization header missing")

            if token not in api_tokens.keys():
                raise HTTPException(status_code=403, detail="Invalid token")

            return token

        @self.app.get("/bill/create")
        async def create_bill(amount: int, bill_name: str = None, token: str = Depends(verify_token)):
            card_to = api_tokens[token]["card_number"]
            bill_number = generate_bill_number()
            bill_name = bill_name or f"Оплата счёта { bill_number }"
            save_bills_data(bill_number, bill_name, str(amount), card_to, 0)
            return {"bill_number": bill_number}

        @self.app.get("/bill/paid")
        async def get_bill(bill_number: int, token: str = Depends(verify_token)):
            return {"paid": bills_data[bill_number]}

        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()

    @staticmethod
    def _encrypt_code(author_id, author_name):
        string = str(author_id) + str(author_name)
        string.replace("_", "UD")
        string.replace("-", "PD")
        return encrypt_text(string, get_from_config("vigenere_key"))

    def run_server(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.config_section["port"])

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"started {self.config_section['port']}")

    @commands.slash_command(name="получить_api_токен", description="Сгенерировать и получить API токен.")
    async def get_api_token(self, inter: disnake.ApplicationCommandInteraction):
        global api_tokens
        author_id = inter.author.id
        author_name = inter.author.name
        author_avatar = inter.author.avatar
        api_token = ApiModules._encrypt_code(author_id, author_name)
        save_api_tokens(api_token, str(author_id), bank_accounts[str(author_id)]["card_number"])
        api_tokens = load_api_tokens()
        await inter.author.send(f"Ваш API код: ```{api_token}```")
        await inter.send("Ваш токен сгенерирован и отправлен вам в ЛС.", ephemeral=True)


def setup(bot):
    bot.add_cog(ApiModules(bot))
