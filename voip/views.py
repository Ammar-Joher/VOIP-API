import requests
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.generic import TemplateView

from .models import Contacts
from .forms import ContactsForm, LoginForm

BASE_API = "https://l7api.com/v1.1/voipstudio/"  # The base api for voip studio.
scheduler = BackgroundScheduler()  # Initializing the scheduler to send pings to the api so we get to keep the user token


# Create your views here.
class VoipView(TemplateView):
    template_name = 'voip.html'
    # form = ContactsForm()

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # Get only contacts that are for that specific user.
            clients = Contacts.objects.filter(user_id=request.user).order_by('id')
            return render(request, self.template_name, {'clients': clients})
        else:
            return redirect('login')

    def post(self, request, **kwargs):
        if request.POST["data"] == "call":
            username = request.user.email
            password = request.session['user_token']
            phone_number = request.POST['phone_number']
            # print("Username -> ", username, "\nPassword -> ", password, "\nPhone Number -> ", phone_number)

            # Header and data needed to connect to the API.
            headers = {'Content-Type': 'application/json'}
            payload = {
                "to": phone_number
            }

            # Make the Call request to the VOIP Studio API.
            r = requests.post(BASE_API + "calls", json=payload, headers=headers, auth=(username, password))

            if r.status_code == 201:
                # Increments counter based on how many calls were made.
                called_user = Contacts.objects.get(phone_number=phone_number)
                called_user.received_count += 1
                called_user.save()

        return redirect('voip')


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = LoginForm(request.POST, request.POST)

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
                json_request = json.loads(r.content)

                if r.status_code != 200:
                    # Display error
                    messages.error(request, json_request["errors"][0]["message"])
                    return redirect('login')
                else:
                    # Start The Scheduler
                    if not scheduler.running:
                        updater(request, 1)

                    print(json_request["user_token"])
                    request.session['user_token'] = json_request["user_token"]
                    return redirect('voip')
            else:
                return redirect(reverse('login'))
        else:
            return redirect(reverse('login'))


def logout_view(request):
    requests.post(BASE_API + "logout", auth=('', request.session['user_token']))

    # Stop Timed Schedule
    updater(request, 0)

    logout(request)
    return redirect('login')


def ping_api(request):
    print("Inside Ping Function")

    # Makes a ping request every 14 minutes to keep the user token alive
    r = requests.get(BASE_API + "ping", auth=('', request.session['user_token']))
    print(r.status_code)
    print(r.content)

    # ToDo: logout if the ping fails


# Start APScheduling
# 0 = Stop
# 1 = Start
def updater(request, start_or_stop):
    if start_or_stop == 1:
        scheduler.start()
        scheduler.add_job(lambda: ping_api(request), 'interval', minutes=14, id='ping_scheduler_id')
    elif start_or_stop == 0:
        scheduler.remove_all_jobs()
