from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Users, Books, Authors, Reviews, Genre
from datetime import datetime

engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#You can add some starter data for your database here.

#comedy = Genre(name="Comedy")
#action = Genre(name="Action")
#drame = Genre(name="Drama")

#dob=datetime(year=1941, month=3, day= 13)
#author1=Authors(name="Mahmoud Darwish", dob=dob, nat="Palestinian", lang="Arabic")
book=Books(name="Unfortunately, it was paradise", authorid=1, lang="Arabic", nat="Palestinian", picture="paradise.jpeg")

#session.add(comedy)
#session.add(action)
#session.add(drame)
session.add(book)
#session.add(author1)



session.commit()

