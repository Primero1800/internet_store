from django import template

from posts.models import Post

register = template.Library()


@register.simple_tag
def add_recent_posted():
    posts = Post.objects.all()

    recent_posted, added = [], []
    for post in posts:
        if post.product and post.product.pk not in added:
            added.append(post.product.pk)
            post_dict = {
                'title': post.product.title,
                'slug': post.product.slug,
                'image_url': post.product.images.first().image.url
            }
            recent_posted.append(post_dict)
            if len(recent_posted) == 5:
                break
    return recent_posted
