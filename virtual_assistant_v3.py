from collections import UserDict
from datetime import datetime
import pickle

class InvalidPhoneNumber(Exception):
    pass

class InvalidBirthday(Exception):
    pass

# батьківський клас для всіх полів 
class Field:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value

    def clear_value(self):
        self.value = None

    def is_empty(self):
        return self.value is None


# обов'язкове поле з ім'ям
class Name(Field):
    def __init__(self, name):
        super().__init__(name)


# не обов'язкове поле з номером телефона
class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        
class Birthday:
    def __init__(self, day, month):
        self.day = day
        self.month = month


# клас, який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = self.validate_birthday(birthday)
        if phone:
            self.validate_phone(phone)


    def validate_phone(self, phone):
        if not isinstance(phone, str) or len(phone) != 10 or not phone.isdigit():
            raise InvalidPhoneNumber("Invalid phone number")
        return phone
    
    def validate_birthday(self, birthday):
        if birthday is None:
            return None

        if not isinstance(birthday, Birthday):
            raise InvalidBirthday("Invalid birthday")

        return birthday
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)

    def get_phones(self):
        return [phone.get_value() for phone in self.phones]

    def days_to_birthday(self):
        if self.birthday is None:
            return None

        current_date = datetime.date.today()
        current_year = current_date.year

        next_birthday = datetime.date(current_year, self.birthday.month, self.birthday.day)

        if current_date > next_birthday:
            next_birthday = datetime.date(current_year + 1, self.birthday.month, self.birthday.day)

        days_until_birthday = (next_birthday - current_date).days
        return days_until_birthday

# наслідується від класу UserDict і виконує пошук за записами до цього класу
class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.get_value()
        self.data[key] = record
        
    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)
        
    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.records):
            raise StopIteration

        page_records = self.records[self.current_index:self.current_index + self.page_size]
        self.current_index += self.page_size

        return page_records

    def iterator(self, page_size=1):
        self.page_size = page_size
        return self
    
    def search(self, query=None, num=None):
        result = []
        if query:
            for k in self.data:
                if query.lower() in k.lower():
                    if self.data[k].birthday:
                        result.append(
                            f"{k} : {self.data[k].phone.value}; birthday = {self.data[k].birthday.value}")
                    else:
                        result.append(
                            f"{k}: {self.data[k].phone.value}")
        if num:
            for k, v in self.data.items():
                if num in v.phone.value:
                    if self.data[k].birthday:
                        result.append(
                            f"{k} : {v.phone.value}; birthday = {self.data[k].birthday.value}")
                    else:
                        result.append(f"{k}: {v.phone.value}")
        res = [i for i in set(result)]
        return res
    
