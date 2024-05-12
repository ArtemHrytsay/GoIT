from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote

# Create your views here.


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'app_quotes/quotes.html', context={'quotes': quotes})


def authors(request):
    if request.GET.get("id", ''):
        authors = Author.objects.all().filter(id=request.GET.get("id", ''))
    else:
        authors = Author.objects.all()
    return render(request, 'app_quotes/authors.html', context={'authors': authors})


def tags(request):
    search_tag = request.GET.get("tag", '')
    if search_tag:
        quotes = Quote.objects.filter(tags__icontains=search_tag)
    else:
        quotes = Quote.objects.all()

    return render(request, 'app_quotes/tags.html', context={'quotes': quotes, 'tag': search_tag})


@login_required
def add_author(request):
    form_author = AuthorForm(instance=Author())
    if request.method == "POST":
        form_author = AuthorForm(request.POST, instance=Author())
        if form_author.is_valid():
            form_author.save()
            return redirect(to='app_quotes:authors')

    return render(request, 'app_quotes/add_author.html', context={'form_author': form_author})


@login_required
def add_quote(request):
    form_quote = QuoteForm(instance=Quote())
    if request.method == "POST":
        my_request = request.POST.dict()
        my_request["tags"] = my_request["tags"].replace(r", ", " ").replace(r",", " ").strip().split(" ")
        form_quote = QuoteForm(my_request, instance=Quote())
        if form_quote.is_valid():
            form_quote.save()
            return redirect(to='app_quotes:quotes')

    return render(request, 'app_quotes/add_quote.html', context={'form_quote': form_quote})
