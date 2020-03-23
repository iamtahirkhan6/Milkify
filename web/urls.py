from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_account', views.create_account, name='create_account'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('localities', views.localities, name='localities'),
    path('locality/<slug:title>/', views.single_locality, name='single_locality'),
    path('services', views.services, name='services'),
]
