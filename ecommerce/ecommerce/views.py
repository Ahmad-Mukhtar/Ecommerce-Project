from django.contrib import messages
from django.shortcuts import render, redirect

from .Classes import DAL
from .forms import CHOICES


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


def login(request):
    form = CHOICES(request.POST)
    if not request.session.has_key('user'):
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
                    return redirect("SEllerDashBoard")
                elif user_type == 'Admin':
                    return redirect("AdminDashBoard")
                else:
                    return redirect("SuperAdminDashboard")


            elif result == 0:
                messages.info(request, "Invalid Credentials")
                return redirect('login')
            else:
                messages.info(request, "You are Banned")
                return redirect('login')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return redirect("DashBoard")


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
    DL = DAL.Dal()
    All_products = DL.getAllProducts()
    items_count = DL.getCartitemslength(int(request.session['user']))
    DL.CloseConnection()
    if 'user' in request.session:
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
            if request.method=='POST':
                street_addr = request.POST['st_address']
                city = request.POST['city']
                phone = request.POST['Phone']

                Full_addr=street_addr+"  "+city
                #get value and insert order
                Dl=DAL.Dal()
                price_index=len(cart_products)-1
                order_id=Dl.addorder(int(request.session['user']),Full_addr,int(phone),'Pending Confirmation',cart_products[price_index])
                for i in range(price_index):
                    Dl.addorderdetails(order_id,cart_products[i])
                return redirect('manageorders')
            else:
                subtotal = cart_products[len(cart_products) - 1]
        else:
            print("Failed")
        return render(request, "Customer/Checkout.html", {'subtotal': subtotal - 50, 'Total': subtotal})
    else:
        return redirect('login')


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


def manageorders(request):
    if 'user' in request.session:
        return render(request, "Customer/manageOrder.html")
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
                    return redirect('login')
        return render(request, "Customer/DeleteAccount.html")
    else:
        return redirect('login')


def logout(request):
    if request.session.has_key('user'):
        request.session.flush()
    return redirect('login')
