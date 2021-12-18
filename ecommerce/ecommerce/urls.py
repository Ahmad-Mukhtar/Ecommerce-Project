from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='HomePage'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('search', views.search, name='search'),
    path('DashBoard', views.userpanel, name='DashBoard'),
    path('logout', views.logout, name='logout'),
    path('UpdateProfile',views.UpdateCustomerProfile,name='UpdateProfile'),
    path('Addtocart', views.Addtocart, name='Addtocart'),
    path('DeleteAccount', views.DeleteAccount, name='DeleteAccount'),



]
