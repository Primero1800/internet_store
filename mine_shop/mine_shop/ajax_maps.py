from cart.ajax_views import ajax_show_basket_in_header, ajax_show_basket_content
from orders.ajax_views import ajax_orders_view_total, ajax_view_orders
from posts.ajax_views import ajax_show_posts, ajax_show_chosen_product, ajax_show_posts_next
from store.ajax_views import ajax_view_filtered_from_selection, ajax_show_comments, ajax_show_stars_rating
from users.ajax_views import ajax_show_wishcompare_header, ajax_show_wishlist_content, ajax_show_comparison_content

ajax_view_filtered_from_selection_map = {
    'checkboxset': ajax_view_filtered_from_selection,
    'class-ordering-sort': ajax_view_filtered_from_selection,
    'class-paging-count': ajax_view_filtered_from_selection,
    'products-list': ajax_view_filtered_from_selection,
}


ajax_show_basket_header_map = {
    'basket': ajax_show_basket_in_header,
    'basket-content-updater': ajax_show_basket_in_header,
    'add-cart-button*': ajax_show_basket_in_header,
    'remove-cart-button': ajax_show_basket_in_header,
    'add_quantity_cart_button': ajax_show_basket_in_header,

    'basket-content': ajax_show_basket_content,
    'cart-item-quantity-0': ajax_show_basket_content,
    'cart-item-quantity-1': ajax_show_basket_content,
    'remove-cart-button-content': ajax_show_basket_content,
}


ajax_show_wishcompare_header_map = {
    'wishlist-compare-holder': ajax_show_wishcompare_header,
    'wish-compare-holder-updater': ajax_show_wishcompare_header,
    'wish-compare': ajax_show_wishcompare_header,
    'wish-compare*': ajax_show_wishcompare_header,

    'wishlist-main-content': ajax_show_wishlist_content,
    'wishlist-item-delete-*': ajax_show_wishlist_content,

    'comparison-main-content': ajax_show_comparison_content,
    'comparison-item-delete-*': ajax_show_comparison_content,
}

ajax_orders_view_total_map = {
    'total_field': ajax_orders_view_total,
    'delivery_group': ajax_orders_view_total,
    'admin_orders': ajax_view_orders,
    'admin_orders_*': ajax_view_orders,
}

ajax_show_comments_map = {
    'comments': ajax_show_comments,
    'button_add_comment': ajax_show_comments,
    'reviews_item_delete_*': ajax_show_comments,
    'reviews_item_delete_admin_*': ajax_show_comments,

    'stars_rating': ajax_show_stars_rating,
    'stars_row_*': ajax_show_stars_rating,
}

ajax_show_posts_map = {
    'posts': ajax_show_posts,
    'button_add_post': ajax_show_posts,
    'posts_item_delete_*': ajax_show_posts,
    'posts_item_delete_admin_*': ajax_show_posts,

    'posts_next': ajax_show_posts_next,
    'posts_next_*': ajax_show_posts_next,

    'chosen_product': ajax_show_chosen_product,
    'choose_product': ajax_show_chosen_product,

}
