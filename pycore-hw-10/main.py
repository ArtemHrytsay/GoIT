from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if len(self.value) != 10 and isinstance(self.value, str) or not self.value.isdigit():
            raise ValueError("Phone number must have 10 numbers. Try again.")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = list()

    def add_phone(self, phone):
        phone_num = Phone(phone)
        phone_num.validate()
        self.phones.append(phone_num)

    def remove_phone(self, phone):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("This number isn´t in the list.")
            
    def find_phone(self, phone) -> None:
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        self.record = dict()
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name] if name in self.data else None
        
    def delete(self, name):
        if name in self.data:
            del self.data[name]