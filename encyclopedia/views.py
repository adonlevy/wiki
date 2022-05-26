from django.shortcuts import render
from markdown import Markdown
from . import util, forms
import re
from random import randrange


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": forms.NewSearch()
    })


def topic(request, topic):
    markdowner = Markdown()
    page = util.get_entry(topic)
    if not page:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/topic.html", {
        "topic": topic,
        "page": markdowner.convert(page)
    })


def error(request):
    return render(request, "encyclopedia/error.html", {
        "message": "Page does not exist :-("
    })


def matches(request):
    # checking to see if the request was a post from our form
    if request.method == "POST":
        # this gets the form data and puts it in a variable called form. Printing this variable actually
        # just looks like an HTML structured form
        form = forms.NewSearch(request.POST)
        # making sure input is valid. Built in Django validator
        if form.is_valid():
            # accessing the query variable and assigning it to one here. I can access this variable like this because
            # I have defined it in forms.py as query. Making it lowercase to do a regex comparisson
            query = form.cleaned_data["query"].lower()
            # check to see if the page exists based on what was entered in the query
            page = util.get_entry(query)
            print(page)
            # if the page doesn't exist
            if not page:
                # prepping an empty array to serve as the place to hold all my regex matches and pass into the template
                matches_array = []
                # get list of all existing wiki pages
                entries = util.list_entries()
                # for each entry, check if the query matches a part of the entry name, if it does, add it to the
                # matches array and move on to the next entry. At the end of this I will have an array of all titles
                # that mtatch the query string and return that to display on the template
                for entry in entries:
                    if re.search(query, entry.lower()):
                        matches_array.append(entry)
                return render(request, "encyclopedia/matches.html", {
                    "query": query,
                    "matches": matches_array
                })
            else:
                return topic(request, query.capitalize())


def random(request):
    # initialize markdowner to convert page to HTML
    markdowner = Markdown()
    # get the list of titles of current pages
    list_of_pages = util.list_entries()
    # get the number of pages
    num_pages = len(list_of_pages)
    # use the number of pages as a ceiling parameter to get a random int in that range
    lookup_index = randrange(num_pages)
    # use that random int to get a page title from the list of pages
    page_title = list_of_pages[lookup_index]
    # use that page title to get the entire page from the helper function
    page = util.get_entry(page_title)

    # render the proper template based on the page returned
    return render(request, "encyclopedia/topic.html", {
        "topic": page_title,
        "page": markdowner.convert(page)
    })


def new(request):
    return render(request, "encyclopedia/new.html", {
        "newpage_form": forms.NewPage(),
        "description": "Create Page"
    })


def save(request):
    if request.method == 'POST':
        form = forms.NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            edit = form.cleaned_data["edit"]
            if edit is False:
                current_titles = util.list_entries()
                for titles in current_titles:
                    if title.lower() == titles.lower():
                        return render(request, "encyclopedia/error.html", {
                            "message": "A Page with that title already exists!"
                        })
            util.save_entry(title, content)
            return index(request)


def edit(request, topic):
    page = util.get_entry(topic)
    if page is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page does not exist :("
        })
    else:
        form = forms.NewPage()
        form.fields["title"].initial = topic
        form.fields["content"].initial = page
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/new.html", {
            "newpage_form": form,
            "title": form.fields["title"].initial,
            "description": "Edit Page",
        })
