from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from markdown2 import Markdown
from random import choice
import os


def index(request):
    return render(request, "encyclopedia/index.html", {
        "all_entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "The entry was not found.",
            "requested_title": title
        }, status=404)
    # Convert .md to .html
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdowner.convert(content)
    })
    
def search(request):
    title = request.GET.get("q")
    content = util.get_entry(title)
    

    # Partial Match
    if not content:
        all_entries = util.list_entries()
        result_entries = []

        title = title.lower()
        for entry in all_entries:
            if title in entry.lower():
                result_entries.append(entry)
            else:
                continue

        return render(request, "encyclopedia/search.html", {
        "entries": result_entries
        })

    # Exact Match
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdowner.convert(content)
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Validation
        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "message": "Title and content should not be empty!"
            })
        entries = util.list_entries()

        if title.lower() in [entry.lower() for entry in entries]:
            return render(request, "encyclopedia/error.html", {
                "message": "The entry already exist."
            })

        if "/" in title or "<" in title:
            return render(request, "encyclopedia/error.html", {"message": "標題包含非法字元！"})

        if "/" in content or "<" in content:
            return render(request, "encyclopedia/error.html", {"message": "內文包含非法字元！"})
        
        # Save it to disk
        util.save_entry(title, content)

        # Redirect to that new entry
        return HttpResponseRedirect(reverse("entry", kwargs={'title':title}))


    else:
        return render(request, "encyclopedia/new_page.html")
    
    
def edit_page(request, original_title):
    # Nameing Rule in this function: Using pre adj "original" and "edited" to describe variable title and content

    # Save the edition
    if request.method =="POST":
        edited_title = request.POST.get("edited_title")
        edited_content = request.POST.get("edited_content")

        # Validation
        if not edited_title or not edited_content:
            return render(request, "encyclopedia/error.html", {
                "message": "Title and content should not be empty!"
            })
    
        # Save the edited_title and edited_content to disk
        util.edit_entry(original_title, edited_title, edited_content)


        # Redirect to that edited entry
        return HttpResponseRedirect(reverse("entry", kwargs={'title':edited_title}))



    # Get the edit page
    else:
        original_content = util.get_entry(original_title)
        if not original_content:
            return render(request, "encyclopedia/error.html", {
                "message": "Wrong title"
            })
        return render(request, "encyclopedia/edit_page.html", {
            "original_title": original_title,
            "original_content": original_content
        })





def random(request):
    all_entries = util.list_entries()
    title = choice(all_entries)
    print(title)
    return HttpResponseRedirect(reverse("entry", kwargs={'title':title}))



