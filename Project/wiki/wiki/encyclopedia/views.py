from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
import logging

from . import util
import secrets
from wiki import settings
from markdown2 import Markdown
class  NewWikiForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'placeholder':'Enter title', 'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'title':'Enter title', 'placeholder':'Enter content'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(),required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'encyclopedia/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            ("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, '/encyclopedia/login.')
            return HttpResponseRedirect("encyclopedia:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'encyclopedia/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return  redirect('index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'encyclopedia/login.html', context)
    else:
        return render(request, 'encyclopedia/login.html', context)


def logout_request(request):
    logout(request)
    context={}
    return render(request, 'encyclopedia/login.html', context)



def entry(request,entry):
    markdowne = Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/error.html",{

        })
    else:
        return render(request,"encyclopedia/page.html",{
            "entry": markdowne.convert(page),
            "entryTitle":entry
        })

def newWiki(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry':title}))
            else:
                return render(request, "encyclopedia/newWiki.html",{
                "form": form,
                "existing":True,
                "entry": title
                })
        else:
            return render(request,"encyclopedia/newWiki.html",{
                "form": form,
                "existing": True,

            })
    else:
        return render(request, "encyclopedia/newWiki.html",{
            "form": NewWikiForm(),
            "existing": False
        })

def edit(request, entry):
    if request.method == "POST":
        entryPage = util.get_entry(entry)

    if entryPage is None:
        return render(request,"encyclopedia/error.html",{
            "entryTitle":entry
        })

    else:
        form = NewWikiForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True

        return render(request, "encyclopedia/newWiki.html",{
            "form":form,
            "edit": form.fields["edit"].initial
        })


def random(request):
    pages = util.list_entries()
    randomPage = secrets.choice(pages)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry':randomPage}))

def search(request):

    text = request.GET.get('q', '')

    if util.get_entry(text) is None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry':Value}))
    else:
        entryString = []

        for entry in util.list_entries():
            if text.upper() in entry.upper():
                entryString.append(entry)

    return render(request,"encyclopedia/index.html",{
        "entries": entryString,
        "search": True,
        "text": text
    })
