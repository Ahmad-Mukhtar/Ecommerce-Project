from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

# ALL the urls/Routin Paths are Stored in this Module
urlpatterns = [
    path('', views.homepage, name='HomePage'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('search', views.search, name='search'),
    path('DashBoard', views.userpanel, name='DashBoard'),
    path('logout', views.logout, name='logout'),
    path('UpdateProfile', views.UpdateCustomerProfile, name='UpdateProfile'),
    path('Addtocart', views.Addtocart, name='Addtocart'),
    path('DeleteAccount', views.DeleteAccount, name='DeleteAccount'),
    path('Categories', views.Categories, name='Categories'),
    path('Cart', views.Cart, name='Cart'),
    path('removefromcart', views.removefromcart, name='removefromcart'),
    path('searchedcategory', views.searchbycategory, name='searchedcategory'),
    path('searchinpanel', views.searchinpanel, name='searchinpanel'),
    path('AdvancedSearch', views.AdvancedSearch, name='AdvancedSearch'),
    path('checkout', views.checkout, name='checkout'),
    path('manageorders', views.manageorders, name='manageorders'),
    path('cancelorder', views.cancelorder, name='cancelorder'),
    path('addeditreview', views.addeditreview, name='addeditreview'),
    path('BuyProduct', views.BuyProduct, name='BuyProduct'),
    path('BuyProductCheckout', views.BuyProductCheckout, name='BuyProductCheckout'),

    # Integrated Paths Starts From here

    path('SEllerDashBoard', views.sellerpanel, name='SEllerDashBoard'),
    path('UpdateSellerProfile', views.UpdateSellerProfile, name='UpdateSellerProfile'),
    path('UpdateAdminProfile', views.UpdateAdminProfile, name='UpdateAdminProfile'),
    path('UpdateSuperAdmin', views.updateSuperAdminProfile, name='UpdateSuperAdmin'),
    path('DeleteSellerAccount', views.DeleteSellerAccount, name='DeleteSellerAccount'),
    path('addProduct', views.addProduct, name='addProduct'),
    path('updateProduct', views.updateProduct, name='updateProduct'),
    path('RemoveProduct', views.RemoveProduct, name='RemoveProduct'),
    path('SuperAdminDashboard', views.SuperAdminPanel, name='SuperAdminDashboard'),
    path('AddAdmin', views.addAdmin, name='AddAdmin'),
    path('RemoveAdmin', views.removeAdmin, name='RemoveAdmin'),
    path('banuser', views.ban_user, name='banuser'),
    path('banseller', views.ban_seller, name='banseller'),
    path('bancustomer', views.ban_customer, name='bancustomer'),
    path('unbanuser', views.unban_user, name='unbanuser'),
    path('unbanseller', views.unban_seller, name='unbanseller'),
    path('unbancustomer', views.unban_customer, name='unbancustomer'),
    path('manage_order_superadmin', views.manage_order_superadmin, name='manage_order_superadmin'),
    path('Update_order_status', views.update_order, name='Update_order_status')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
