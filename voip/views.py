from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView

from .models import voip_user
from .forms import voip_user_form, LoginForm


class voipView(TemplateView):
    template_name = 'voip.html'
    form = voip_user_form()

    def get(self, request, *args, **kwargs):
        clients = voip_user.objects.all().order_by('id')
        print(clients)

        # password = request.session['password']

        return render(request, self.template_name, {'clients': clients})

    def post(self, request, **kwargs):
        form = voip_user_form(request.POST)
        print(form)

        password = kwargs['password']

        # if form.is_valid():
        #     form.save()

        return redirect('voip', password)


class loginView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = LoginForm(request.POST, request.POST)
        print(form)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session['password'] = password
                login(request, user)
                return redirect('voip')
            else:
                return redirect(reverse('login'))
        else:
            return redirect(reverse('login'))


def logoutView(request):
    logout(request)
    return redirect('login')