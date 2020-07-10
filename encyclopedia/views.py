from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
import markdown2
import random
from . import util


class newPageForm(forms.Form):
    title = forms.CharField(label='Page Title',max_length=100, min_length=1)
    content = forms.CharField(widget=forms.Textarea, min_length=1)

    def clean_title(self):
        title = self.cleaned_data['title']
        entries = util.list_entries()
        for entry in entries:
            if entry.lower() == title.lower():
                raise forms.ValidationError("A page with that title already exists!")
        return title


def index(request):
    if request.GET:
        query = request.GET.get('q')
        print(query)
        if util.get_entry(query):
            return redirect('view', title=query)
        else:
            entries = []
            all_entry = util.list_entries()
            for entry in all_entry:
                if query.lower() in entry.lower():
                    entries.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "search": query
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def view(request, title):
    text = util.get_entry(title)
    if not text:
        return render(request, "encyclopedia/404.html")
    entry = markdown2.markdown(text)
    return render(request, "encyclopedia/pages.html", {
        "entries": entry,
        "title": title.capitalize()
    })

def edit(request, title):
    if request.POST:
        content = request.POST.get('text')
        util.save_entry(title, content)
        return redirect('view',title=title)
    text = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "entries": text,
        "title": title.capitalize()
    })

def create(request):
    if request.POST:
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('view',title=title)
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "title": 'Create a page'
        })
    return render(request, "encyclopedia/create.html", {
        "form": newPageForm(),
        "title": 'Create a page'
    })

def random_page(request):
    value = random.randint(0, len(util.list_entries())-1)
    return redirect('view', title=util.list_entries()[value])