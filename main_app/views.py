from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.message import EmailMessage
from . import pytubelinks as lnks
from django import template

context = lnks.videos_data


def main_page_view(request):

    context["indx"] = [i for i in range(len(context["links"]))]
    return render(request, "main_page/main_page_tube.html")


def index(request):
    return render(request, "authenticate/index.html")


def signup(request):
    if request.method == "POST":

        u_name = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        print(u_name, email, pass1)

        new_user = User.objects.create_user(u_name, email, pass1)
        new_user.save()
        messages.success(request, "Account Created Successfully.")

        my_address, gmail_key = "ckefa65@gmail.com", "gbjttvtibsxoojav"

        msg = EmailMessage()
        mssg = f"Hey {new_user.username},\nI’m Clinton, the founder of PyTube and I’d like to personally thank you for signing up to our service.\n\nWe established PyTube in order to provide a new way to stream online videos without  interuptions.\nI’d love to hear what you think of PyTube and if there is anything we can improve.\n\n If you have any questions, please reply to this email. I’m always happy to help!\n\nFrom\nClinton Kefa"

        msg.set_content(mssg)
        msg['Subject'] = "Welcome to PyTube"
        msg['From'] = my_address
        msg['To'] = new_user.email

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(my_address, gmail_key)
        s.send_message(msg)
        s.quit()

        return redirect("login")

    return render(request, "authenticate/reg/index.html")


def signin(request):
    if request.method == "POST":
        eml = request.POST["email"]
        pwd = request.POST["pass1"]

        username = User.objects.get(email=eml.lower()).username
        user = authenticate(request, username=username, password=pwd)

        if user:
            login(request, user)
            messages.success(request, "login successfull")
            return redirect('main_page_view')
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect("login")

    return render(request, "authenticate/login/index.html")


def signout(request):
    logout(request)
    messages.success(request, " Logout successfull")
    return redirect("main_page_view")


def vidplay(request):
    if request.method == "POST":
        indvid = request.POST['ind']
        txt = str(context["title"][int(indvid)])
        indvid = str(context["links"][int(indvid)])

        mplayer = {"h": indvid, "txt": txt}
        return render(request, "player/index.html", mplayer)
    return render(request, "player/index.html")
