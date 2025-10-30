from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

# Определяем базовую модель
Base = declarative_base()

# Определяем модель таблицы
class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)


# Создаём подключение к базе данных
engine = create_engine('sqlite:///people.db')
Base.metadata.create_all(engine)