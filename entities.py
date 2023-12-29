from collections import UserDict
from datetime import date, datetime
import pickle
import os


class Field:
    mandatory = False

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, ind):
        self.__value = ind

class Name(Field):
    mandatory = True


class Phone(Field):

    def __init__(self, value):
        self.phone_validate(value)
        self.__value = value


    def phone_validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Not correct No')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, ind):
        self.phone_validate(ind)
        self.__value = ind

class Birthday(Field):

    def __init__(self, birth_date):
        self.__value = self.birth_validate(birth_date)

    def birth_validate(self, birth_date):
        try:
            result = datetime.strptime(birth_date, '%d.%m.%Y')
            return result
        except ValueError:
            raise ValueError('Not correct format of birth date. Should be like: 16.02.1990')


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birth_date):
        self.__value = self.birth_validate(birth_date)


class Record:

    def __init__(self, name, birth_date=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birth_date
        if birth_date:
            self.birthday = Birthday(birth_date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError('We dont have such No in the record')


    def remove_phone(self, phone_to_del):
        for phone in self.phones:
            if phone.value == phone_to_del:
                self.phones.remove(phone)

    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return Phone(phone_to_find)  #  this A-book method returns Record inst

    def days_to_birthday(self):
        try:
            if self.birthday.value:
                today = date.today()
                next_birthday = date(year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)

                if today > next_birthday:  # if we already had bday this year
                    next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)

                days_left = (next_birthday - today).days
                return days_left
        except:
            return 'This Record does not have Information on birthday'

    def __str__(self):
        result_str = 'Record name: ' + self.name.value + ' '
        if self.phones:
            phones_list = 'Phones_list: '
            for phone in self.phones:
                phones_list += phone.value + ' '
            result_str += phones_list
        if self.birthday:
            birthday_val = 'Birthday: '
            birthday_val += str(self.birthday.value)
            result_str += birthday_val

        return result_str

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)  #  it returns Record instance

    def find_part(self, str_part):  # divided this func to 2 parts - search by name and tel
        matching_names = []
        self.find_part_name(str_part, matching_names)
        self.find_part_tel(str_part, matching_names)
        for match in matching_names:
            print(match)
        return matching_names

    def find_part_name(self, str_part, matching_names):
        if matching_names is None:
            matching_names = []
        for record in self.data:
            if str_part in self.data[record].name.value:
                matching_names.append(self.data[record])
        return matching_names

    def find_part_tel(self, tel_part, matching_names):
        if matching_names is None:
            matching_names = []
        for record in self.data:
            if self.data[record] not in matching_names:  # exclude the objects if we already have it
                for phone in self.data[record].phones:
                    if tel_part in phone.value:
                        matching_names.append(self.data[record])
        return matching_names

    def delete(self, name_to_del):
        self.data = {n: rec for n, rec in self.data.items() if n != name_to_del}

    def print_rec(self, lines_per_time=2):
        iter_address_book = iter(self.items())
        while True:
            try:
                for _ in range(lines_per_time):
                    line = next(iter_address_book)
                    name, rec = line  # in name we store name of the record in str format(not object) in rec- Record obj
                    print(rec)
                print()
            except StopIteration:
                break

    def save_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_pickle(filename):
        with open(filename,  'rb') as file:
            deserialized = pickle.load(file)
        return deserialized


#

# rec2 = Record('rec2_2', '01.03.1988')
rec1 = Record('234')
rec2 = Record('rec2_2', '01.03.1988')

rec3 = Record('re23', '01.03.1988')

rec3.add_phone('1234567890')
# rec4.add_phone('1234567890')
a_book = AddressBook()

# a_book.add_record(rec1)
# a_book.add_record(rec2)
a_book.add_record(rec3)
a_book.add_record(rec1)
# a_book.save_pickle('content_file.bin')

re_stored_abook = None

if os.path.isfile('content_file.bin'):  # this block aut-ly runs everytime - to load objects if we have them in file
    try:  #  we use standard name of the file content_file.bin and the A-book is always saved to the name re_stored_abook
        re_stored_abook = AddressBook.load_pickle('content_file.bin')  # its a static method, no need to run it from some instance
    except MemoryError:
        print('Not correct object')
    except Exception:
        print('Error reading the file')
else:
    print('no file to load objects from found')

if re_stored_abook:
    print(re_stored_abook)
