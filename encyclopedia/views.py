from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import random

from . import util


class Search_Form(forms.Form):
    search = forms.CharField() # var here should match id/name in html form 


class Create_Page_Form(forms.Form):
    title = forms.CharField(label = "title")
    content = forms.CharField(label = "content")


class Edit_Page_form(forms.Form):
    content = forms.CharField(label = "content")


def apologize(request, message):
    return render(request, "encyclopedia/apologize.html", {
        "apology": message
    })


def create_new_page(request):
    if request.method == "POST":
        """
        Saves user's Pages. 
        """
        form = Create_Page_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        else: 
            apologize(request, "Invalid submission.")
        if title in util.list_entries():
            return apologize(request, "That page already exists. Try editing it instead.")
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": util.return_markdowned_content(title)
            })
    else:
        return render(request, "encyclopedia/create_new_page.html")


def edit_page(request, title):
    if request.method == "POST":
        form = Edit_Page_form(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": util.return_markdowned_content(title)
            })
        else: 
            return apologize(request, "Invalid submission.")
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": util.return_markdowned_content(title)
    })


def entries(request, title):
    if title == "random_page": 
        """
        Handles request for Random Page.
        """
        title = random.choice(util.list_entries())
        return render(request, "encyclopedia/entries.html", {
                    "title": title,
                    "content": util.return_markdowned_content(title)
        })
    else: 
        return render(request, "encyclopedia/entries.html", {
                    "title": title,
                    "content": util.return_markdowned_content(title)
                    })


def index(request):
    if request.method == "POST":
        """
        Handles Search Requests
        """
        form = Search_Form(request.POST)
        if form.is_valid():
            request.session["search"] = form.cleaned_data["search"]
            titles = util.list_entries()
            possible_matches = []
            for title in titles:
                if util.do_strings_match(request.session["search"], title):
                    """
                    Checks for exact matches. 
                    """
                    return render(request, "encyclopedia/entries.html", {
                        "title": title,
                        "content": util.return_markdowned_content(title)
                    })
                else:
                    if util.is_possible_match(request.session["search"], title):
                        """
                        Adds to list of possible matches
                        """
                        possible_matches.append(title)
            if possible_matches:
                """
                Returns list of potential matches. 
                """
                return render(request, "encyclopedia/index.html", {
                    "entries": possible_matches,
                    "search": True
                })
            else:
                return apologize(request, "There are no matches. Try again, or contribute.")
        else:
            return apologize(request, "The request was invalid.") 
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": sorted(util.list_entries(), key=str.lower)
    })