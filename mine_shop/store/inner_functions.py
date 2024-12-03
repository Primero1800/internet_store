from django.conf import settings

from store.models import Brand, Product

from itertools import permutations


def get_list_of_all_possible_keywords(word):
    words = [word.strip().lower() for word in word.split() if word]
    result = [word for word in words if len(word) > 2]

    for i in range(2, len(words)+1):
        result.extend(' '.join(word) for word in permutations(words, i) if len(' '.join(word))>4 and ' '.join(word) not in result)
    return sorted(result, key=len, reverse=True)

def get_simple_list_of_all_possible_keywords(word):
    words = [word.strip().lower() for word in word.split() if word]
    result = [word for word in words if len(word) > 2]

    while words:
        if len(words) > 1:
            result.append(' '.join(words))
        for i in range(len(words)-1, 1, -1):
            result.append(' '.join(words[:i]))
        words = words[1:]
    return sorted(result, key=len, reverse=True)


def find_products_and_links_by_words(queryset, words):
    """
                1. Поиск в наименованиях товаров:
                    1.1. Вхождение наименования товара в слово.
                    1.2. Вхождение слова длиннее 2-х символов или сочетания слов длиннее 3-x символов в наименование товара
                    1.3.

                2. Поиск в наименованиях Брэндов (вхождение наименования брэнда в слово или слово длинее 2-х символов входит в наименование брэнда)

                3. Поиск в описаниях  товаров (слово длиннее трех символов, вхождение в описание целиком)
    """
    products, ids, ids_count, links = [], [], {}, [],
    queryset_ids = [dset['id'] for dset in queryset]

        ## 1
    for word in words:
        for dprod in queryset:
            title_words = get_simple_list_of_all_possible_keywords(dprod['title'])
            for title_word in title_words:
                if title_word in word or word in title_word:
                    len_match = min(len(title_word), len(word))
                    word_match = min(title_word, word, key=len)
                    if dprod['id'] not in ids:
                        ids.append(dprod['id'])
                        ids_count[dprod['id']] = {}
                        ids_count[dprod['id']]['count'] = len_match
                        ids_count[dprod['id']]['words'] = [word_match]
                    else:
                        if word_match not in ids_count[dprod['id']]['words']:
                            ids_count[dprod['id']] ['count'] += len_match
                            ids_count[dprod['id']]['words'].append(word_match)
                    break

    ids.sort(key=lambda x: ids_count[x]['count'], reverse=True)
    for id in ids:
        products.append(Product.objects.get(id=id))

        ## 2
    for word in words:
        for brand in Brand.objects.all():
            if brand.title.lower() in word or word in brand.title.lower():
                for brand_product in brand.items.all():
                    if brand_product.id in queryset_ids and brand_product.id not in ids:
                        products.append(brand_product)
                        ids.append(brand_product.id)

        ## 3
    for word in words:
        for dprod in queryset:
            if word in dprod['description'].lower() and len(word) > 3:
                if dprod['id'] not in ids:
                    ids.append(dprod['id'])
                    products.append(Product.objects.get(id=dprod['id']))

        for keylink in settings.SEARCHING_KEYS_FOR_LINKS:
            if word in keylink['SEARCHING_KEYS']:
                links.append(keylink['LINK'])

    return products, links