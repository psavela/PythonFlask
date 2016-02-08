from flask import Blueprint,render_template,flash,request,redirect,session
from app.forms import LoginForm,RegisterForm
from app.db_models import Users,Friends
from app import db
from flask.ext.bcrypt import check_password_hash

auth = Blueprint('auth',__name__,template_folder='templates')

@auth.route('/index/<int:page>',methods=['GET','POST'])
@auth.route('/',methods=['GET','POST'])
def index(page=1):
	login = LoginForm()
	if request.method == 'GET' and 'user_id' in session:
		friends = Friends.query.filter_by(user_id=session['user_id']).paginate(page,10,False)
		return render_template('template_user.html',isLogged=True,friends=friends)
	#Check if get method
	if request.method == 'GET':
		return render_template('template_index.html',form=login,isLogged=False)
	else:
		#check if form data is valid
		if login.validate_on_submit():
			#Check if correct username
			user = Users.query.filter_by(email=login.email.data)
			print(user)
			if (user.count() == 1) and (check_password_hash(user[0].passw,login.passw.data)):
				print(user[0])
				session['user_id'] = user[0].id
				session['isLogged'] = True
				#tapa 1
				friends = Friends.query.filter_by(user_id=user[0].id).paginate(page,10,False)
				print(friends)
				return render_template('template_user.html',isLogged=True,friends=friends)
			else:
				flash('Wrong email or password')
				return render_template('template_index.html',form=login,isLogged=False)
		#form data was not valid
		else:
			flash('Give proper information to email and password fields!')
			return render_template('template_index.html',form=login,isLogged=False)

@auth.route('/register',methods=['GET','POST'])
def registerUser():
	form = RegisterForm()
	if request.method == 'GET':
		return render_template('template_register.html',form=form,isLogged=False)
	else:
		if form.validate_on_submit():
			user = Users(form.email.data,form.passw.data)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				db.session.rollback()
				flash('Username allready in use')
				return render_template('template_register.html',form=form,isLogged=False)
			flash("Name {0} registered.".format(form.email.data))
			return redirect('/')
		else:
			flash('Invalid email address or no password given')
			return render_template('template_register.html',form=form,isLogged=False)
	

@auth.route('/logout')
def logout():
	#delete user session (clear all values)
	session.clear()
	return redirect('/')