import os.path
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .Classes import DAL
from .Classes.Button import Btn
from .forms import CHOICES


# This module shows the views of different pages

def homepage(request):
    DL = DAL.Dal()
    All_products = DL.getAllProducts()
    DL.CloseConnection()
    return render(request, 'HomePage.html', {'allproducts': All_products, 'searchresults': "Featured Products"})


def search(request):
    DL = DAL.Dal()
    All_products = DL.getAllProducts()
    search_value = request.GET['searchfield']
    All_products = [x for x in All_products if x.prodname.find(search_value) != -1]
    search_result = "Search Results"
    if len(All_products) == 0:
        search_result = "No Results Found"
    DL.CloseConnection()
    return render(request, 'HomePage.html', {'allproducts': All_products, 'searchresults': search_result})


def searchinpanel(request):
    if 'user' in request.session:
        DL = DAL.Dal()
        All_products = DL.getAllProducts()
        search_value = request.GET['searchbox']
        All_products = [x for x in All_products if x.prodname.find(search_value) != -1]
        search_result = "Search Results"
        if len(All_products) == 0:
            search_result = "No Results Found"
        items_count = DL.getCartitemslength(int(request.session['user']))
        messages.success(request, str(items_count))

        DL.CloseConnection()
        return render(request, 'Customer\Panel.html', {'allproducts': All_products, 'SearchValue': search_result})
    else:
        return redirect("login")


def AdvancedSearch(request):
    if 'user' in request.session:
        if request.method == 'POST':
            filtered_products = []
            all_letters = request.POST['Allletters']
            exact_letters = request.POST['exactletters']
            any_letters = request.POST['anyletter']
            DL = DAL.Dal()
            All_products = DL.getAllProducts()
            if any_letters == '':
                any_letters = "#"
            if exact_letters == '':
                exact_letters = "#"
            if all_letters == '':
                all_letters = "#"
            for product in All_products:
                print(exact_letters, product.prodname)
                if product.prodname.lower().find(
                        any_letters.lower()) != -1 or product.prodname.lower() == exact_letters.lower():
                    filtered_products.append(product)

                else:
                    for letter in all_letters:
                        if letter.lower() in product.prodname.lower():
                            filtered_products.append(product)
                            break
            search_result = "Search Results"
            if len(All_products) == 0:
                search_result = "No Results Found"
            items_count = DL.getCartitemslength(int(request.session['user']))
            messages.success(request, str(items_count))
            DL.CloseConnection()
            return render(request, 'Customer\Panel.html',
                          {'allproducts': filtered_products, 'SearchValue': search_result})
        else:
            return render(request, 'Customer/advancedSearch.html')
    else:
        return redirect('login')


def searchbycategory(request):
    if 'user' in request.session:
        val = request.COOKIES.get('catcookie', 'default')
        Dl = DAL.Dal()
        result = []
        if val != 'default':
            result = Dl.getAllProducts()
            result = [x for x in result if x.category.find(val) != -1]
            items_count = Dl.getCartitemslength(int(request.session['user']))
            messages.success(request, str(items_count))
            Dl.CloseConnection()
        else:
            print("Failed")
        return render(request, 'Customer\Panel.html', {'allproducts': result, 'SearchValue': val})
    else:
        return redirect('login')


