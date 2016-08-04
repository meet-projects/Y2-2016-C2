from flask import Flask, render_template, request , redirect, url_for
app = Flask(__name__)

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews, association_table,Genre,UserToGenre

from datetime import datetime

from sqlalchemy import create_engine, desc

from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



#YOUR WEB APP CODE GOES HERE
@app.route('/')
def main():
	return render_template('index.html')




@app.route('/home/<int:user>')
def home(user):
	user=session.query(Users).filter_by(id=user).first()
	return render_template('home.html', user=user)

@app.route('/nationalities')
def Nationalities():
	booksp = session.query(Books).filter_by(nat="Palestinian").all()
	booksi = session.query(Books).filter_by(nat="Israeli").all()
	return render_template("nationality.html", booksp=booksp, booksi=booksi)


@app.route('/login', methods=['GET', 'POST'])
def Signin():
	if (request.method=='POST'):
		password=request.form['password']
		email=request.form['email']
		results=session.query(Users).filter_by(password=password, email=email).all()
		if (len(results)>0):
			return redirect(url_for('home', user=results[0].id))
		else:
			return render_template('SignIn.html')
	return render_template("SignIn.html")
 
@app.route('/signout')
def Signout():
	return redirect(url_for('main'))

@app.route('/book/<int:book_id>')
def book(book_id):
	book=session.query(Books).filter_by(id=book_id).one()
	author=session.query(Authors).filter_by(id=book.authorid).one()
	return render_template("view_book.html", book=book, author=author)



@app.route('/author')
def author(user, author):
	books = session.query(Books).all()
	authors = session.query(Authors).all()
	return render_template('author.html', authors=authors, books=books)


@app.route('/settings/<int:user>', methods=['GET', 'POST'])
def settings(user):
	User=session.query(Users).filter_by(id=user).first()
	if (request.method=='POST' and request.form['confpass']==User.password):
		if (request.form['password']==request.form['confpassword']):
			User.password=request.form['password']
		User.name=request.form['name']
		User.email=request.form['email']
		User.nat=request.form['nat']
		session.commit()
		return redirect(url_for('main'))
	return render_template('settings.html', user=User.id)



@app.route('/history/<int:user>')
def history(user):
	user=session.query(Users).filter_by(id=user).one()
	books=session.query(association_table).filter_by(user_id=user.id).all()
	booksp=[]
	booksi=[]
	print(len(books))
	return render_template('history.html', user=user, booksp=booksp, booksi=booksi)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	if request.method == 'GET':
		genres=session.query(Genre).all()
		return render_template("SignUp.html", genres=genres)
	else:
		print(request.form)
		new_name = request.form['name']
		new_email = request.form['email']
		new_password = request.form['password']
		new_day = request.form['day']
		new_month = request.form['month']
		new_year = request.form['year']
		new_nat = request.form['nat']
		new_dob =  datetime(year=int(new_year), month=int(new_month), day=int(new_day))
	#	new_dob = datetime.strptime(new_day+' '+new_month+' '+new_year,'%b %d %Y')

		user = Users(name = new_name, email = new_email, password = new_password, dob = new_dob , nat = new_nat)
		session.add(user)
		session.commit()
		for g_id in request.form['genres']:
			user_to_genre=UserToGenre(user_id=user.id,genre_id=g_id)
			session.add(user_to_genre)
	
		session.commit()
		

		return redirect(url_for('main'))

@app.route('/genres')
def Genres(user):
	if (user!=0):
		user=session.query(Users).filter_by(id=user).first()
	genres = session.query(Genre).all()
	return render_template('genre.html', genres=genres)


if __name__ == '__main__':
    app.run(debug=True)
