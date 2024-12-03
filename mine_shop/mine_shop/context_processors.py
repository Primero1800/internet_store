from dotenv import load_dotenv
load_dotenv()
import os
from django.conf import settings


def add_author_to_context(request):
    return {
        'author':  {
            'email': os.environ.get('AUTHOR_EMAIL'),
            'github': os.environ.get('AUTHOR_GITHUB'),
            'tg': os.environ.get('AUTHOR_TG'),
            'vk': os.environ.get('AUTHOR_VK'),
        },
        'tech': settings.LIBRARIES
    }

def add_store_to_context(request):
    return {
        'store': {
            'email': os.environ.get('STORE_EMAIL'),
            'address': os.environ.get('STORE_ADDRESS'),
            'phonenumber': os.environ.get('STORE_PHONENUMBER'),
        },
    }