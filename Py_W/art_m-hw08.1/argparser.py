import argparse

from mongoengine import ListField, ReferenceField, EmbeddedDocumentField, Document, EmbeddedDocument
from mongoengine.queryset import QuerySet
from pathlib import Path

import models



parser     = None
subparsers = None
commands   = dict()

def create_parser():
    global parser
    global subparsers
    global commands
    exit_on_error = False


    parser = argparse.ArgumentParser(
        exit_on_error = exit_on_error,
        description = "Database commands",
        formatter_class = argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-d --data",
        help = "Specify data path.",
        type = Path,
        metavar = "data",
        dest = "data",
        default = "data",
        required=False
    )

 
    subparsers = parser.add_subparsers(dest = "command")

    for name, model in models.registry.items():
        for fieldname in  model._fields:
            if fieldname != "id":
                commands[fieldname] = model
    for name, model in commands.items():
        alias = ''.join([n[0] for n in name.split('_')])
        aliases = [name + ':', alias, alias +':']#'-' + 
        command = subparsers.add_parser(
            name,
            exit_on_error = exit_on_error,
            aliases = aliases,
            help = "Search by " + name + " in " + model._class_name
        )
        command.prog = name
        command.add_argument(
            "filter",
            help = "Filter",
            type = str,
            nargs = '+'
        )
        command.set_defaults(func = process_command)
    return parser

def process_command(args):
    command = subparsers.choices[args.command].prog
    model = commands[command]
    field = model._fields[command]
    if isinstance(args.filter, list) and len(args.filter) == 1:
        if type(field) != ListField:
            filters = {command + "__icontains": args.filter[0]}
        elif type(field) == ListField and type(field.field) == EmbeddedDocumentField:
            field_name = list(field.field.document_type._fields.keys())[0]
            filters = {command + "__" + field_name + "__icontains": args.filter[0]}
        result = model.objects(**filters).first()
        if result is not None:
            r = result.to_mongo()
            return r.to_dict()
    else:
        if type(field) != ListField:
            filters = {command + "__in": args.filter}
        elif type(field) == ListField and type(field.field) == EmbeddedDocumentField:
            field_name = list(field.field.document_type._fields.keys())[0]
            s = '|'.join(args.filter)
            filters = {command + "__" + field_name + "__iregex": s}
        result = model.objects(**filters).first()
        if result is not None:
            r = to_dict(result)
            return r
    return None

def to_dict(obj):
    if isinstance(obj, (QuerySet, list)):
        return list(map(to_dict, obj))
    elif isinstance(obj, (Document, EmbeddedDocument)):
        doc = dict()
        for field_name, field_type in obj._fields.items():
            field_value = getattr(obj, field_name)
            doc[field_name] = to_dict(field_value)
        return doc
    else:
        return obj


def parse_command(command: str) -> list:
    commands = tokenize(command, separators = ":, \t\n")
    commands = list(map(lambda x: x.strip(), commands))
    commands = list(filter(lambda x: len(x), commands))
    return commands


def parse_commands(commands: list, _parser: argparse.ArgumentParser|None = None):
    if _parser is None:
        _parser = parser
    result = None
    parsed_commands = None

    try:
        parsed_commands = _parser.parse_args(commands)
    except SystemExit as e:
        result =  ""
    except argparse.ArgumentError as e:
        result = str(e)

    if parsed_commands:
        result = parsed_commands.func(parsed_commands)
 
    return result


def tokenize(string: str, separators = " \t\n", delimiters = "\'\"") -> list:
    tokens    = list()
    i = 0
    delimiter = ''
    token     = ""

    while i < len(string):
        char = string[i]

        if not token and char in delimiters:
            delimiter = char
            i += 1
            continue
        if delimiter:
            i += 1
            if char in delimiters:
                delimiter = ''
                if token:
                    tokens.append(token)
                    token = ""
                else:
                    delimiter = char
            else:
                token += char
            continue
        i += 1
        if char in separators:
            # i += 1
            if token:
                tokens.append(token)
                token = ""
            continue
        else:
            # i += 1
            token += char

    if token:
        tokens.append(token)
        token = ""
    return tokens
