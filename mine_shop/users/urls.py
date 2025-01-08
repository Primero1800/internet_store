from django.urls import path
from users.views import RegisterView, registration_confirm, login, logout, restore_password, wishlist, comparison

app_name = 'users'

urlpatterns = [
    path('registration/', RegisterView.as_view(), name="registration"),
    path('registration_confirm/<token>', registration_confirm, name="registration_confirm"),

    path('login/<message>/<email>/<next>/', login, name='login'),
    path('login/<message>/<email>/', login, name='login'),
    path('login/', login, name='login'),

    path('logout/', logout, name='logout'),
    path('restore_password/', restore_password, name='restore_password'),
    path('wishlist/', wishlist, name='wishlist'),
    path('comparison/', comparison, name='comparison'),

]
