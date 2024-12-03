import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v7xyal4p$tnf+__tltv(p@_9t(a7@ph$(ny49)=_qu62kwgz-1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'django.contrib.postgres',

    'siteajax',
    'phonenumber_field',
    'rest_framework',
    'corsheaders',

    'store.apps.StoreConfig',
    'users.apps.UsersConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'posts.apps.PostsConfig',
    'api.apps.ApiConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'mine_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'store/templates/store')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'mine_shop.context_processors.add_author_to_context',
                'mine_shop.context_processors.add_store_to_context',

                'store.context_processors.add_currency_to_context',                            # 'currency' - Добавляет дескриптор валюты в контекст
                'store.context_processors.add_store_title_to_context',                          # 'store_title' - Добавляет дескриптор главного мени ресурса в контекст
                'cart.context_processors.add_cart_to_context',                                        # 'cart' - Добавляет дескриптор корзины в контекст

            ],
            'libraries': {
                'store_tags_products': 'store.templatetags.templatetags_products',
                'store_tags_brands': 'store.templatetags.templatetags_brands',
                'store_tags_sale_information': 'store.templatetags.templatetags_sale_information',
                'store_tags_rubrics': 'store.templatetags.templatetags_rubrics',
                'store_tags_category_grid_page': 'store.templatetags.templatetags_category_grid_page',
                'store_tags_error_page': 'store.templatetags.templatetags_error_page',
                'store_tags_rating': 'store.templatetags.templatetags_rating',

                'users_tags_members': 'users.templatetags.templatetags_members',

                'cart_tags_cart': 'cart.templatetags.templatetags_cart',

                'orders_tags_phone_numbers': 'orders.templatetags.templatetags_phone_numbers',

                'posts_tags_posts': 'posts.templatetags.templatetags_posts',

                'mine_shop_tags_constants': 'mine_shop.templatetags.templatetags_mine_shop_constants',

            }
        },
    },
]

WSGI_APPLICATION = 'mine_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DB_ENGINE'),
#         'HOST':  os.environ.get("DB_HOST"),
#         'PORT': os.environ.get("DB_PORT"),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'NAME': os.environ.get('DB_NAME'),
#     }
# }

# MAIL SETTINGS

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True if os.environ.get('EMAIL_USE_TLS')=='True' else False
EMAIL_USE_SSL = True if os.environ.get('EMAIL_USE_SSL')=='True' else False
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# CACHE

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.environ.get('REDIS_ADDRESS'),  # Use the appropriate Redis server URL
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 300,
        'OPTIONS':{
            'MAX_ENTRIES': 300,
        }
    }
}

MINE_SHOP_USER_CONFIRMATION_KEY = "user_confirmation_{token}"
MINE_SHOP_USER_CONFIRMATION_TIMEOUT = 300


# Cors API

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api /.*$'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ("ru", "Russian"),
    ("en", "English"),
    ("de", "Deutsch"),
]


SHORT_DATETIME_FORMAT = 'd.m.Y H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
     #BASE_DIR / "static",
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





# USER_DEFAULTS

STORE_TITLE = 'Элементарно!'                                    #      """ Используемое внутреннее главное название проекта"""
CURRENCY = 'BYN'                                                           #       """Используемый дескриптор валюты"""
PRODUCT_NEW_ARRIVALS_COUNT = 25                   #        """Максимальное число продуктов, попадающих в категорию 'Новинки' """
PRODUCT_BESTSELLERS_COUNT = 12                       #       """Максимальное число продуктов, попадающих в категорию "Бестселлеры", должно быть не меньше числа лидеров продаж"""
PRODUCT_TOP_SALES_COUNT = 25                           #       """Максимально число продуктов, попадающих в категорию "Лидеры продаж", должно быть не меньше числа Бестселлеров"""
PRODUCT_TOP_VIEWED_COUNT = 25                       #       """Максимальное число продуктов, попадающих в категорию "Лидеры просмотров" """"
PRODUCT_TOP_RATED_COUNT = 25                          #       """Максимальное число продуктов, попадающих в категорию "Лидеры по рейтингу" """"
PRODUCT_HEROES_COUNT = 5                                   #        """Количество товаров на скидке, попадающих в секцию ГЕРОИ"""

USER_TOOLS_MAX_LENGTH_RECENTLY_VIEWED = 8       #       """Количество товаров, попадающее в категорию пользователя "Недавно просмотренное". Работает по принципу очереди"""
USER_TOOLS_MAX_LENGTH_WISHLIST = 20                       #      """Количество товаров, попадающее в категорию "Избранное". Работает по принципу очереди"""
USER_TOOLS_MAX_LENGTH_COMPARISON = 4                #       """Количество товаров, попадающее в категорию "Сравнение". Работает по принципу очереди"""


