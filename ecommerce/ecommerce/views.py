from django.contrib import messages
from django.shortcuts import render, redirect
from .Classes.Login_Register import LR
from .forms import CHOICES


def homepage(request):
    return render(request, 'HomePage.html')


def login(request):
    form = CHOICES(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_type = form.cleaned_data.get("NUMS")

        Login = LR()
        email=request.POST['email']
        password=request.POST['password']
        result = Login.validate_login(email,password, user_type)
        print(email,password,user_type)
        if result == 1:
            return redirect("/")
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
        Register = LR()
        user_type = request.POST.get('usertype', 'off')
        print(user_type)
        if user_type == 'off':
            user_type = 'Customer'
        else:
            user_type = 'Seller'
        result = Register.register(request.POST['username'], request.POST['email'], request.POST['password'],
                                   request.POST['DOB'], user_type)
        if result == 1:
            messages.success(request,"Registered SuccessFully Please Login to Continue")
            return redirect("register")
        elif result == 0:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
        else:
            messages.error(request, "You are Banned")
            return redirect('login')
    else:
        return render(request, 'register.html')
