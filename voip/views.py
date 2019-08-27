import requests
import json
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.generic import TemplateView

from .models import Contacts
from .forms import ContactsForm, LoginForm

BASE_API = "https://l7api.com/v1.1/voipstudio/"


# Create your views here.
class VoipView(TemplateView):
    template_name = 'voip.html'
    # form = ContactsForm()

    def get(self, request, *args, **kwargs):
        clients = Contacts.objects.all().order_by('id')
        print(clients)

        # Log in to VOIP Studio only if the user isn't authenticated
        # if 'password' in request.session:

        return render(request, self.template_name, {'clients': clients})

    def post(self, request, **kwargs):
        form = ContactsForm(request.POST)
        print(request.POST)

        # if form.is_valid():
        #     form.save()

        return redirect('voip')


class LoginView(TemplateView):
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
                login(request, user)

                current_user = request.user
                email = current_user.email

                # Headers and data needed to connect to the API.
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "email": email,
                    "password": password,
                }

                # Make the login request to the VOIP Studio API.
                r = requests.post(BASE_API + "login", json=payload, headers=headers)

                print("Status code is -> ", r.status_code)
                json_request = json.loads(r.content)

                if r.status_code != 200:
                    # Display error
                    messages.error(request, json_request["errors"][0]["message"])
                    return redirect('login')
                else:
                    print(json_request["user_token"])
                    request.session['user_token'] = json_request["user_token"]
                    return redirect('voip')
            else:
                return redirect(reverse('login'))
        else:
            return redirect(reverse('login'))


def logout_view(request):
    logout(request)
    return redirect('login')
