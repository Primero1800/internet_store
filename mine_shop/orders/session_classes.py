from django.conf import settings
import json


class SessionPerson(object):

    def __init__(self, request):

        """Инициализация данных покупателя для оформления заказа"""
        self.session = request.session
        person = self.session.get(settings.PERSON_SESSION_ID)
        if not person:
            person = self.session[settings.PERSON_SESSION_ID] = {}
        self.person = person

    def set_attributes(self, name=None, surname=None, company_name=None):
        self.person['name'] = name
        self.person['surname'] = surname
        self.person['company_name'] = company_name
        self.save()

    def get_fullname(self):
        return (self.person['name'] + ' ' + self.person['surname']).strip()

    def to_form(self):
        name = self.person['name'] if 'name' in self.person else None
        surname = self.person['surname'] if 'surname' in self.person else None
        company_name = self.person['company_name'] if 'company_name' in self.person else None
        return {'name': name, 'surname': surname, 'company_name': company_name}

    def serialize(self):
        to_serialize = {
            'name': self.person['name'],
            'surname': self.person['surname'],
            'company_name': self.person['company_name']
        }
        return json.dumps(to_serialize)


    def save(self):
        self.session[settings.PERSON_SESSION_ID] = self.person
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True


    def clear(self):
        "Удаление данных персоны из сессии"
        del self.session[settings.PERSON_SESSION_ID]
        self.session.modified = True


class SessionAddress(object):

    def __init__(self, request):

        """Инициализация данных покупателя для оформления заказа"""
        self.session = request.session
        address = self.session.get(settings.ADDRESS_SESSION_ID)
        if not address:
            address = self.session[settings.ADDRESS_SESSION_ID] = {}
        self.address = address


    def set_attributes(self, address=None, city=None, postcode=None, email=None, phonenumber=None):
        self.address['address'] = address
        self.address['city'] = city
        self.address['postcode'] = postcode
        self.address['email'] = email
        self.address['phonenumber'] = phonenumber
        self.save()

    def get_phonenumber(self):
        return self.address['phonenumber']

    def to_form(self):
        address = self.address['address'] if 'address' in self.address else None
        city = self.address['city'] if 'city' in self.address else None
        postcode = self.address['postcode'] if 'postcode' in self.address else 0
        email = self.address['email'] if 'email' in self.address else None
        phonenumber_0, phonenumber_1 = None, None
        if 'phonenumber' in self.address:
            separator = settings.PHONE_NUMBER_DATABASE_SEPARATOR
            phonenumber = self.address['phonenumber'].split(separator)
            phonenumber_0 = phonenumber[0]
            phonenumber_1 = phonenumber[-1]

        return {'address': address, 'city': city, 'postcode': postcode, 'email': email, 'phonenumber_0': phonenumber_0, 'phonenumber_1': phonenumber_1}


    def serialize(self):
        to_serialize = {
            'address': self.address['address'],
            'city': self.address['city'],
            'postcode': self.address['postcode'],
            'email': self.address['email'],
            'phonenumber': self.address['phonenumber']
        }
        return json.dumps(to_serialize)


    def save(self):
        self.session[settings.ADDRESS_SESSION_ID] = self.address
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True


    def clear(self):
        "Удаление данных персоны из сессии"
        del self.session[settings.ADDRESS_SESSION_ID]
        self.session.modified = True


