'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

        /top_site/views.py
            Django Views
                index
                profile
                register
'''

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserCreationForm

# Create your views here.

'''
index
    landing page for entire application. links to login/register

    url         /
    template    /top_site/templates/top_site/index.html
'''
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    else:
        return render(request, "top_site/index.html")

'''
login_required
    landing page following login. routes to game/editor

    url         /accounts/profile/
    template    /top_site/templates/top_site/accounts/profile.html
'''
@login_required
def profile(request):
    context = {"first_name": request.user}
    return render(request, "top_site/accounts/profile.html", context)

'''
register
    uses code from
        http://www.djangobook.com/en/2.0/chapter14.html

    url         /registration/register/
    template    /top_site/templates/registration/register/
'''
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, "registration/register.html", context)
