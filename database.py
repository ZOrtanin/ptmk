from sqlalchemy.orm import sessionmaker
import model


class BaseDB:
    def __init__(self, arg):
        self.arg = arg
        self.Session = sessionmaker(bind=model.engine)

    def addTable(self, fio, birth_date, gender) -> bool:
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
            print(f"Запись: {self.fio}, {self.birth_date}, {self.gender}")
        except Exception as e:
            print(f"Ошибка: {e}")
            session.rollback()
            return False
        finally:
            session.close()
        return True

    def addTableArr(self, arr) -> bool:
        session = self.Session()

        try:
            # Пакетная вставка
            session.bulk_save_objects(arr)

            # Фиксируем изменения
            session.commit()
            result = f" {len(arr)} Запись добавленна" if len(arr) == 1 else f" {len(arr)} Записи добавленно"
            print(result)

        except Exception as e:
            print(f"Ошибка: {e}")
            session.rollback()
            return False
        finally:
            session.close()

        return True

    def dataGet(self, filters=None, custom_filters=None, order=None):
        # Открываем сессию
        session = self.Session()

        # Собераем запрос
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