SEARCHING_KEYS_FOR_LINKS = [
    {                #   """Ключи поиска для включения ссылки на страницу Доставки"""
        'SEARCHING_KEYS': ('доставка', 'delivery',), 'LINK': {'name': 'доставка', 'url': 'orders:index'}
    },
    {               #   """Ключи поиска для включения ссылки на страницу Оплаты"""
        'SEARCHING_KEYS': ('оплата', 'payment',), 'LINK': {'name': 'оплата', 'url': 'orders:index'}
    },
    {               #   """Ключи поиска для включения ссылки на страницу Аккаунта"""
        'SEARCHING_KEYS': ('аккаунт', 'кабинет', 'личная страница', 'личный кабинет', 'account',), 'LINK': {'name': 'аккаунт', 'url': 'cart:cart'}
    },
    {               #   """Ключи поиска для включения ссылки на страницу Входа/Регистрации"""
        'SEARCHING_KEYS': ('вход', 'регистрация', 'логин', 'лог ин', 'login', 'log in', 'registration',), 'LINK': {'name': 'вход/регистрация', 'url': 'users:login'}
    },
    {               #   """Ключи поиска для включения ссылки на страницу Корзины"""
        'SEARCHING_KEYS': ('корзина', 'заказ', 'заказы',  'cart', 'order',), 'LINK': {'name': 'корзина', 'url': 'cart:cart'}
    },
    {               #   """Ключи поиска для включения ссылки на страницу Заказа"""
        'SEARCHING_KEYS': ('корзина', 'заказ', 'заказы', 'cart', 'order',), 'LINK': {'name': 'заказы', 'url': 'orders:index'}
    },
]

# USERS

AUTH_USER_MODEL = 'users.User'



# CART, PERSON AND ADDRESS

CART_SESSION_ID = 'cart'
PERSON_SESSION_ID = 'person'
ADDRESS_SESSION_ID = 'address'


# GLOBAL_PROJECT_SETTINGS

        # ANONIMOUS -> AUTHENTICATED USER

AFTER_LOGIN_CART_PREFERENCES = [
                    # После авторизации пользователя его корзина из базы данных объединяется с корзиной анонима.
                    # При этом корзина анонима уничтожается. После выхода пользователя аноним получает новую пустую корзину
    '0',            # user.cart = user.cart + anonimous.cart, del anonimous.cart

                     #  После авторизации пользователя его анонимная корзина уничтожается, а работа продолжается с корзиной пользователя
                     # из базы данных. После выхода пользователя аноним получает новую пустую корзину
    '1'             # user.cart = user.cart, del anonimous.cart
]
GLOBAL_CART_PREFERENCES = AFTER_LOGIN_CART_PREFERENCES[0]


ORDERS_FREE_DELIVERY_FLOOR = 300                # Минимальная сумма заказа для бесплатной доставки
ORDERS_DELIVERY_COST = 30                               # Стоимость платной доставки

# Phone number regions allowed

PHONE_NUMBER_DATABASE_SEPARATOR = ' | '
PHONE_NUMBER_DEFAULT_REGION = 'RU'

PHONE_NUMBER_ALOWED_REGIONS = {
    'RU': 'Russia, +7',
    'BY': 'Belarus, +375',
    'KZ':  'Kazakhstan, +7',
    'UZ': 'Uzbekistan, +998',
}

# Telegram_bot

TELEGRAM_SEND_NOTIFICATIONS = True
TELEGRAM_SEND_ORDER_NOTIFICTATION = True
TELEGRAM_SEND_POST_NOTIFICATION = True
TELEGRAM_SEND_VOTE_NOTIFICATION = True

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Used libraries and frameworks

LIBRARIES = [
    'Django', 'Django REST', 'Redis', 'Postgres', 'Siteajax', 'Gettext', 'Babel', 'Phonenumber', 'Whitenoise', 'Pillow',
]



# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'formatters': {
        'django.server': {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        'simple': {
            "()": "django.utils.log.ServerFormatter",
            'format': '[{asctime}]  {levelname} : {message}',
            'datefmt': '%Y.%m.%d %H:%M:%S',
            "style": "{",
        }
    },
    'handlers' : {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': os.path.join(BASE_DIR, 'logging/logs.log'),
            'maxBytes': 1048576,
            'backupCount': 10,
            'formatter': 'simple'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'django.server'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
        },
        'django.server': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
        },
        'django.server': {
            'handlers': ['file', 'django.server'],
            'propagate': False,
        },
    }
}