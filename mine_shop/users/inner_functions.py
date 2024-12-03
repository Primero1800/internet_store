import string
import random

PASSWORD_SET = string.ascii_letters + string.digits
PASSWORD_LENGTH = 8



def generate_password():
    return ''.join(random.choice(PASSWORD_SET) for i in range(PASSWORD_LENGTH))


def get_products_by_tool_items(tool_items):
    return [item.product for item in tool_items]