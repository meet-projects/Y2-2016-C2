from flask import Flask, render_template, request , redirect, url_for, session
app = Flask(__name__)
app.secret_key="this is my project"
# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews,Genre,UserToGenre, BooksToReviews, UserToReviews, ReadBooks

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
	readbooks=dbsession.query(ReadBooks).filter_by(user=user.id).all()

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
	if (request.method=='GET'):
		author=dbsession.query(Authors).filter_by(id=book.authorid).first()
		bookreviews=dbsession.query(BooksToReviews).filter_by(book=book.id).all()
		revusers=[]
		reviews=[]
		users=[]
		i=0
		if (bookreviews is not None):
			for review in bookreviews:
				reviews.append(dbsession.query(Reviews).filter_by(id=review.id).first())
				revusers.append(dbsession.query(UserToReviews).filter_by(review=review.id).first())
				users.append(Query(revusers[i].id))
				i+=1
		
		#reviews=dbsession.query(Reviews).filter_by().all()
		return render_template("view_book.html", book=book, author=author, user=user, reviews=reviews, users=users)

	else:
		if ('read' not in request.form):
			if (request.form['mark'] is not None):
				read=ReadBooks(user=session['user'], book=book.id)
				dbsession.add(read)
				dbsession.commit()
			return redirect(url_for('book', book_id=book.id))



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
	history=dbsession.query(ReadBooks).filter_by(user=user.id).all()
	booksi=[]
	booksp=[]
	if (history is not None):
		i=len(history)-1
		while (len(booksi)<5 and len(booksp)<5 and i>=0):
			book=dbsession.query(Books).filter_by(id=history[i].book).first()
			if (book.nat=="Palestinian"):
				booksp.append(book)
			else:
				booksi.append(book)
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


@app.route('/review/<int:book>', methods=['POST'])
def Review(book):
	user=Query(session['user'])	
	rating=request.form['rating']
	revtext=request.form['review']
	bookrev=dbsession.query(BooksToReviews).filter_by(book=book).all()
	reviewed=dbsession.query(UserToReviews).filter_by(user=user.id).all()
	for review in reviewed:
		if (review in reviewed):
			return redirect(url_for('book', book_id=book))
	review=Reviews(rating=rating, review=revtext)
	dbsession.add(review)
	dbsession.commit()
	review=dbsession.query(Reviews).filter_by(rating=rating, review=revtext).first()
	revuser=UserToReviews(user=user.id, review=review.id)
	revbook=BooksToReviews(book=book, review=review.id)
	dbsession.add(revuser)
	dbsession.add(revbook)
	dbsession.commit()
	return redirect(url_for('book', book_id=book))

def Query(id):
	return dbsession.query(Users).filter_by(id=id).first()

if __name__ == '__main__':
	app.run(debug=True)
