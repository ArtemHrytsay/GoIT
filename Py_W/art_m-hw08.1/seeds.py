
import json

import connect
from models import Tags, Authors, Quotes


with open("authors.json", "r", encoding="utf-8") as json_file:
    authors_json = json.load(json_file)

for authors in authors_json:
    new_author = Authors(
        fullname=authors.get("fullname"),
        born_date=authors.get("born_date"),
        born_location=authors.get("born_location"),
        description=authors.get("description"),
    )
    new_author.save()

with open("quotes.json", "r", encoding="utf-8") as json_file:
    quotes_json = json.load(json_file)

for quote in quotes_json:
    tags = list()
    author_for_quotes = None
    new_quote = quote.get("quote")

    for tag in quote.get("tags"):
        tags.append(Tags(name=tag))

    for author in Authors.objects():
        if quote.get("author") == author.fullname:
            author_for_quotes = author

    output_quote = Quotes(tags=tags, author=author_for_quotes, quote=new_quote)
    output_quote.save()
