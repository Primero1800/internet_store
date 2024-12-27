from django.utils.datastructures import MultiValueDict

SWAGGER_EMPTIES = [[''], '']

def _parse_list(data):
    _temp = data[0].split(',')
    if len(_temp) > 1:
        return _temp
    return data


def swagger_initial_rubrics(initial_data: MultiValueDict):
    if 'products' in initial_data:
        products_list = initial_data.getlist('products')
        if len(products_list) > 1:
            return initial_data
        initial_data.setlist('products', _parse_list(products_list))
    return initial_data

