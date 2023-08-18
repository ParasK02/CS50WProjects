from django.http import  HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
import random


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,name):
    if name.lower() in [item.lower() for item in util.list_entries()]:

        return render(request, "encyclopedia/entry.html",{
            "name":name,
            "content": util.get_entry(name)
        })
    return render(request, "encyclopedia/error.html",{
            'errormsg':"Entry not found."
        })

def search(request):
    searchq = request.GET.get('q','')
    if searchq.lower() in [item.lower() for item in util.list_entries()]:
        return entry(request,searchq)
    else:
        return partial_search(request,searchq)
        
        
        
def partial_search(request,search):
    pages = []
    for query in util.list_entries():
        if search.lower() in query.lower():
            pages.append(query)
    return render(request,"encyclopedia/search.html",{
        "results":pages
    })
def create(request):
    if request.method == "POST":
        title=request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is None:
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')
        else:
            return render(request,"encyclopedia/create.html",{
                "title": title,
                "content": content,
                "error": True
            })


    return render(request,"encyclopedia/create.html")
def edit(request,name):
    if request.method == "POST":
        newContent = request.POST["new-content"]
        util.save_entry(name,newContent)
        return redirect(f'/wiki/{name}')
    return render(request, "encyclopedia/edit.html",{
        "name":name,
        "content": util.get_entry(name)
    })
    
    

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect(f'/wiki/{random_entry}')

