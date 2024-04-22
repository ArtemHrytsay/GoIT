from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, ReferenceField


class Authors(Document):
    meta = {'collection': 'authors'}
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Tags(EmbeddedDocument):
    name = StringField()


class Quotes(Document):
    meta = {'collection': 'quotes', "allow_inheritance": True}
    tags = ListField(EmbeddedDocumentField(Tags))
    author = ReferenceField(Authors)
    quote = StringField()
