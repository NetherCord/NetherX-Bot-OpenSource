import random
import re

from operations.config import get_from_config


def generate_card_number():
    number = ""
    for c in range(16):
        number += str(random.randint(0, 9))
    return number


def format_card_number(card_number):
    if not parse_card_number(card_number):
        return None
    if len(card_number) == 6:
        return card_number
    return card_number[0:4] + '-' + card_number[4:8] + '-' + card_number[8:12] + '-' + card_number[12:16]


def parse_card_number(card_number):
    return re.search(get_from_config("card_validation_regex"), card_number) is not None
