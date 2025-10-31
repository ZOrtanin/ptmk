import sys
import time
import argparse
import random
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from faker import Faker

import model, database

# Создаём объект базы данных
db = database.BaseDB(True)

# добовляем индексы в базу если их нет
db.create_partial_index()

# Создаём объект Faker для русского языка
fake = Faker('ru_RU')

# Счетчик рандомных фамилий
letter_count = 0


# mode 0
def help(error=False, mode=None):
    if error: print('        ### please enter the arguments ###')
    mode_1 = '''
    mode [1] -  Create a database
                no arguments
             '''
    mode_2 = '''
    mode [2] -  Add to the database
                arguments: ["fio"] [date] [gendr]
                Example:
                    add piople: 
                     "fio" 1987-02-15 Male
                
                    add pioples: 
                        "fio" 1987-02-15 Male "fio" 1987-02-15 Male
             '''
    mode_3 = '''
    mode [3] -  get all items from the database
                no arguments
            '''
    mode_4 = '''
    mode [4] -  random filling of the database
                arguments: [mode]
                Example:

                1 - 1000000 item of random entries

                0 - add 100 item only men with a name 
                    starting with F 
            '''
    mode_5 = '''
    mode [5] -  get only only men with a name starting 
                with F (0 - False , 1 - True)
                arguments: [print list] [print time]

            '''
    mode_6 = '''
    mode [6] -  get the number of all the first letters
                no arguments
                '''
    mode_7 = '''
    mode [7] -  Get all the men
                no arguments
            '''
    mode_8 = '''
    mode [8] -  random filling of the database
                arguments: [count] [bool]

                count - number of random entries

                bool - add only men with a name starting 
                       with F (0-False, 1-True)

    '''

    actions = {            
            '1': lambda: print(mode_1),
            '2': lambda: print(mode_2),
            '3': lambda: print(mode_3),
            '4': lambda: print(mode_4),
            '5': lambda: print(mode_5),
            '6': lambda: print(mode_6),
            '7': lambda: print(mode_7),
            '8': lambda: print(mode_8)
        }
    
    if mode:
        result = actions.get(str(mode))  
    else: 
        for func in actions.values():
            func()
        return
    result()

    return 


# mode 2
def addPeoples(arg):
    ''' Функция добовления людей '''

    if (len(arg) == 2):         
        return help(True, 2)

    # add_obj = People({})
    peoples = []
    row = []   

    for i, item in enumerate(arg[2:], start=0):
        row.append(item)

        if (len(row) == 3):
            # peoples.append(row[:])
            human = model.Person(
                            fio=translateStr(row[0]), 
                            birth_date=datetime.strptime(row[1], '%Y-%m-%d').date(), 
                            gender=row[2]
                            )
            peoples.append(human) 
            print(row)               
            row = []  

    if len(arg[2:]) > 0 and len(arg[2:])%3:
        print(row)
        print('колличество полей не совподает')
        return       

    if (db.addTableArr(peoples)):
        print('-- успешно --')


# mode 3
def getAll() -> None:
    # Получаем всех отсортированных по ФИО    
    people = db.dataGet(None, None, [model.Person.fio.asc()])    

    # Выводим данные
    for person in people:
        print(person.to_string())


# mode 4 
def addRandomPeoples(arg) -> None:
    
    if len(arg) >= 3:
        if int(arg[2]): 
            addRandom(1000000, False)
        else:
            addRandom(100, True)
    else:
        help(True, 4)


# mode 5
def getMaleF(arg) -> None:

    print_list = True
    print_time = True
    letter = "F"
    gender = "Male"

    if len(arg[2:]) >= 1:
        print_list = bool(int(arg[2]))

    if len(arg[2:]) >= 2:
        print_time = bool(int(arg[3]))

    if len(arg[2:]) >= 3:
        letter = arg[4]

    if len(arg[2:]) >= 4:
        gender = arg[5]

    starttime = time.time()

    # Получаем всех <--- для тестирования
    # filters = {"gender": gender}
    # custom_filters = [
    #     model.Person.fio.startswith(letter)  # Фильтр: фамилия начинается на "F"
    # ]
    # peoples = db.dataGet(filters, custom_filters) <--- для тестирования

    peoples = db.dataGetRaw(gender, letter)
    
    if print_list:
        for person in peoples:
            new_people = model.Person(person[1], person[2], person[3])
            print(new_people.to_string())
            # print(person.to_string())
    
    if print_time:        
        print(round(time.time() - starttime, 5), "сек Затрачено на выполнение запроса")
        print(len(peoples), '- количество полученных строк')

    print()
    help(True, 5)


