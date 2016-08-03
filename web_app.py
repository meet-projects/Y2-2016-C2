from flask import Flask, render_template
app = Flask(__name__)

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#YOUR WEB APP CODE GOES HERE
@app.route('/')
def main():
	return render_template('main_page.html')

@app.route('/nationalities')
def Nationalities():
	books = session.query(Books).filter_by(nat="Palestinian").all()
	return render_template("nationality.html", books=books)



@app.route('/genres')
def Genres():
	return

@app.route('/login')
def Signin():
	return render_template('SignIn.html')
 

@app.route('/book/<int:book_id>')
def book(book_id):
	book=session.query(Books).filter_by(id=book_id).one()
	author=session.query(Authors).filter_by(id=book.authorid).one()
	return render_template("view_book.html", book=book, author=author)





if __name__ == '__main__':
    app.run(debug=True)
