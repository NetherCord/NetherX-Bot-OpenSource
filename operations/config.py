import os

import yaml


BASE_DIR = os.environ["NETHERX_BASE_DIR"]
config_path = os.path.join(BASE_DIR, "configuration", "config.yml")
sql_requests_path = os.path.join(BASE_DIR, "configuration", "sql_requests.yml")
bank_settings_path = os.path.join(BASE_DIR, "configuration", "bank_settings.yml")


def get_config() -> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_bank_settings() -> dict:
    with open(bank_settings_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_from_config(var: str):
    config = get_config()
    return config[var]


def get_db_data():
    return get_from_config("database")


def get_bank_setting(var: str):
    return get_bank_settings()[var]


def get_request_string(var: str):
    with open(sql_requests_path, 'r') as file:
        return yaml.safe_load(file)[var]
