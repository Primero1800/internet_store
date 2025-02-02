from django.shortcuts import render, get_object_or_404
from siteajax.toolbox import AjaxResponse

from orders.inner_functions import get_current_person, get_current_address
from posts.inner_functions import correct_by_word_length
from store.forms import VoteForm
from store.info_classes import Vote
from store.models import Product


def ajax_view_filtered_from_selection(request, *args, **kwargs):
    context = {}
    grid_active = True
    if request.method == "POST":
        params = dict(request.POST)
    else:
        params = dict(request.GET)

    try:
        product_ids = params['product_ids']
        rubric_products = [Product.objects.get(id=int(id)) for id in product_ids]
        rubric_brands = sorted(set(prod.brand.title for prod in rubric_products))
    except Exception:
        product_ids, rubric_products, rubric_brands = [], [], []
    per_page = 6

    if not request.ajax.source.id == 'products-list':
        filter_statuses = params['checkbox_statuses']
        checkboxes_count = int(filter_statuses.pop(0))
        checkbox_statuses = filter_statuses[:checkboxes_count]

        current_tab_pane = filter_statuses.pop()
        paging_status = filter_statuses.pop()
        ordering_status = filter_statuses.pop()

        for filter, brand_title in zip(checkbox_statuses, rubric_brands):
            if filter == 'false':
                rubric_products = [prod for prod in rubric_products if prod.brand.title != brand_title]

        if ordering_status == '3':
            rubric_products.sort(key=lambda x: x.rating, reverse=True)
        elif ordering_status == '2':
            rubric_products.sort(key=lambda x: x.price)
        elif ordering_status == '1':
            rubric_products.sort(key=lambda x: x.id, reverse=True)

        if paging_status == '1':
            per_page = 12
        elif paging_status == '2':
            per_page = 24

        grid_active = True if 'active' in str(current_tab_pane) else False

    context['div_filtered_products'] = [rubric_product.id for rubric_product in rubric_products]
    context['div_current_page'] = 1
    context['div_per_page'] = per_page
    context['pages_count'] = len(context['div_filtered_products'])//per_page if len(context['div_filtered_products']) % per_page == 0 else len(context['div_filtered_products'])//per_page+1

    context['grid_active'] = grid_active

    response = AjaxResponse(render(request, 'store/ajax_divs/ajax_div_category_grid.html', context=context))
    return response


def ajax_show_stars_rating(request, *args, **kwargs):
    context = {'new_vote': 5}
    if 'new_vote' in request.POST:
        context['new_vote'] = int(request.POST['new_vote'])

    response = AjaxResponse(render(request, 'store/ajax_divs/ajax_div_stars_rating.html', context=context))
    return response


def ajax_show_comments(request, *args, **kwargs):
    context = {}
    user = request.user
    product = Product.objects.get(slug=kwargs['slug'])
    context['product'] = product

    if request.ajax.source.id.startswith('reviews_item_delete'):
        vote_id = int(request.POST['vote_id'])
        vote = get_object_or_404(Vote, id=vote_id)
        if user == vote.user or user.is_staff or user.is_superuser:
            # vote.del_vote()
            vote.delete()

    context['stars'] = 5
    if 'stars' in request.POST:
        context['stars'] = int(request.POST['stars'])

    if user.is_authenticated:
        try:
            votes = product.votes.get(user=user)
            if votes:
                context['voted'] = True
        except Exception:
            pass

    if 'voted' not in context and user.is_authenticated:
        if 'name' and 'stars' in request.POST:
            form = VoteForm(data=request.POST)
            if form.is_valid():
                data = form.cleaned_data
                vote = Vote(
                    user=user,
                    product=product,
                    name=data['name'],
                    stars=int(data['stars']),
                    review=correct_by_word_length(data['review'], 70),
                )
                vote.save()
                vote.vote()
                context['voted'] = True
        else:
            person = get_current_person(request)
            address = get_current_address(request)
            name = person.get_fullname()
            data = {
                'name': name,
                'email': address.email,
                'stars': 5,
                'review': None,
            }
            form = VoteForm(data=data)
        context['form'] = form

    response = AjaxResponse(render(request, 'store/ajax_divs/ajax_div_comments.html', context=context))
    return response
