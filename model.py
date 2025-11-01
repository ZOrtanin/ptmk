# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from datetime import date

# Определяем базовую модель
Base = declarative_base()

# Определяем модель таблицы
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, fio, birth_date, gender):
        super(Person, self).__init__()
        self.fio = fio 
        self.birth_date = self.getDate(birth_date) 
        self.gender = gender
        self.age = self.getAge()

    def getDate(self, date) -> date:
        if date is None: return None
        return datetime.strptime(str(date), '%Y-%m-%d').date()

    def getAge(self) -> str:
        # проверка на пустоту
        if self.birth_date is None: return None
        # получаем полные года        
        now = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d').date()
        age = (now - self.birth_date).days  # возраст в днях

        return str(round((age/365)//1))

    def to_dict(self) -> dict:
        return {
            "full_name": self.fio,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "age": self.getAge()
        }

    def to_string(self) -> str:
        return f"ФИО: {self.fio}, Дата рождения: {self.birth_date}, Пол: {self.gender}, кол-во полных лет: {self.getAge()}"


# Создаём подключение к базе данных
new_sqlite = 'sqlite:///people.db'

# Обычный движок
engine = create_engine(new_sqlite)
Base.metadata.create_all(engine)

# Для тестирования
# sqlite = 'sqlite:///base_test/people_big.db'
# sqlite_fast = 'sqlite:///base_test/people_big_fast.db'
# postgress = 'postgresql://postgres:postgres@localhost:5432/test'
# Асинхронный
# async_engine = create_async_engine("sqlite+aiosqlite:///people_big.db")
