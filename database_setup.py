from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()



class Users(Base):
	__tablename__='users'
	id=Column(Integer, primary_key=True)
	name=Column(String(40))
	email=Column(String(40))
	password=Column(String(40))
	dob=Column(Date)
	nat=Column(String)
	genres = relationship('Genre', secondary='user_to_genre', uselist=True)
	review=relationship('Reviews', secondary='user_to_review', uselist=True)
	books=relationship('Books', secondary='read_books', uselist=True)
	lang=relationship('Languages', secondary='users_to_languages', uselist=True)

class UserToReviews(Base):
	__tablename__='user_to_review'
	id=Column(Integer, primary_key=True)
	user=Column(Integer, ForeignKey('users.id'))
	review=Column(Integer, ForeignKey('reviews.id'))

class BooksToReviews(Base):
	__tablename__='book_to_review'
	id=Column(Integer, primary_key=True)
	book=Column(Integer, ForeignKey('books.id'))
	review=Column(Integer, ForeignKey('reviews.id'))

class ReadBooks(Base):
	__tablename__='read_books'
	id=Column(Integer, primary_key=True)
	book=Column(Integer, ForeignKey('books.id'))
	user=Column(Integer, ForeignKey('users.id'))

class Genre(Base):
	__tablename__='genre'
	id=Column(Integer, primary_key=True)
	name = Column(String)
	books = relationship('Books', secondary='book_to_genre', uselist=True)
	


class Books(Base):
	__tablename__='books'
	id=Column(Integer, primary_key=True)
	name=Column(String)
	authorid=Column(Integer, ForeignKey("authors.id"))
	author = relationship("Authors")
	lang=relationship('Languages', secondary='books_to_languages', uselist=True)
	nat=Column(String)
	review=relationship('Reviews', secondary='book_to_review', uselist=True)
	genres = relationship('Genre', secondary='book_to_genre', uselist=True)
	picture=Column(String)
	users=relationship('Users', secondary='read_books', uselist=True)

class BookToGenre(Base):
	__tablename__='book_to_genre'
	id=Column(Integer, primary_key=True)
	book_id = Column(Integer, ForeignKey('books.id'))
	genre_id = Column(Integer, ForeignKey('genre.id'))

class UserToGenre(Base):
	__tablename__='user_to_genre'
	id=Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	genre_id = Column(Integer, ForeignKey('genre.id'))

class Authors(Base):
	__tablename__='authors'
	id=Column(Integer, primary_key=True)
	name=Column(String)
	dob=Column(Date)
	nat=Column(String)
	lang=Column(String)
	picture=Column(String)
	books = relationship("Books", uselist=True)



class Reviews(Base):
	__tablename__='reviews'
	id=Column(Integer, primary_key=True)
	book=relationship('Books', secondary='book_to_review')
	user=relationship('Users', secondary='user_to_review')
	rating=Column(Integer)
	review=Column(String(300))


class Languages(Base):
	__tablename__="languages"
	id=Column(Integer, primary_key=True)
	language=Column(String)
	users=relationship('Users', secondary='users_to_languages', uselist=True)
	books=relationship('Books', secondary='books_to_languages', uselist=True)


class UsersToLanguages(Base):
	__tablename__="users_to_languages"
	id=Column(Integer, primary_key=True)
	user=Column(Integer, ForeignKey('users.id'))
	language=Column(Integer, ForeignKey('languages.id'))

class BooksToLanguages(Base):
	__tablename__='books_to_languages'
	id=Column(Integer, primary_key=True)
	book=Column(Integer, ForeignKey('books.id'))
	language=Column(Integer, ForeignKey('languages.id'))




#PLACE YOUR TABLE SETUP INFORMATION HERE

