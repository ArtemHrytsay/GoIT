import json
import mongoengine
from datetime import datetime
from pathlib import Path

import models

def seed(path: Path):
    filename = path / "authors.json"
    with open(filename) as fd:
        datas = json.load(fd)

    for data in datas:
        author_data = dict()

        for key, value in data.items():
            if "date" in key:
                value = datetime.strptime(value, "%B %d, %Y").date()
            author_data[key] = value
        uniques = [k for k, v in models.Author._fields.items() if v.unique]
        params = {u: data[u] for u in uniques if u in data}
        if not (author := models.Author.objects(**params).first()):
            author = models.Author(**author_data)
        else:
            [author.__setitem__(key, value) for key, value in author_data.items() if key not in uniques]
        author.save()
        
    filename = path / "quotes.json"
    with open(filename) as fd:
        datas = json.load(fd)
    for data in datas:
        uniques = [k for k, v in models.Quote._fields.items() if v.unique]
        params = {u: data[u] for u in uniques if u in data}
        quote = models.Quote.objects(**params).first()
        quote_data = dict()

        for key, value in data.items():
            field = models.Quote._fields[key]
            if isinstance(field, mongoengine.ListField):
                values = []
                for v in value:
                    k = list(field.field.document_type._fields.keys())[0]
                    params = {k: v}
                    o = field.field.document_type(**params)
                    values.append(o)
                quote_data[key] = values
                continue

            if not quote and isinstance(field, mongoengine.ReferenceField):
                reference_type = models.Quote._fields[key].document_type
                uniques = [k for k, v in models.Author._fields.items() if v.unique]
                params = {uniques[0]: data[key]}
                reference = reference_type.objects(**params).first()
                quote_data[key] = reference
                continue

            if not quote:
                quote_data[key] = value

        if quote_data:
            if not quote:
                quote = models.Quote(**quote_data)
            else:
                [quote.__setitem__(key, value) for key, value in quote_data.items() if key not in uniques]
            quote.save()
