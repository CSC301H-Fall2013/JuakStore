from django.contrib.auth import authenticate, login
from django.shortcuts import render

def login_user(request):
    state = "Welcome."
    username = password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='admin').count():
                    group_name = 'admin'
                elif user.groups.filter(name='booker').count():
                    group_name = 'booker'
                elif user_groups.filter(name='user').count():
                    group_name - 'user'
                else: print("something is not right..")
                state = "Login success. Group: " + group_name
            else:
                state = "Deactived account."
        else:
            state = "Username or password incorrect."

    return render(request, 'auth.html',{'state':state, 'username': username})