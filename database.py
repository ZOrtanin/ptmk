from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import model


class BaseDB:
    def __init__(self, arg):
        self.arg = arg
        self.Session = sessionmaker(bind=model.engine)

    def create_partial_index(self) -> None:
        ''' Добавляем индексы в базу '''

        session = self.Session()
        query = text("""
            CREATE INDEX IF NOT EXISTS idx_my_fantasy
            ON people (fio, gender)
            WHERE SUBSTR(fio, 1, 1) = 'F';
        """)
        session.execute(query)
        session.commit()

    def addTable(self, fio, birth_date, gender) -> bool:
        ''' Запись одной строки в базу '''

        # Открываем сессию
        session = self.Session()

        # Добавляем запись
        try:            
            person = model.Person(
                    fio=fio, 
                    birth_date=birth_date, 
                    gender=gender
                    )

            session.add(person)
            session.commit()
            print(f"line: {self.fio}, {self.birth_date}, {self.gender}")
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            return False
        finally:
            session.close()
        return True

    def addTableArr(self, arr) -> bool:
        ''' Запись списка в базу '''

        session = self.Session()

        try:
            # Пакетная вставка
            session.bulk_save_objects(arr)

            # Фиксируем изменения
            session.commit()
            result = f" {len(arr)} line added" if len(arr) == 1 else f" {len(arr)} lines added"
            print(result)

        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            return False
        finally:
            session.close()

        return True

    def dataGet(self, filters=None, custom_filters=None, order=None) -> list[model.Person]:
        ''' Получаем составной запрос к базе в ответ объекты '''

        # Открываем сессию
        session = self.Session()

        # Собираем запрос
        query = session.query(model.Person)

        if filters:
            query = query.filter_by(**filters)

        if custom_filters:
            query = query.filter(*custom_filters)

        if order:
            query = query.order_by(*order)

        result = query.all()

        # Закрываем сессию
        session.close()

        return result

    def dataGetRaw(self, gender=None, letter=None) -> tuple:
        ''' Получаем параметры для поиска по базе в ответ кортедж '''

        # Открываем сессию
        session = self.Session()

        # Собераем запрос
        query = text("SELECT * FROM people WHERE gender = :gender AND SUBSTR(fio, 1, 1) = :letter")
        
        # query = text("SELECT * FROM people WHERE fio LIKE 'F%' AND gender = 'Male'")

        result = session.execute(query, {'gender': gender, 'letter': letter})

        rows = result.fetchall()

        # Закрываем сессию
        session.close()

        return rows
