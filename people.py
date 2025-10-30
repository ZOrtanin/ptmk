from sqlalchemy.orm import sessionmaker
from datetime import datetime
import model, database

db = database.BaseDB(True)


class People(object):
    """ Клас человека """
    def __init__(self, arg):
        super(People, self).__init__()
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

    def addTable(self) -> bool:
        return db.addTable(self.fio, self.birth_date, self.gender)

    def addTableArr(self, arr) -> bool:
        return db.addTableArr(arr)
