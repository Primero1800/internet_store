from django.urls import path

from store.views import index, ProductDetailView, view_category_grid, show_paginator, view_special_grid, search, error

app_name = 'store'

urlpatterns = [
    path('', index, name="index"),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='detail'),

    path('rubric/<slug:slug>/', view_category_grid, name='rubric'),
    path('rubric/<slug:slug>/<to_filter>', view_category_grid, name='rubric'),
    path('all/', view_category_grid, name='all'),
    path('all/<to_filter>', view_category_grid, name='all'),

    path('search/', search, name='search'),

    path('discont/<int:discont>/', view_special_grid, name='discont'),
    path('popular/<pop>/', view_special_grid, name='popular'),

    path('rubric_pag/', show_paginator, name="show_paginator"),

    path('404/<int:message_id>', error, name='error'),

]
