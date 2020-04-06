from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_account', views.create_account, name='create_account'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('services', views.services, name='services'),
    path('localities', views.localities, name='localities'),
    path('locality/<slug:title>/', views.single_locality, name='single_locality'),
    path('purchase', views.purchase, name='purchase'),
    path('profile', views.profile, name='profile'),
    path('profile/create-listing', views.create_listing, name='create_listing'),
    path('profile/delete-listing', views.delete_listing, name='delete_listing'),
    path('profile/add-money', views.add_money, name='add_money'),
]
