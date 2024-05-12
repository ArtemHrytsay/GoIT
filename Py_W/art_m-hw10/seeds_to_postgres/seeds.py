
import json
from connect import session
from models import Author, Quote

with open("authors.json", "r", encoding="utf-8") as json_file:
    authors_json = json.load(json_file)


for record in authors_json:
    author = Author(fullname=record['fullname'],
                    born_date=record['date_born'],
                    born_location=record['location_born'],
                    description=record['bio'],
                    user_id=1
                    )
    session.add(author)
    session.commit()


with open("quotes.json", "r", encoding="utf-8") as json_file:
    quotes_json = json.load(json_file)


for record in quotes_json:
    author = (session.query(Author.id)
              .filter(Author.fullname.contains(record['author'])).first())
    if author:
        quote = Quote(tags=record['tags'],
                      author_id=author[0],
                      quote=record['quote'])
        session.add(quote)
        session.commit()
