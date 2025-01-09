import random

from cacher import CacheableDict

bills_data = CacheableDict("bills_data", {}, True)


def generate_bill_number():
    number = str(random.randint(1000000, 9999999))
    while number in bills_data:
        number = str(random.randint(1000000, 9999999))
    return number
