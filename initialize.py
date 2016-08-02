from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Users, Books, Authors, Reviews
from datetime import datetime

engine = create_engine('sqlite:///crudlab.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# You can add some starter data for your database here.

dob=datetime(year=2000, month=8, day=23)
booik1=Books(name="Hunger", type1="Action", type2="Comedy", type3="N/A", type4="N/A", type5="N/A", lang="Arabic", nat="Palestinian")
session.add(booik1)
test=Users(name="test", email="george17@meet.mit.edu", password="123", dob=dob, int1="Action", int2="Comedy", int3="N/A", int4="N/A", int5="N/A", nat="Palestinian")
session.add(test)
session.commit()