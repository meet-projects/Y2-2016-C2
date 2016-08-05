from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Users, Books, Authors, Reviews, Genre, BookToGenre, UserToGenre, association_table
from datetime import datetime

engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#You can add some starter data for your database here.

comedy = Genre(name="Comedy")
action = Genre(name="Action")
drame = Genre(name="Drama")

dob=datetime(year=1941, month=3, day= 13)
author1=Authors(name="Mahmoud Darwish", dob=dob, nat="Palestinian", lang="Arabic", picture="Mahmoud-Darwish.jpg")
book=Books(name="Unfortunately, it was paradise", authorid=1, lang="Arabic", nat="Palestinian", picture="paradise.jpeg")
book2=Books(name="Journal of an Ordinary Grief", authorid=1, lang="Arabic", nat="Palestinian", picture="grief.jpeg")
bookrel=BookToGenre(book_id=1, genre_id=3)
book2rel=BookToGenre(book_id=2, genre_id=3)
session.add(comedy)
session.add(action)
session.add(drame)
session.add(book)
session.add(book2)
session.add(author1)
session.add(bookrel)



session.commit()

