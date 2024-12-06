from orders.models import Person, Address
from orders.session_classes import SessionPerson, SessionAddress
import django.conf



def get_current_person(request):
    user = request.user
    if user.is_authenticated:
        person, _ = Person.objects.get_or_create(user=user)
    else:
        person = SessionPerson(request)
    return person


def get_current_address(request):
    user = request.user
    if user.is_authenticated:
        address, _ = Address.objects.get_or_create(user=user)
    else:
        address = SessionAddress(request)
    return address


def get_complex_phonenumber(country_code='RU', phone_number=''):
    if phone_number:
        phone_number = [symbol for symbol in phone_number if symbol.isdigit()]
        parts = []
        parts.append(''.join(phone_number[:3]))
        parts.append(''.join(phone_number[3:6]))
        for i in range(6, len(phone_number), 2):
            d = 0
            if len(phone_number) - i == 3:
                d = 1
            parts.append(''.join(phone_number[i: i+2+d]))
            if d: break
        phone_number = '-'.join(parts)

    phone_numbers_regions = django.conf.settings.PHONE_NUMBER_ALOWED_REGIONS
    phone_number_prefix = [value for key, value in phone_numbers_regions.items() if key==country_code][0]
    separator = django.conf.settings.PHONE_NUMBER_DATABASE_SEPARATOR
    return separator.join((country_code, phone_number_prefix, phone_number))


def _separator_normalize(value):
    value = value.replace(',', '.')
    return value


