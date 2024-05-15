from django.forms import DateField, DateInput, HiddenInput, IntegerField, ModelForm, CharField, TextInput, Select, \
    ModelChoiceField, JSONField, Textarea
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    id            = IntegerField(widget=HiddenInput(), required=False)
    fullname      = CharField(min_length=3, max_length=25, widget=TextInput(attrs={"class": "form-control"}))
    born_date     = DateField(widget=DateInput(attrs={"type": "date", "class": "form-control"}))
    born_location = CharField(max_length=150, widget=TextInput(attrs={"class": "form-control"}))
    description   = CharField(max_length=2700, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model  = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    id     = IntegerField(widget=HiddenInput(), required=False)
    quote  = CharField(max_length=1500, required=True, widget=TextInput(attrs={"class": "form-control"}))
    author = ModelChoiceField(queryset=Author.objects.all(), required=True,
                              widget=Select(attrs={"class": "form-control"}))
    tags   = JSONField(max_length=500, required=False, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
