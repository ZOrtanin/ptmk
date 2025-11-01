# ptmk
CLI Application

## Описание
Консольное приложение для управления справочником сотрудников с поддержкой следующих функций:
- Создание таблицы в базе данных.
- Добавление записей о сотрудниках.
- Вывод всех записей с сортировкой по ФИО.
- Автоматическое заполнение базы данными (1,000,000 записей).
- Поиск по критерию: мужской пол и фамилия на "F".
- Оптимизация запросов к базе данных.

---

## Требования
- **Язык программирования**: Python 3.13.2 
- **База данных**: SQLite.
- **Библиотеки**:
  - `Faker` (для генерации тестовых данных).
  - Установить зависимости:

    ```bash
    pip install -r requirements.txt
    ```

---

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ZOrtanin/ptmk.git
   cd employee-directory
   ```
2. Создание виртуального окружения и активация (Linux):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
	```bash 
	pip install -r requirements.txt
	```

```bash

	Package           Version
	----------------- -------
	aiosqlite         0.21.0
	Faker             37.12.0
	iniconfig         2.3.0
	packaging         25.0
	pip               25.3
	pluggy            1.6.0
	psycopg2-binary   2.9.11
	Pygments          2.19.2
	pytest            8.4.2
	SQLAlchemy        2.0.44
	typing_extensions 4.15.0
	tzdata            2025.2

```


## Использование

### Приложение запускается из командной строки с параметрами:
```bash 

    mode [1] -  Create a database
                no arguments

    mode [2] -  Add to the database
                arguments: ["fio"] [date] [gendr]
                Example:
                    add human: 
                     "fio" 1987-02-15 Male
                
                    add humans: 
                        "fio" 1987-02-15 Male "fio" 1987-02-15 Male
    
    mode [3] -  get all items from the database
                no arguments
           
    
    mode [4] -  random filling of the database
                arguments: [mode]
                Example:

                1 - 1000000 item of random entries

                0 - add 100 item only men with a name 
                    starting with F 
    
    mode [5] -  get only only men with a name starting 
                with F (0 - False , 1 - True)
                arguments: [print list] [print time]

    mode [6] -  get the number of all the first letters
                no arguments

    
    mode [7] -  Get all the men
                no arguments

    
    mode [8] -  random filling of the database
                arguments: [count] [bool]

                count - number of random entries

                bool - add only men with a name starting 
                       with F (0-False, 1-True)


```


### Структура проекта
```
 
	 Copyemployee-directory/
	 	├── updete/          # Раздел для обновления функционала
	 	├── base_test/       # базы для тестов
		├── main.py          # Основной файл приложения
		├── employee.py      # Класс Employee с методами
		├── database.py      # Логика работы с базой данных
		├── requirements.txt # Зависимости
		└── README.md        # Документация

```


### Оптимизация базы данных
проверка идет на таблице с 1000000 строк в среднем

| SQLite:        | SQLite(индексы): | PostgresSQL:     |PostgresSQL(индексы): |
|----------------|------------------|------------------|----------------------|
| 0.12389        | 0,39944          | 0,09961          | 0,16039              |  
| 0.09725        | 0,05408          | 0,07551          | 0,06209              |  
| 0.09435        | 0,05157          | 0,09235          | 0,05940              |  
| 0.09361        | 0,05148          | 0,08661          | 0,05867              |  
| 0.09648        | 0,05311          | 0,0895           | 0,05807              |  
| 0.09269        | 0,04905          | 0,07288          | 0,08272              |  
| 0.09738        | 0,05122          | 0,0821           | 0,07133              |  
| 0.10204        | 0,06275          | 0,06836          | 0,06533              |  
| 0.09380        | 0,04955          | 0,0722           | 0,06319              |  
| 0.09452        | 0,04887          | 0,07473          | 0,06175              |  
|----------------|------------------|------------------|----------------------|
| 0,98601 сек    | 0,87112 сек      | 0,81385 сек      | 0,74294 сек          | 


### Планы на расширение функционала

#### Стабильность:
[ ] - Собрать Docker-образ с PostgreSQL базой
[ ] - Добавить логирование ошибок
[ ] - Написать автоматические тесты (например, с pytest).

#### Удобный интерфейс:
[ ] - Использовать как пример argparse для парсинга аргументов
	пример: 
	myApp --mode 2 --fio 'Фамилию Имя Отчество' --date 'дату рождения' --gender 'пол'
	myApp --mode 2  --date 'дату рождения' --gender 'пол' --fio 'Фамилию Имя Отчество'
[ ] - argparse автоматически сгенерирует --help

#### Прочее:
[ ] - Добавить сортировку в методы запросов.
[ ] - Реализовать генерацию ФИО с заданной буквой.
[ ] - фильтрация:
	[ ] - поиск по полному совпадению слова (например, 'Иванов')
	[ ] - фильтрацию по первой букве (не только по первой букве "F")
[ ] - Генерация дат рождения с максимальным количеством дней в месяце.
[ ] - Добавить конфигурационный файл (например, config.json) для гибкой настройки.
[ ] - Реализовать экспорт/импорт данных в CSV/JSON.