# mode 6
def getAllLetter() -> None:
    arr = [ 
            'A', 'B', 'V', 'G', 'D', 'E', 'Y', 
            'Z', 'I', 'K', 'L', 'M', 'N', 'O', 
            'P', 'R', 'S', 'T', 'U', 'F', 'C'       
            ]

    for letter in arr:

        custom_filters = [
            model.Person.fio.startswith(letter) 
        ]

        peoples = db.dataGet(None, custom_filters)
        print(len(peoples), f"колличество - {letter}")


# mode 7
def getAllMale() -> None:
    starttime = time.time()

    # Получаем всех male
    filters = {"gender": "Male"}
    custom_filters = None
    people = db.dataGet(filters, custom_filters)
    print(len(people), 'Мужчин')

    # Получаем всех male
    filters = {"gender": "Female"}
    custom_filters = None
    people = db.dataGet(filters, custom_filters)
    print(len(people), 'Женщин')

    print(round(time.time() - starttime, 5), "сек Затрачено на выполнение запроса")


# mode 8
def addRandom(count=100, f=False, arg=None) -> None:

    if arg != None and len(arg) == 2:         
        return help(True, 8)

    print('Начинаем заполнение')

    if arg is not None:
        if len(arg) > 2:
            count = int(arg[2])

        if len(arg) > 3:
            f = bool(int(arg[3]))

    if (f):
        print('Заполняем только мужчин c F')

    # people = People({})

    # Список новых записей
    new_people = []

    for i in range(count):
        fakedata = fakeData(i % 2) if not f else fakeData(1, True, "Male")

        human = model.Person(
                    fio=fakedata['name'], 
                    birth_date=datetime.strptime(fakedata['birth_date'], '%Y-%m-%d').date(), 
                    gender=fakedata['gender']
                    )
        new_people.append(human)
        print('Заполнение:', i, end='\r')

    db.addTableArr(new_people)


# mode 9
def testBase() -> None:

    for i in range(10):
        starttime = time.time()

        # Получаем всех 
        filters = {"gender": "Male"}
        custom_filters = [
            model.Person.fio.startswith("F")  # Фильтр: фамилия начинается на "F"
        ]

        peoples = db.dataGetRaw(filters, custom_filters)

        print(round(time.time() - starttime, 5), "сек")
    

# helps functions
def translateStr(string) -> str:
    ''' Перевод слова на транслит '''
    translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '',
            'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', ' ': ' '
        }

    if string[0] not in translit_dict.keys():
        return string

    result = []

    for item in string:
        result.append(translit_dict[item])

    return ''.join(result)


def fakeData(gen=0, nameF=False, gender=None, attempts=0) -> dict:
    global letter_count
    max_attempts = 100  # Максимальное количество попыток 

    # для одинакового количества фамили с начальной буквой список и счетчик
    arr = [ 
            'A', 'B', 'V', 'G', 'D', 'E', 'Y', 
            'Z', 'I', 'K', 'L', 'M', 'N', 'O', 
            'P', 'R', 'S', 'T', 'U', 'F', 'C'       
            ]

    if (letter_count == len(arr)):
        letter_count = 0

    # Собираем дату рождения ( fake - создает проблемы )
    birth_date = f"{random.randint(1935, 2010)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    # Определяем пол если он не задан и на основе этого генерируем ФИО
    if (gender is None):
        gender = fake.random_element(elements=("Male", "Female"))

    last_name = fake.last_name_male() if gender == "Male" else fake.last_name_female()
    first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
    middle_name = fake.middle_name_male() if gender == "Male" else fake.middle_name_female()

    # Переводим это все в транслит ( fake - не умеет )
    name = translateStr(f"{last_name} {first_name} {middle_name}")

    # Защита от максимальной глубины рекурсивных вызовов
    if attempts >= max_attempts:
        return {'name': name, 'birth_date': birth_date, 'gender': gender}
    
    # Условия для вызова рекурсий
    if (name[0] != 'F' and nameF):        
        return fakeData(1, True, gender, attempts + 1)

    if (name[0] != arr[letter_count] and not nameF):        
        return fakeData(gen, nameF, gender, attempts + 1)

    letter_count += 1

    return {'name': name, 'birth_date': birth_date, 'gender': gender}


# main function
def main() -> None:
    arg = sys.argv
    
    if (len(arg) == 1):         
        return help(True)

    actions = {
            '0': lambda arg: help(),
            '1': lambda arg: print('База успешно создана'),
            '2': lambda arg: addPeoples(arg),
            '3': lambda arg: getAll(),
            '4': lambda arg: addRandomPeoples(arg),
            '5': lambda arg: getMaleF(arg),
            '6': lambda arg: getAllLetter(),
            '7': lambda arg: getAllMale(),
            '8': lambda arg: addRandom(100, False, arg),
            '9': lambda arg: testBase()
        }

    actions.get(arg[1], lambda arg: help())(arg)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")
