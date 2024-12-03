from django.shortcuts import render, get_object_or_404
from siteajax.utils import AjaxResponse

import asyncio
import telegram

from orders.inner_functions import get_current_person, get_current_address
from posts.forms import PostForm
from posts.inner_functions import correct_by_word_length, get_product_by_link, get_product_by_title, \
    send_telegram_message
from posts.models import Post
from store.models import Product

POSTS_PER_PAGE = 10


def ajax_show_posts(request, *args, **kwargs):
    context = {}
    user = request.user

    if request.ajax.source.id.startswith('posts_item_delete'):
        post_id = int(request.POST['post_id'])
        post = get_object_or_404(Post, id=post_id)
        if user == post.user or user.is_staff or user.is_superuser:
            post.delete()

    if user.is_authenticated:
        if 'name' and 'review' in request.POST:
            form = PostForm(data=request.POST)
            if form.is_valid():
                data = form.cleaned_data
                product = None
                if 'product_id' in request.POST and request.POST['product_id']:
                    product = get_object_or_404(Product, id=int(request.POST['product_id']))
                post = Post(
                    name=data['name'],
                    product=product,
                    user=user,
                    review=correct_by_word_length(data['review'], 60)
                )
                context['posted'] = True
                post.save()
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
            form = PostForm(data=data)

        context['form'] = form

    posts_count = len(Post.objects.all())
    context['posts_count'] = posts_count

    response = AjaxResponse(render(request, 'posts/ajax_divs/ajax_div_posts.html', context=context))
    return response


def ajax_show_posts_next(request, *args, **kwargs):
    context = {}

    all_posts = Post.objects.all()
    last_post_id = all_posts.first().id + 1 if 'last_post_id' not in request.POST else request.POST['last_post_id']
    posts = all_posts.filter(id__lt=last_post_id)
    if len(posts) > POSTS_PER_PAGE:
        context['has_next'] = True
        posts = posts[:POSTS_PER_PAGE]

    if posts:
        context['last_post_id'] = list(posts)[-1].pk

    list_posts = []
    for post in posts:
        post_dict = {
            'name': post.name,
            'time_published': post.time_published,
            'review': post.review,
            'user': post.user,
            'id': post.pk
        }
        product = post.product
        if product:
            post_dict['product'] = {
                'title': product.title,
                'image': product.images.first().image.url,
                'slug': product.slug,
                'rating': product.rating,
                'get_rating_display': product.get_rating_display(),
                'id': product.pk,
            }
        list_posts.append(post_dict)
    context['posts'] = list_posts

    response = AjaxResponse(render(request, 'posts/ajax_divs/ajax_div_posts_page.html', context=context))
    return response

def ajax_show_chosen_product(request, *args, **kwargs):
    context = {}

    if request.ajax.source.id == "choose_product":
        raw_chosen_product = request.POST['raw_chosen_product']
        product = get_product_by_link(raw_chosen_product)
        if not product:
            product = get_product_by_title(raw_chosen_product)

        if not product:
            context['not_found'] = True
        else:
            chosen_product = {
                'title': product.title,
                'image': product.images.first().image.url,
                'slug': product.slug,
                'rating': product.rating,
                'get_rating_display': product.get_rating_display(),
                'id': product.pk,
            }
            context['chosen_product'] = chosen_product

    response = AjaxResponse(render(request, 'posts/ajax_divs/ajax_div_chosen_product.html', context=context))
    return response