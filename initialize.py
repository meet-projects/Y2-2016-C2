from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Users, Books, Authors, Reviews, Genre, BookToGenre, UserToGenre
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
dob2=datetime(year=1971, month=12, day=31)
author2=Authors(name="Liad Shoham", dob=dob2, nat="Israeli", lang="Hebrew", picture="liad_shoham.png")
dob3=datetime(year=1971, month=1, day=1)
author3=Authors(name="Nevo Eshkol", dob=dob3, nat="Israeli", lang="Hebrew", picture="nevo_eshkol.png")
dob4=datetime(year=1980, month=12, day=27)
author4=Authors(name="Shai Amit", dob=dob4, nat="Israeli", lang="Hebrew", picture="shai_amit.png")
dob5=datetime(year=1963, month=11, day=5)
author5=Authors(name="Yair Lapid", dob=dob5, nat="Israeli", lang="Hebrew", picture="yair_lapid.png")
dob6=datetime(year=1952, month=3, day=22)
author6=Authors(name="Mishka Ben David", dob=dob6, nat="Israeli", lang="Hebrew", picture="mishka_ben_david.png")

book=Books(name="Unfortunately, it was paradise", authorid=1, lang="Arabic", nat="Palestinian", picture="paradise.jpeg")
book2=Books(name="Journal of an Ordinary Grief", authorid=1, lang="Arabic", nat="Palestinian", picture="grief.jpeg")
book3=Books(name="LINE UP HB", authorid=2, lang="Hebrew", nat="Israeli", picture="line_up_hb.png")
book4=Books(name="Neuland", authorid=3, lang="Hebrew", nat="Israeli", picture="neuland.png")
book5=Books(name="Tender", authorid=4, lang="Hebrew", nat="Israeli", picture="tender.png")
book6=Books(name="MEMORIES AFTER MY DEATH", authorid=5, lang="Hebrew", nat="Israeli", picture="memories_after_my_death.png")
book7=Books(name="DUET IN BEIRUT", authorid=6, lang="Hebrew", nat="Israeli", picture="duet_in_beirut.png")

bookrel=BookToGenre(book_id=1, genre_id=3)
book2rel=BookToGenre(book_id=2, genre_id=3)
#book3rel=BookToGenre(book_id=3, genre_id=)
#book4rel=BookToGenre(book_id=4, genre_id=)
#book5rel=BookToGenre(book_id=5, genre_id=)
#book6rel=BookToGenre(book_id=6, genre_id=)
#book7rel=BookToGenre(book_id=7, genre_id=)

session.add(comedy)
session.add(action)
session.add(drame)
session.add(book)
session.add(book2)
session.add(author1)
session.add(bookrel)
session.add(book2rel)
session.add(author2)
session.add(author3)
session.add(author4)
session.add(author5)
session.add(author6)
session.add(book3)
session.add(book4)
session.add(book5)
session.add(book6)
session.add(book7)
#session.add(book3rel)
#session.add(book4rel)
#session.add(book5rel)
#session.add(book6rel)
#session.add(book7rel)


session.commit()

