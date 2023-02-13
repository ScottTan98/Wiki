from django.shortcuts import render
from markdown2 import Markdown

import random
from . import util


def convert_mdtohtml(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = convert_mdtohtml(title)
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "error" : "Entry not found!"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content" : content
    })

def search(request):
    if request.method == "POST": 
        search_entry = request.POST['q']
        search_entry2 = convert_mdtohtml(search_entry)
        if search_entry2 is not None:
            return render(request, "encyclopedia/entry.html",{
            "title": search_entry,
            "content" : search_entry2
        })
        else: 
            alldata = util.list_entries()
            recommendation = []
            for entry in alldata:
                if search_entry.lower() in entry.lower():
                    recommendation.append(entry) 
            return render(request, "encyclopedia/searchresult.html",{
                "search" : recommendation
            })


def create(request):
    if request.method == "POST":
        title = request.POST['title']
        contentbr = request.POST['content']
        alldata = util.get_entry(title)
        if alldata == None:
            util.save_entry(title, contentbr)
            content = convert_mdtohtml(title)
            return render(request, "encyclopedia/entry.html",{
                "title" : title,
                "content" : content
            })
        else:
            return render(request, "encyclopedia/error.html",{
            "error" : "Entry page already exists!"
        })

    else:
        return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "POST": 
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title" : title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        converted_content = convert_mdtohtml(title)
        return render(request, "encyclopedia/entry.html",{
                "title" : title,
                "content" : converted_content
            })

def random_page(request):
    titles = util.list_entries()
    title = random.choice(titles)
    converted_content = convert_mdtohtml(title)
    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "content" : converted_content
     })