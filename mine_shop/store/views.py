from django.conf import settings
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from siteajax.decorators import ajax_dispatch

from mine_shop.ajax_maps import ajax_show_basket_header_map, ajax_show_wishcompare_header_map, \
    ajax_view_filtered_from_selection_map, ajax_show_comments_map
from store.info_classes import Sale_information
from store.inner_functions import find_products_and_links_by_words, get_simple_list_of_all_possible_keywords

from store.models import Product, Rubric
from users.models import UserTools


@method_decorator(
    ajax_dispatch(
        ajax_show_basket_header_map | ajax_show_wishcompare_header_map | ajax_show_comments_map,
    ),
    name='dispatch'
)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/single_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = kwargs['object']

        sale_information, _ = Sale_information.objects.get_or_create(product=product)
        sale_information.view()

        user = self.request.user
        if user and user.is_authenticated:
            user_tools, _ = UserTools.objects.get_or_create(user=user)
            user_tools.add_rv(product)

        return context


@ajax_dispatch(ajax_view_filtered_from_selection_map | ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def view_category_grid(request, slug=None, to_filter=None):
    context = {}
    try:
        rubric = get_object_or_404(Rubric, slug=slug)
        context['rubric'] = rubric
        page_title = rubric.title
        products = rubric.products.all()
    except Exception:
        products = Product.objects.all()
        page_title = _("Все товары")

    if to_filter:
        if to_filter == 'd':
            products = products.filter(discont__gte=5)
            page_title += _(". На скидке")
        elif to_filter == 'n':
            from store.templatetags.templatetags_products import add_new_arrivals_to_context
            nids = add_new_arrivals_to_context()['ids']
            products = products.filter(id__in=nids)
            page_title += _(". Новинки")
    context['products'] = products
    context['page_title'] = page_title
    return render(request, "store/category-grid.html", context=context)


@ajax_dispatch(ajax_view_filtered_from_selection_map | ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def view_special_grid(request, discont=5, pop=None):
    context = {}
    if not pop:
        title = _("Скидка") if discont == 5 else _("Скидка более ") + str(discont) + '%'
        products = Product.objects.filter(discont__gte=discont)
        context['is_discont_page'] = True
    else:
        if pop == 's' or pop == 'b':
            products = Sale_information.objects.all().order_by('-sold_count')[:settings.PRODUCT_TOP_SALES_COUNT]
            products = [top.product for top in products]
            if pop == 'b':
                products = products[:settings.PRODUCT_BESTSELLERS_COUNT]
                title = _("Бестселлеры")
            else:
                title = _("Лидеры продаж")
        elif pop == 'r':
            products = list(Product.objects.order_by('rating')[:settings.PRODUCT_TOP_RATED_COUNT])
            title = _("Лидеры рейтинга")
        else:  # pop == 'v'
            products = [top.product for top in Sale_information.objects.all().order_by('-viewed_count')[:settings.PRODUCT_TOP_VIEWED_COUNT]]
            title = _("Лидеры просмотров")

    context['products'] = products
    context['discont'] = {'title': title}
    return render(request, "store/category-grid.html", context=context)


@ajax_dispatch(ajax_view_filtered_from_selection_map | ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def search(request):
    if request.method == 'POST':
        params = dict(request.POST)
    else:
        params = dict(request.GET)
    try:
        keyword = ' '.join(params['search-field'][0].split())[:30]
        keyrubric = params['category-field'][0].lower()
    except Exception:
        if 'HTTP_REFERER' in request.META:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return redirect(to=reverse('store:index'))

    import re
    keyword = re.sub(r'[^\w\s]', '', keyword).strip()
    keywords = get_simple_list_of_all_possible_keywords(keyword)

    queryset = None
    for rubric in Rubric.objects.all():
        if keyrubric == rubric.title.lower():
            queryset = rubric.products.all().values('title', 'description', 'id')
            break
    if not queryset:  # 'все категории':
        queryset = Product.objects.all().values('title', 'description', 'id')

    products, links = find_products_and_links_by_words(queryset, keywords)
    context = {}
    context['products'] = products
    context['page_title'] = _("Поиск")
    context['search'] = {}
    context['search']['keyword'] = keyword
    context['search']['keyrubric'] = keyrubric
    context['search']['links'] = links

    return render(request, "store/category-grid.html", context=context)


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def index(request):
    context = {}
    response = render(request, "store/index.html", context)
    return response


def show_paginator(request):
    if request.method == "GET":
        params = dict(request.GET)
    else:
        params = dict(request.POST)
    per_page = int(params['per_page'][0])
    current_page = int(params['current_page'][0])
    tab = params['tab'][0]
    if tab == '0':
        try:
            current_page += int(params['next_page'][0])
        except Exception:
            pass

    pages_count = int(params['pages_count'][0])
    try:
        filtered_products_ids = params['filtered_products']
    except Exception:
        filtered_products_ids = []
    page_ids = filtered_products_ids[(current_page-1)*per_page: current_page*per_page]
    first_index = (current_page-1)*per_page+1
    last_index = min(current_page*per_page, len(filtered_products_ids))

    filtered_products = [Product.objects.get(id=int(id)) for id in page_ids]

    context = {'filtered_products': filtered_products, 'current_page': current_page, 'pages_count': pages_count,
                        'all_filtered_products_count': len(filtered_products_ids), 'indices': (first_index, last_index)}

    template = 'grid' if tab == '0' else 'list'

    response = render(request, f'store/ajax_divs/ajax_div_{template}_tab.html', context)
    return response


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def error(request, message_id=None):
    context = {'message': message_id, 'title': _("Ошибка")}
    return render(request, 'store/404.html', context)
