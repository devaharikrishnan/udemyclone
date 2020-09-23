from django.urls import path
from .views import *
from accounts import views
app_name = 'udemy'

urlpatterns = [
	path('', index, name='index'),
	path('login', views.LoginView.as_view(), name='login'),
    path('home', HomeListView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),

]
