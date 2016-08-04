from flask import Flask, render_template, request , redirect, url_for, session
app = Flask(__name__)
app.secret_key="this is my project"
# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews, association_table,Genre,UserToGenre

from datetime import datetime

from sqlalchemy import create_engine, desc, asc

from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()



#YOUR WEB APP CODE GOES HERE
@app.route('/')
def main():
	return render_template('index.html')




@app.route('/home')
def home():
	user=Query(session['user'])
	readbooks=dbsession.query(association_table).filter_by(user_id=user.id).all()

	books=dbsession.query(Books).all()
	for book in books:
		if (book.nat!=user.nat):
			sortedlist.append(book)
	sortedlist=sorted(books)
	return render_template('home.html', user=user, books=sortedlist)

@app.route('/nationalities')
def Nationalities():
	user=Query(session['user'])
	booksp = dbsession.query(Books).filter_by(nat="Palestinian").all()
	booksi = dbsession.query(Books).filter_by(nat="Israeli").all()
	return render_template("nationality.html", booksp=booksp, booksi=booksi, user=user)


@app.route('/login', methods=['GET', 'POST'])
def Signin():
	if (request.method=='POST'):
		password=request.form['password']
		email=request.form['email']
		results=dbsession.query(Users).filter_by(password=password, email=email).first()
		if (results != None):
			session['user'] = results.id
			return redirect(url_for('home'))
		else:
			return render_template('SignIn.html')
	return render_template("SignIn.html")
 
@app.route('/signout')
def Signout():
	session['user']=None
	return redirect(url_for('main'))

@app.route('/book/<int:book_id>')
def book(book_id):
	book=dbsession.query(Books).filter_by(id=book_id).one()
	author=dbsession.query(Authors).filter_by(id=book.authorid).one()
	return render_template("view_book.html", book=book, author=author)



@app.route('/author')
def author(user, author):
	books = dbsession.query(Books).all()
	authors = dbsession.query(Authors).all()
	return render_template('author.html', authors=authors, books=books)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
	user=Query(session['user'])
	if (request.method=='POST'):
		if (request.form['confpass']==user.password):
			if (request.form['password']==request.form['confpassword']):
				user.password=request.form['password']
			user.name=request.form['name']
			user.email=request.form['email']
			user.nat=request.form['nat']
			dbsession.commit()
			return redirect(url_for('main'))
	return render_template('settings.html', user=user)



@app.route('/history')
def history():
	user=Query(session['user'])
	books=dbsession.query(association_table).filter_by(user_id=user.id).all()
	booksp=[]
	booksi=[]
	i=len(books)-1
	while (len(booksp)<5 and len(booksi)<5 and i>len(books)):
		isread=dbsession.query(association_table).filter_by(user_id=user.id, book_id=books[i].id).scalar()
		if (not isread):
			if (books[i].nat=="Palestinian"):
				booksp.append(books[i])
			else:
				booksi.append(books[i])
		i-=1
	return render_template('history.html', user=user, booksp=booksp, booksi=booksi)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	if request.method == 'GET':
		genres=dbsession.query(Genre).all()
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
	#   new_dob = datetime.strptime(new_day+' '+new_month+' '+new_year,'%b %d %Y')

		user = Users(name = new_name, email = new_email, password = new_password, dob = new_dob , nat = new_nat)
		dbsession.add(user)
		dbsession.commit()
		for g_id in request.form['genres']:
			user_to_genre=UserToGenre(user_id=user.id,genre_id=g_id)
			dbsession.add(user_to_genre)
	
		dbsession.commit()
		

		return redirect(url_for('Signin'))

@app.route('/genres/')
def Genres():
	genres = dbsession.query(Genre).all()
	user=Query(session['user'])
	return render_template('genre.html', user=user, genres=genres)


def Query(id):
	return dbsession.query(Users).filter_by(id=id).first()

if __name__ == '__main__':
	app.run(debug=True)