def login(request):
    form = CHOICES(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_type = form.cleaned_data.get("NUMS")

        Login = DAL.Dal()
        email = request.POST['email']
        password = request.POST['password']
        result = Login.validate_login(email, password, user_type)
        if result == 1:
            if user_type == 'Customer':
                user = Login.getuserinfo(email, password)
                request.session['user'] = user.ID
                return redirect("DashBoard")
            elif user_type == 'Seller':
                seller = Login.getSellerinfo(email, password)
                request.session['user'] = seller.ID
                return redirect("SEllerDashBoard")
            elif user_type == 'Admin':
                admin = Login.getAdminInformation(email, password)
                request.session['user'] = admin.ID
                return redirect("UpdateAdminProfile")
            else:
                super_admin = Login.getSuperAdminInformation(email, password)
                request.session['user'] = super_admin.ID
                return redirect("UpdateSuperAdmin")


        elif result == 0:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
        else:
            messages.info(request, "You are Banned")
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        Register = DAL.Dal()
        user_type = request.POST.get('usertype', 'off')
        email = request.POST['email']
        if user_type == 'off':
            user_type = 'Customer'

        else:
            user_type = 'Seller'
        result = Register.register(request.POST['username'], email, request.POST['password'],
                                   request.POST['DOB'], user_type)
        if result == 1:
            messages.success(request, "Registered SuccessFully Please Login to Continue")
            return redirect("register")
        else:
            messages.warning(request, "This Email is Already Registered")
            return redirect('register')
    else:
        return render(request, 'register.html')


def userpanel(request):
    if 'user' in request.session:
        DL = DAL.Dal()
        All_products = DL.getAllProducts()
        items_count = DL.getCartitemslength(int(request.session['user']))
        DL.CloseConnection()
        messages.success(request, str(items_count))
        return render(request, 'Customer\Panel.html', {'allproducts': All_products, 'SearchValue': "Our Products"})
    else:
        return redirect("login")


def UpdateCustomerProfile(request):
    if 'user' in request.session:
        if request.method == 'POST':
            new_name = request.POST['newname']
            new_email = request.POST['newemail']
            old_password = request.POST['oldpass']
            new_password = request.POST['newpass']
            dal = DAL.Dal()
            user = dal.getuserinfofromId(int(request.session['user']))
            if user.password == old_password:
                if old_password != new_password:

                    if new_email not in dal.getAlluseremails() or user.email == new_email:
                        if new_name == '':
                            new_name = user.name
                        if new_email == '':
                            new_email = user.email
                        if dal.Update_Customer(new_name, new_email, new_password, int(request.session['user'])) == 1:
                            messages.success(request, "Profile Updated Successfully")
                        else:
                            messages.warning(request, "Some Error Occured")
                    else:
                        messages.warning(request, "This Email is Already Registered")
                else:
                    messages.warning(request, "New Password Cannot Be same as Old Password")

            else:
                messages.warning(request, "Old Password is Incorrect")
            dal.CloseConnection()
            return render(request, 'Customer\profileupdate.html')
        else:
            return render(request, 'Customer\profileupdate.html')


    else:
        return redirect("login")


def Categories(request):
    if 'user' in request.session:
        return render(request, 'Customer/Categories.html')
    else:
        return redirect('login')


def Cart(request):
    if 'user' in request.session:
        Dl = DAL.Dal()
        All_products = Dl.getCartitems(int(request.session['user']))
        total_sum = 0
        for prod in All_products:
            total_sum = total_sum + prod.getprice()
        Dl.CloseConnection()
        return render(request, 'Customer/Cart.html',
                      {'cartproducts': All_products, 'Totalsum': total_sum, 'Sumwithshipping': total_sum + 50})
    else:
        return redirect('login')


def removefromcart(request):
    if 'user' in request.session:
        if request.method == 'POST':
            prodid = request.POST['productid']
            Dl = DAL.Dal()
            Dl.Remove_From_Cart(int(request.session['user']), int(prodid))
            Dl.CloseConnection()
            return redirect("Cart")
    else:
        return redirect('login')


def Addtocart(request):
    response = redirect("DashBoard")
    val = request.COOKIES.get('prodcookie', 'default')
    Dl = DAL.Dal()
    res = None
    if val != 'default':
        res = Dl.getCart(int(request.session['user']), int(val))
    if res is None:
        result = Dl.addtoCart(int(request.session['user']), int(val))
        items_count = Dl.getCartitemslength(int(request.session['user']))
        Dl.CloseConnection()
        if result == 1:
            messages.success(request, str(items_count))
            print("success")
    else:
        print("Failed")
    return response


def checkout(request):
    if 'user' in request.session:
        val = str(request.COOKIES.get('cartprodts', 'default'))
        subtotal = 0
        if val != 'default':
            cart_products = filterstring(val)
            if request.method == 'POST':
                street_addr = request.POST['st_address']
                city = request.POST['city']
                phone = request.POST['Phone']

                Full_addr = street_addr + "  " + city
                Dl = DAL.Dal()
                price_index = len(cart_products) - 1
                order_id = Dl.addorder(int(request.session['user']), Full_addr, int(phone), 'Pending Confirmation',
                                       cart_products[price_index])
                for i in range(price_index):
                    Dl.addorderdetails(order_id, cart_products[i])
                Dl.Empty_Cart(int(request.session['user']))
                Dl.CloseConnection()
                return redirect('manageorders')
            else:
                subtotal = cart_products[len(cart_products) - 1]
        else:
            print("Failed")
        return render(request, "Customer/Checkout.html", {'subtotal': subtotal - 50, 'Total': subtotal})
    else:
        return redirect('login')


def BuyProductCheckout(request):
    if 'user' in request.session:
        f = open("prodid.txt", "r")
        val = f.read()
        val = int(val)
        f.close()
        os.remove("prodid.txt")
        subtotal = 0
        if val != 'default':
            Dl = DAL.Dal()
            All_prod = Dl.getAllProducts()
            Selected_product = [x for x in All_prod if x.prodid == int(val)]
            if request.method == 'POST':
                street_addr = request.POST['st_address']
                city = request.POST['city']
                phone = request.POST['Phone']
                Full_addr = street_addr + "  " + city
                price = Selected_product[0].getprice()
                order_id = Dl.addorder(int(request.session['user']), Full_addr, int(phone), 'Pending Confirmation',
                                       price)
                Dl.addorderdetails(order_id, Selected_product[0].prodid)
                Dl.CloseConnection()
                return redirect('manageorders')
            else:
                subtotal = Selected_product[0].getprice() + 50
        else:
            print("Failed")
        return render(request, "Customer/Checkout.html", {'subtotal': subtotal - 50, 'Total': subtotal})
    else:
        return redirect('login')


# filter string to retrieve the required values for products
def filterstring(str):
    tempstr = ""
    lis = []
    price_ind = 0
    for x in range(len(str)):
        if str[x] != ',':
            tempstr = tempstr + str[x]
        elif str[x + 1] != ',':
            lis.append(int(tempstr))
            tempstr = ""
        else:
            lis.append(int(tempstr))
            price_ind = x + 2
            break
    tempstr = ""
    for x in range(price_ind, len(str)):
        tempstr = tempstr + str[x]

    lis.append(int(tempstr))
    return lis


def cancelorder(request):
    if 'user' in request.session:
        val = request.COOKIES.get('ordercookie', 'default')
        Dl = DAL.Dal()
        if val != 'default':
            Dl.cancel_order(int(val))
            Dl.CloseConnection()
            return redirect('manageorders')
        else:
            print("Failed")
        return redirect('manageorders')
    else:
        return redirect('login')


def manageorders(request):
    if 'user' in request.session:
        Dl = DAL.Dal()
        order_list = Dl.get_orders(int(request.session['user']))
        buttons_list = []
        for order in order_list:
            productslist = []
            products_ids = Dl.get_order_products(order.orderid)
            Allproducts = Dl.getAllProducts()
            for product in Allproducts:
                for id in products_ids:
                    if product.prodid == id:
                        productslist.append(product)

            for prod in productslist:
                if order.products == '':
                    order.products = prod.prodname
                else:
                    order.products = order.products + "," + prod.prodname
            if order.order_Status == 'Pending Confirmation':
                btn = Btn("Cancel Order", "", "#bf1c3d")
                buttons_list.append(btn)
            elif order.order_Status == 'Shipped':
                btn = Btn("Cancel Order", "hidden", "#bf1c3d")
                buttons_list.append(btn)
            elif order.order_Status == 'Cancelled':
                btn = Btn("", "hidden", "#bf1c3d")
                buttons_list.append(btn)
            else:
                btn = Btn("Add/Edit Review", "", "#1cbf34")
                buttons_list.append(btn)
        order_list = zip(order_list, buttons_list)
        Dl.CloseConnection()
        return render(request, "Customer/manageOrder.html", {'orderslist': order_list})
    else:
        return redirect('login')


def addeditreview(request):
    if 'user' in request.session:
        if request.method == 'POST':
            review_txt = request.POST['reviewtext']
            val = request.COOKIES.get('ordercookie', 'default')
            if val != 'default':
                Dl = DAL.Dal()
                result = Dl.add_editReview(int(request.session['user']), val, review_txt)
                Dl.CloseConnection()
                if result == 0:
                    messages.success(request, "Review Addded SuccessFully")
                else:
                    messages.success(request, "Review Updated SuccessFully")
                return render(request, "Customer/Reviews.html")
            else:
                print("Failed")
                messages.error(request, "")
                return render(request, "Customer/Reviews.html")
        else:
            return render(request, "Customer/Reviews.html")
    else:
        return redirect('login')


def BuyProduct(request):
    if 'user' in request.session:
        val = request.COOKIES.get('prodcookie', 'default')
        Dl = DAL.Dal()
        subtotal = 0
        if val != 'default':
            All_prod = Dl.getAllProducts()
            Selected_product = [x for x in All_prod if x.prodid == int(val)]
            subtotal = Selected_product[0].getprice()
            if os.path.exists("prodid.txt"):
                os.remove("prodid.txt")
                f = open("prodid.txt", "w")
                f.write(val)
                f.close()
            else:
                f = open("prodid.txt", "w")
                f.write(val)
                f.close()
        else:
            print("Failed")
        return render(request, "Customer/BuyCheckout.html", {'subtotal': subtotal, 'Total': subtotal + 50})
    else:
        return redirect('login')


def DeleteAccount(request):
    if 'user' in request.session:
        if request.method == 'POST':
            password = request.POST['pass']
            confirm_password = request.POST['confpass']
            if password != confirm_password:
                messages.error(request, "Password and Confirm Password does not matches")
            else:
                dal = DAL.Dal()
                user = dal.getuserinfofromId(int(request.session['user']))
                if user.password != password:
                    messages.error(request, "Incorrect Password")
                else:
                    dal.deleteAccount(int(request.session['user']))
                    request.session.flush()
                    dal.CloseConnection()
                    return redirect('login')
        return render(request, "Customer/DeleteAccount.html")
    else:
        return redirect('login')


def logout(request):
    if request.session.has_key('user'):
        request.session.flush()
    return redirect('login')


# Integrated Work


def UpdateSellerProfile(request):
    form = CHOICES(request.POST)
    if 'user' in request.session:
        if request.method == 'POST':
            new_name = request.POST['newname']
            new_email = request.POST['newemail']
            old_password = request.POST['oldpass']
            new_password = request.POST['newpass']
            dal = DAL.Dal()
            user = dal.getSellerinfothroughId(int(request.session['user']))
            if user.password == old_password:
                if old_password != new_password:

                    if new_email not in dal.getSellerEmailInformation() or user.email == new_email:
                        if new_name == '':
                            new_name = user.name
                        if new_email == '':
                            new_email = user.email
                        if dal.Update_Seller(new_name, new_email, new_password, int(request.session['user'])) == 1:
                            messages.success(request, "Seller Profile Updated Successfully")

                        else:
                            messages.warning(request, "Some Error Occured")

                    else:
                        messages.warning(request, "This Email is Already Registered")

                else:
                    messages.warning(request, "New Password Cannot Be same as Old Password")



            else:
                messages.warning(request, "Old Password is Incorrect")
            dal.CloseConnection()
            return render(request, 'Seller\SellerProfileupdate.html')
        else:
            return render(request, 'Seller\SellerProfileupdate.html')


    else:
        return redirect("login")


# function for adding product
def addProduct(request):
    form = CHOICES(request.POST)
    if 'user' in request.session:
        if request.method == 'POST':
            product_name = request.POST['name']
            product_price = request.POST['price']
            product_category = request.POST['category']
            product_image = request.FILES['product_img']
            seller_id = int(request.session['user'])
            dal = DAL.Dal()
            fs = FileSystemStorage()
            product_image_name = fs.save(product_image.name, product_image)
            product_image_url = fs.url(product_image_name)
            if dal.addProduct(seller_id, product_name, product_price, product_category, product_image_url) == 1:

                messages.success(request, "Product added Successfully")
            else:
                os.remove()
                messages.warning(request, "Some Error in Processing")
            dal.CloseConnection()
            return render(request, 'Seller\AddProduct.html')
        else:
            return render(request, 'Seller\AddProduct.html')
    else:
        return redirect("login")


# function for updating product
def updateProduct(request):
    if 'user' in request.session:
        if request.method == 'POST':
            product_id = request.POST['id']
            new_name = request.POST['newname']
            new_price = request.POST['newprice']
            new_category = request.POST['newcategory']
            seller_id = int(request.session['user'])
            dal = DAL.Dal()
            if dal.checkValidSeller(product_id, seller_id) > 0:
                if dal.updateProduct(product_id, new_name, new_price, new_category) == 1:
                    messages.success(request, "Product updated Successfully")
                else:
                    messages.warning(request, "Some Error in Processing")
                dal.CloseConnection()
                return render(request, 'Seller\Productupdate.html')

            else:
                messages.warning(request, "You are trying to update invalid product")
            return render(request, 'Seller\Productupdate.html')


        else:
            return render(request, 'Seller\Productupdate.html')

    else:
        return redirect("login")


# function for removing product
def RemoveProduct(request):
    if 'user' in request.session:
        if request.method == 'POST':
            product_id = int(request.POST['id'])
            seller_id = int(request.session['user'])
            dal = DAL.Dal()
            if dal.checkValidSeller(product_id, seller_id) > 0:
                if dal.removeProduct(product_id) == 1:
                    messages.success(request, "Product deleted Successfully")
                else:
                    messages.warning(request, "Some Error in Processing")
                dal.CloseConnection()
                return render(request, 'Seller\RemoveProduct.html')

            else:
                messages.warning(request, "You are trying to delete invalid product")
            return render(request, 'Seller\RemoveProduct.html')
        else:
            return render(request, 'Seller\RemoveProduct.html')

    else:
        return redirect("login")


# function for updating Admin Profile.
def UpdateAdminProfile(request):
    form = CHOICES(request.POST)
    if 'user' in request.session:
        if request.method == 'POST':
            new_name = request.POST['newname']
            new_email = request.POST['newemail']
            old_password = request.POST['oldpass']
            new_password = request.POST['newpass']
            dal = DAL.Dal()
            user = dal.getAdminInfothroughid(int(request.session['user']))
            if user.password == old_password:
                if old_password != new_password:

                    if new_email not in dal.getAdminEmailInformation() or user.email == new_email:
                        if new_name == '':
                            new_name = user.name
                        if new_email == '':
                            new_email = user.email
                        if dal.Update_admin(new_name, new_email, new_password, int(request.session['user'])) == 1:
                            messages.success(request, "Admin Profile Updated Successfully")

                        else:
                            messages.warning(request, "Some Error Occured")

                    else:
                        messages.warning(request, "This Email is Already Registered")

                else:
                    messages.warning(request, "New Password Cannot Be same as Old Password")



            else:
                messages.warning(request, "Old Password is Incorrect")
            dal.CloseConnection()
            return render(request, 'Admin\AdminUpdateInformation.html')
        else:
            return render(request, 'Admin\AdminUpdateInformation.html')


    else:
        return redirect("login")


# function for Update Super Admin Information
def updateSuperAdminProfile(request):
    if 'user' in request.session:
        if request.method == 'POST':
            new_name = request.POST['newname']
            new_email = request.POST['newemail']
            old_password = request.POST['oldpass']
            new_password = request.POST['newpass']
            dal = DAL.Dal()
            user = dal.getSuperAdminInfofromid(int(request.session['user']))
            if user.password == old_password:
                if old_password != new_password:

                    if new_email not in dal.getSuperAdminEmailInformation() or user.email == new_email:
                        if new_name == '':
                            new_name = user.name
                        if new_email == '':
                            new_email = user.email
                        if dal.updateSuperAdmin(new_name, new_email, new_password, int(request.session['user'])) == 1:
                            messages.success(request, "Super Admin Profile Updated Successfully")

                        else:
                            messages.warning(request, "Some Error Occured")

                    else:
                        messages.warning(request, "This Email is Already Registered")

                else:
                    messages.warning(request, "New Password Cannot Be same as Old Password")
            else:
                messages.warning(request, "Old Password is Incorrect")
            dal.CloseConnection()
            return render(request, 'SuperAdmin\SuperAdminUpdateInformation.html')
        else:
            return render(request, 'SuperAdmin\SuperAdminUpdateInformation.html')


    else:
        return redirect("login")


# function for add Admin
def addAdmin(request):
    form = CHOICES(request.POST)
    if 'user' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            password = request.POST['password']
            email = request.POST['email']
            dal = DAL.Dal()
            if email not in dal.getAdminEmailInformation():
                if dal.addAdmin(password, name, email) == 1:
                    messages.success(request, "Admin added successfully")
                else:
                    messages.warning(request, "Some Error in Processing")
            else:
                messages.warning(request, "The admin with this email already exists")
            dal.CloseConnection()
            return render(request, 'SuperAdmin\AddAdmin.html')
        else:
            return render(request, 'SuperAdmin\AddAdmin.html')


    else:
        return redirect("login")


# function for remove Admin
def removeAdmin(request):
    form = CHOICES(request.POST)
    if 'user' in request.session:
        if request.method == 'POST':
            adminId = int(request.POST['id'])
            dal = DAL.Dal()
            if adminId not in dal.getAdminIds():
                messages.warning(request, "The admin with this id does not exist")
            else:
                if dal.removeAdmin(adminId) == 1:
                    messages.success(request, "Admin removed successfully")
                else:
                    messages.warning(request, "Some error in processing")

            dal.CloseConnection()
            return render(request, 'SuperAdmin\RemoveAdmin.html')

        else:
            return render(request, 'SuperAdmin\RemoveAdmin.html')

    else:
        return redirect("login")


def DeleteSellerAccount(request):
    if 'user' in request.session:
        if request.method == 'POST':
            password = request.POST['pass']
            confirm_password = request.POST['confpass']
            if password != confirm_password:
                messages.warning(request, "Password and Confirm Password does not matches")
            else:
                dal = DAL.Dal()
                user = dal.getSellerinfothroughId(int(request.session['user']))
                if user.password != password:
                    messages.warning(request, "Incorrect Password")
                else:
                    dal.deleteSellerAccount(int(request.session['user']))
                    request.session.flush()
                    return redirect('login')
        return render(request, "Seller/DeleteAccount.html")
    else:
        return redirect('login')


# panel for Seller
def sellerpanel(request):
    if 'user' in request.session:
        DL = DAL.Dal()
        All_products = DL.getSellerProducts(int(request.session['user']))
        DL.CloseConnection()
        # messages.success(request,str(items_count))
        return render(request, 'Seller\SellerPanel.html', {'allproducts': All_products})
    else:
        return redirect("login")


# panel for Super Admin
def SuperAdminPanel(request):
    if 'user' in request.session:
        return render(request, 'SuperAdmin/SuperAdminPanel.html')
    else:
        return redirect("login")


def ban_user(request):
    if 'user' in request.session:
        return render(request, "Admin\\ban.html")
    else:
        return redirect("login")


def ban_seller(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_id = int(request.POST['seller_id'])
            Dl = DAL.Dal()
            result = Dl.Ban_User(user_id, 'Seller')
            if result == 3:
                mssg = "Invalid Id"
                mssg_type = "#e30834"
            elif result == 2:
                mssg = "This Seller is already banned"
                mssg_type = "#e30834"
            elif result == 1:
                mssg = "Seller Banned SuccessFully"
                mssg_type = "#58c132"
            else:
                mssg = "Some Unknown Error Occurred"
                mssg_type = "#e30834"
            Dl.CloseConnection()
        return render(request, "Admin\\ban.html",
                      {'SellerMssg': mssg, 'sellmssgtype': mssg_type, 'CustMssg': "", 'custmssgtype': ""})
    else:
        return redirect("login")


def ban_customer(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_id = int(request.POST['cust_id'])
            Dl = DAL.Dal()
            result = Dl.Ban_User(user_id, 'Customer')
            if result == 3:
                mssg = "Invalid Id"
                mssg_type = "#e30834"
            elif result == 2:
                mssg = "This Customer is already banned"
                mssg_type = "#e30834"
            elif result == 1:
                mssg = "Customer Banned SuccessFully"
                mssg_type = "#58c132"
            else:
                mssg = "Some Unknown Error Occurred"
                mssg_type = "danger"
        return render(request, "Admin\\ban.html",
                      {'SellerMssg': "", 'sellmssgtype': "", 'CustMssg': mssg, 'custmssgtype': mssg_type})
    else:
        return redirect("login")


def unban_user(request):
    if 'user' in request.session:
        return render(request, 'Admin\\unban.html')
    else:
        return redirect("login")


def unban_seller(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_id = int(request.POST['seller_id'])
            Dl = DAL.Dal()
            result = Dl.Unban_User(user_id, 'Seller')
            if result == 3:
                mssg = "Invalid Id"
                mssg_type = "#e30834"
            elif result == 2:
                mssg = "This Seller is not banned"
                mssg_type = "#e30834"
            elif result == 1:
                mssg = "Seller Unbanned SuccessFully"
                mssg_type = "#58c132"
            else:
                mssg = "Some Unknown Error Occurred"
                mssg_type = "#e30834"
            Dl.CloseConnection()

        return render(request, "Admin\\unban.html",
                      {'SellerMssg': mssg, 'sellmssgtype': mssg_type, 'CustMssg': "", 'custmssgtype': ""})
    else:
        return redirect("login")


def unban_customer(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_id = int(request.POST['cust_id'])
            Dl = DAL.Dal()
            result = Dl.Unban_User(user_id, 'Customer')
            if result == 3:
                mssg = "Invalid Id"
                mssg_type = "#e30834"
            elif result == 2:
                mssg = "This Customer is not banned"
                mssg_type = "#e30834"
            elif result == 1:
                mssg = "Customer Unbanned SuccessFully"
                mssg_type = "#58c132"
            else:
                mssg = "Some Unknown Error Occurred"
                mssg_type = "danger"
            Dl.CloseConnection()
        return render(request, "Admin\\unban.html",
                      {'SellerMssg': "", 'sellmssgtype': "", 'CustMssg': mssg, 'custmssgtype': mssg_type})
    else:
        return redirect("login")


def manage_order_superadmin(request):
    if 'user' in request.session:
        Dl = DAL.Dal()
        order_list = Dl.getAllorders()
        buttons_list = []
        for order in order_list:
            if order.order_Status == "Completed":
                btn = Btn("", "hidden", "")
                buttons_list.append(btn)
            else:
                btn = Btn("", "", "")

                buttons_list.append(btn)
        order_list = zip(order_list, buttons_list)
        Dl.CloseConnection()
        return render(request, 'SuperAdmin/manageOrder.html', {'orderslist': order_list})
    else:
        return redirect("login")


def update_order(request):
    if 'user' in request.session:
        if request.method == 'POST':
            orderid = int(request.POST['order_id'])
            order_status = request.POST['order_status']
            Dl = DAL.Dal()
            Dl.update_order_status(orderid, order_status)
            Dl.CloseConnection()
        return redirect("manage_order_superadmin")
    else:
        return redirect("login")
