from django.contrib.auth import authenticate, login
from django.shortcuts import render


def login_user(request):
    state = "Welcome."
    username = password = ""

    # User types
    group_one = "user"
    group_two = "booker"
    group_three = "admin"

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.groups.filter(name=group_one).count():
                    state = "Login success. Group: " + group_one
                    login(request, user)
                elif user.groups.filter(name=group_two).count():
                    state = "Login success. Group: " + group_two
                    login(request, user)
                elif user.groups.filter(name=group_three).count():
                    state = "Login success. Group: " + group_three
                    login(request, user)
                else:
                    # Should put error-handling code here later..
                    state = "weird"
            else:
                state = "Deactived account."
        else:
            state = "Username or password incorrect."

    return render(request, 'auth.html',{'state':state, 'username': username})