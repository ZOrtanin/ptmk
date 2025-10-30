from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Определяем базовую модель
Base = declarative_base()

# Определяем модель таблицы
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, arg):
        super(Person, self).__init__()
        self.fio = arg.get('fio') 
        self.birth_date = self.getDate(arg.get('birth_date')) 
        self.gender = arg.get('gender')
        self.age = self.getAge()

    def getDate(self, date) -> str:
        if date is None: return None
        return datetime.strptime(date, '%Y-%m-%d').date()

    def getAge(self) -> str:
        # проверка на пустоту
        if self.birth_date is None: return None
        # получаем полные года        
        now = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d').date()
        age = (now - self.birth_date).days  # возраст в днях

        return str(round((age/365)//1))

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "birth_date": self.birth_date.strftime("%Y-%m-%d"),
            "gender": self.gender,
            "age": self.getAge()
        }


# Создаём подключение к базе данных
engine = create_engine('sqlite:///people.db')
Base.metadata.create_all(engine)