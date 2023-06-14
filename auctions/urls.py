from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path("toggle_watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path('listing/<int:listing_id>/close', views.close_listing, name='close_listing'),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
]
