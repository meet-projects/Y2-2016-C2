from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


def Users(Base):
	__tablename__='users'
	id=Column(Integer, primary_key=True)
	name=Column(String(40))
	email=Column(String(40))
	password=Column(String(40))
	int1=Column(String)
	int2=Column(String)
	int3=Column(String)
	int4=Column(String)
	int5=Column(String)
	dob=Column(Date)
	nat=Column(String)
	read=relationship("Books", secondary=association_table)


def Books(Base):
	__tablename__='books'
	id=Column(Integer, primary_key=True)
	name=Column(String)
	authorid=Column(Integer, Foreignkey('authors.id'), nullable=False)
	type1=Column(String)
	type2=Column(String)
	type3=Column(String)
	type4=Column(String)
	type5=Column(String)
	lang=Column(String)
	nat=Column(String)
	review=Column(Integer)

def Authors(Base):
	__tablename__='authors'
	id=Column(Integer, primary_key=True)
	name=Column(String)
	dob=Column(Date)
	nat=Column(String)
	lang=Column(String)



def Reviews(Base):
	__tablename__='reviews'
	id=Column(Integer, primary_key=True)
	book_id=Column(Integer, Foreignkey('books.id'), nullable=False)
	user_id=Column(Integer, Foreignkey('users.id'), nullable=False)
	rating=Column(Integer)
	review=Column(String(300))

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)


#PLACE YOUR TABLE SETUP INFORMATION HERE

