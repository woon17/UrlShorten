from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import info

# Create your views here.
def loginPage(request):
    context = {}
    print(f'loginPage: \n\n{"loginPage"}\n\n')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            info(request, 'username OR password is incorrect!')

    return render(request, 'account/login.html', context)

# logout: back to loginPage
def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    context = {}
    return render(request, 'account/register.html', context)
