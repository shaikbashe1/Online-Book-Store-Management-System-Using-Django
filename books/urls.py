from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<str:book_id>/', views.book_detail, name='book_detail'),
    path('category/<str:category_id>/', views.category_books, name='category_books'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<str:book_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<str:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    # Auth URLs
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
