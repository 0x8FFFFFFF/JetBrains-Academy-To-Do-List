from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date


class ToDo:
    Base = declarative_base()

    class Table(Base):
        """The database model of a task"""
        # noinspection SpellCheckingInspection
        __tablename__ = 'task'
        id = Column(Integer, primary_key=True)
        task = Column(String, default='Unnamed task')
        deadline = Column(Date, default=datetime.today())

        def __repr__(self):
            return f'{self.id}. {self.task}'

    def __init__(self):
        self.session = None
        self.menu_choice = ''
        self.init_database()

    def init_database(self):
        """Creates and initializes a database"""
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        self.Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def menu(self):
        """Prints menu items and accepts user choice"""
        print('1) Today\'s tasks')
        print('2) Add task')
        print('0) Exit')
        self.menu_choice = input()

    def show_tasks(self):
        """Shows tasks from the database"""
        tasks = self.session.query(self.Table).all()
        print('Today:')
        if tasks:
            for task in tasks:
                print(f'{task}')
        else:
            print('Nothing to do!')

    def add_task(self):
        """Add a task to the database"""
        print('Enter task')
        new_task = self.Table(task=input(), deadline=datetime.today())  # strftime('%m-%d-%Y')
        self.session.add(new_task)
        self.session.commit()
        print('The task has been added!')

    def run(self):
        """Main logic of the program"""
        self.menu()
        if self.menu_choice == '1':
            self.show_tasks()
        elif self.menu_choice == '2':
            self.add_task()
        else:
            print('Bye!')


if __name__ == '__main__':
    todo = ToDo()
    todo.run()
