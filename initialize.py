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

comedy = Genre(name="Comedy")
action = Genre(name="Action")
drame = Genre(name="Drama")

session.add(comedy)
session.add(action)
session.add(drame)

dob=datetime(year=2000, month=8, day=23)
author=Authors(name="test", dob=dob, nat="Something", lang="Unknown", picture="hitham.png")
session.add(author)
booik1=Books(name="Hunger", authorid=1, picture="test.png", type1="Action", type2="Comedy", type3="N/A", type4="N/A", type5="N/A", lang="Arabic", nat="Palestinian")
session.add(booik1)

booik1.genres = [comedy, action]

test=Users(name="test", email="george17@meet.mit.edu", password="123", dob=dob, int1="Action", int2="Comedy", int3="N/A", int4="N/A", int5="N/A", nat="Palestinian")
session.add(test)
session.commit()

print comedy.books
print booik1.genres
