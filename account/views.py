from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import info
from .forms import SignUpForm
from django.http import HttpResponseRedirect
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


def singUpNewUser(request):
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()

    return render(request, 'account/signup.html', {'form': form})
