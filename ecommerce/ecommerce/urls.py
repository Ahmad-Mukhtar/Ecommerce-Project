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
    path('Categories', views.Categories, name='Categories'),
    path('Cart', views.Cart, name='Cart'),
    path('removefromcart', views.removefromcart, name='removefromcart'),
    path('searchedcategory',views.searchbycategory,name='searchedcategory'),
    path('searchinpanel',views.searchinpanel,name='searchinpanel'),
    path('AdvancedSearch', views.AdvancedSearch, name='AdvancedSearch'),
    path('checkout', views.checkout, name='checkout'),
    path('manageorders', views.manageorders, name='manageorders'),
    path('cancelorder', views.cancelorder, name='cancelorder'),
    path('addeditreview', views.addeditreview, name='addeditreview'),

]
