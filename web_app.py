from flask import Flask, render_template, request , redirect, url_for, session
app = Flask(__name__)
app.secret_key="this is my project"
# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews, association_table,Genre,UserToGenre, BooksToReviews, UserToReviews

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
	sortedlist=[]
	for book in books:
		if (book.nat!=user.nat):
			sortedlist.append(book)
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

@app.route('/book/<int:book_id>', methods=['POST', 'GET'])
def book(book_id):
	user=Query(session['user'])
	book=dbsession.query(Books).filter_by(id=book_id).first()
	if request.method=='GET':
		author=dbsession.query(Authors).filter_by(id=book.authorid).first()
		bookreviews=dbsession.query(BooksToReviews).filter_by(book=book.id).all()
		reviews=[]
		for review in bookreviews:
			reviews.append(dbsession.query(Reviews).filter_by(id=review.id))
		#reviews=dbsession.query(Reviews).filter_by(book.id=book.id)
		return render_template("view_book.html", book=book, author=author, user=user, reviews=reviews)
	else:
		rating=request.form['rating']
		revtext=request.form['review']
		reviewmain=Reviews(rating=rating, review=revtext, book=book)
		dbsession.add(reviewmain)
		userreview=UserToReviews(user=session['user'], review=)
		dbsession.commit()



@app.route('/author/<int:author>')
def author(author):
	user=Query(session['user'])
	author=dbsession.query(Authors).filter_by(id=author).first()
	books=dbsession.query(Books).filter_by(authorid=author.id).all()
	return render_template('author.html', author=author, user=user, books=books)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
	user=Query(session['user'])
	if (request.method=='POST'):
		if (request.form['confpass']==user.password):
			if (request.form['password']==request.form['confpassword'] and request.form['password']!=""):
				user.password=request.form['password']
			user.name=request.form['name']
			user.email=request.form['email']
			user.nat=request.form['nat']
			dbsession.commit()
			return redirect(url_for('settings', user=user))
	return render_template('settings.html', user=user)



@app.route('/history')
def history():
	user=Query(session['user'])
	books=dbsession.query(association_table).filter_by(user_id=user.id).all()
	booksp=[]
	booksi=[]
	i=len(books)-1
	while (len(booksp)<5 and len(booksi)<5 and i>len(books)):
		isread=dbsession.query(association_table).filter_by(user_id=user.id, book_id=books[i].id).all()
		if (books[i].nat=="Palestinian" and books[i] not in isread):
			booksp.append(books[i])
		elif (books[i].nat=="Israeli" and books[i] not in isread):
			booksi.append(books[i])
		i-=1
	return render_template('history.html', user=user, booksp=booksp, booksi=booksi)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	genres=dbsession.query(Genre).all()
	if request.method == 'POST':
		if (dbsession.query(Users).filter_by(email=request.form['email']).first()==None):
			name=request.form['name']
			email=request.form['email']
			password=request.form['password']
			dob=datetime(year=int(request.form['year']), month=int(request.form['month']), day=int(request.form['day']))
			nat=request.form['nat']
			user=Users(name=name, email=email, dob=dob, password=password, nat=nat)
			dbsession.add(user)
			dbsession.commit()
			id=dbsession.query(Users).filter_by(email=email).first().id
			genres=request.form.getlist('genres')
			for genre in genres:
				genreob=UserToGenre(user_id=id, genre_id=int(genre))
				dbsession.add(genreob)
				dbsession.commit()
			return redirect(url_for("Signin"))
	return render_template("SignUp.html", genres=genres)

@app.route('/genres/')
def Genres():
	genres = dbsession.query(Genre).all()
	user=Query(session['user'])
	return render_template('genre.html', user=user, genres=genres)


def Query(id):
	return dbsession.query(Users).filter_by(id=id).first()

if __name__ == '__main__':
	app.run(debug=True)
