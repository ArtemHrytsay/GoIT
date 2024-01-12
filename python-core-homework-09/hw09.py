contact_data = dict()


def add_change_contact(name_and_phone):
    data = name_and_phone.split(' ')
    contact_data[data[0]] = data[1]
    
def input_error(func):
    def inner():
        flag = True
        while flag:
            try:
                result = func()
                flag = False
            except KeyError:
                print("There is no contact with this name")
            except ValueError:
                print('Please, try again')
            except IndexError:
                print('Please, enter your name and phone separated by space')
        return result
    return inner


@ input_error
def handler():
    bot = True

    while bot:
        command = input('Enter the command: ').lower()
        if command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            add_change_contact(command.removeprefix('add '))
        elif command == "change":
            add_change_contact(command.removeprefix('change '))
        elif command == "phone":
            print(contact_data[command.removeprefix("phone ")])
        elif command == "show all":
            if contact_data:
                for name, number in contact_data.items():
                    print(f'Name: {name}, phone: {number}')
            else:
                print('The list is empty')
        elif command in ("good bye", "close", "exit"):
            print("Good bye!")
            bot = False
        else:
            print("Incorrect command. Please, try again")


if __name__ == '__hw09__':
    handler()