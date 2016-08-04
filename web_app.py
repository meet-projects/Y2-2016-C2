from flask import Flask, render_template, request , redirect, url_for
app = Flask(__name__)

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base, Books, Users, Authors, Reviews, association_table

from datetime import datetime
from sqlalchemy import create_engine

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



@app.route('/genres')
def Genres():
	return

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
def author():
	books = session.query(Books).all()
	authors = session.query(Authors).all()
	return render_template('author.html', authors=authors, books=books)

@app.route('/history/<int:user>')
def history(user):
	user=session.query(Users).filter_by(id=user).one()
	books=session.query(association_table).filter_by(user_id=user.id).all()
	booksp=[]
	booksi=[]
	i=len(books)-1
	pcur=0
	icur=0
	while (len(booksp)<5 and len(booksi)<5):
		if (books[i].nat=="Palestinian"):
			booksp.append(books[i])
			pcur+=1
		else:
			booksi.append(books[i])
			icur+=1
		i-=1
	return render_template('history.html', user=user, booksp=booksp, booksi=booksi)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	if request.method == 'GET':
		return render_template("SignUp.html")
	else:
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
		

		return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)
