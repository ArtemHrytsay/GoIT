from models import Authors, Quotes

import connect


def input_parser(user_input):
    command, value = user_input.split(':')
    return command.strip(), value.strip()


def input_handler(command, value):
    match command:
        case 'name':
            find_author(value)
        case 'tag':
            find_tag(value)
        case 'tags':
            tags = value.strip().split(',')
            for tag in tags:
                find_tag(tag.strip())
        case _:
            print(f'Wrong command. Try again')


def find_author(author):
    data = Quotes.objects()
    if data:
        for i in range(int(len(data)/2)):
            if author == data[i]["author"].fullname:
                print(data[i].quote)
    else:
        print('Information has not been found')


def find_tag(tag):
    tags_list = list()
    data = Quotes.objects()

    if data:
        for el in data:
            for data_tag in el.tags:
                if tag == data_tag.name:
                    tags_list.append(el.quote)
        print(tags_list)
    else:
        print('Information has not been found')


if __name__ == '__main__':
    while True:
        user_input = input('Type the command: ')
        if user_input == 'exit':
            exit(0)
        else:
            try:
                command, value = input_parser(user_input)
                input_handler(command, value)
            except ValueError:
                print(f'Wrong format. Try {command}:{value}')
