
def newUI():
    if (arg[1] == '--mode'):

        # Парсим аргументы командной строки
        parser = argparse.ArgumentParser(description='Добавление записи в базу данных.')

        parser.add_argument('--mode', type=str, required=True, help='"Режим"')
        parser.add_argument('--fio', type=str, required=False, help='"ФИО"')
        parser.add_argument('--b_date', type=str, required=False, help='"Дата рождения (YYYY-MM-DD)"')
        parser.add_argument('--gender', type=str, required=False, help='"Пол"')

        args = parser.parse_args()  

        if ('1' == args.mode):
            # проверка аргументов
            # Создание объекта
            print("База успешно создана")        

        if ('2' == args.mode):
            human = People({'fio': args.fio, 'birth_date': args.b_date, 'gender': args.gender})    
            if (human.addTable()):
                print('-- успешно добавлена --')

        if ('3' == args.mode):
            getAll()

        if ('4' == args.mode):
            randomAdd(10)

        if ('5' == args.mode):
            getMaleF()