from django.utils.datastructures import MultiValueDict
from django.utils.text import slugify

ALPHABET = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
    'я': 'ya', '-': '-',
}

ENGLISH = 'abcdefghijklmnopqrstuvwxyz'


def sym_cyr2lat(sym):
    if sym.isdigit() or sym in ENGLISH:
        return sym
    if sym not in ALPHABET:
        return '_'
    return ALPHABET[sym]


def cyr_to_lat(text):
    return ''.join(sym_cyr2lat(sym) for sym in text.lower())


def data_slugification(serializer):
    initial_data = MultiValueDict(serializer.initial_data)
    if 'title' in serializer.context['request'].POST:
        initial_data['slug'] = cyr_to_lat(slugify(serializer.context['request'].POST['title'], allow_unicode=True))
    else:
        if 'slug' in initial_data:
            del initial_data['slug']
    return initial_data


def filters(queryset, count, sort_by, x_filters_mapping, other, dict_mapping=None):
    data = None
    for case, value in x_filters_mapping.items():
        if sort_by == case:
            data = sorted(queryset, key=lambda x: x[value], reverse=True) if value else queryset
            break
    else:
        if dict_mapping:
            for case, value in dict_mapping.items():
                if sort_by == case:
                    def func(x):
                        return x[case][value] if value else sum(len(v) for v in x[case].values())
                    data = sorted(queryset, key=func, reverse=True)
                    break
    if not data:
        data = sorted(queryset, key=lambda x: x[other], reverse=True) if other else queryset

    if count:
        try:
            count = int(count)
            if count != 0:
                data = data[:count] if count > 0 else reversed(data[count:])
        except Exception:
            pass
    elif sort_by:
        try:
            sort_by = int(sort_by)
            if sort_by != 0:
                data = data[:sort_by] if sort_by > 0 else reversed(data[sort_by:])
        except Exception:
            pass

    return data
