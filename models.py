import os
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = "capstone"
database_path = 'postgresql://postgres:29042000@localhost:5432/' + database_name
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)

'''
Book
'''
class Book(db.Model):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    publish_date = Column(DateTime)
    authors = relationship('Author', backref="book", lazy=True)

    def __init__(self, title, publish_date):
        self.title = title
        self.publish_date = publish_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'publish_date': self.publish_date,
            'authors': list(map(lambda author: author.format(), self.authors))
        }

'''
Author
'''
class Author(db.Model):

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)

    def __init__(self, name, age, gender, book_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.book_id = book_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            "book_id": self.book_id
        }
