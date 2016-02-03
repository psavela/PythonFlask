from app import app

#render_template gives you access to Jinj2 template
from flask import render_template,request,make_response,flash,redirect,session
from app.forms import LoginForm,RegisterForm,FriendForm
from app.db_models import Users,Friends
from app import db


@app.route('/',methods=['GET','POST'])
def index():
    login = LoginForm()
    #Check if get method
    if request.method == 'GET':
        return render_template('template_index.html',form=login,isLogged=False)
    else:
        #check if form data is valid
        if login.validate_on_submit():
            #Check if correct username and password
            user = Users.query.filter_by(email=login.email.data).filter_by(passw=login.passw.data)
            print(user)
            if user.count() == 1:
                print(user[0])
                session['user_id'] = user[0].id
                session['isLogged'] = True
                #tapa1
                friends = Friends.query.filter_by(user_id=user[0].id)
                print(friends)
                return render_template('template_user.html',isLogged=True,friends=friends)
            else:
                flash('Wrong email or password')
                return render_template('template_index.html',form=login,isLogged=False)
        #form data was not valid
        else:
            flash('Give proper information to email and password fields')
            return render_template('template_index.html',form=login,isLogged=False)


@app.route('/register',methods=['GET','POST'])
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
            
        
@app.route('/user/<name>')
def user(name):
    print(request.headers.get('User-Agent'))
    return render_template('template_user.html',name=name)

#Example how you can define route methods
@app.route('/user',methods=['GET','POST'])
def userParams():
    name = request.args.get('name')
    return render_template('template_user.html',name=name)


@app.route('/friends',methods=['GET','POST'])
def friends():
	#Check that user has logged in before you let execute this route
	if not('isLogged' in session) or (session['isLogged'] == False):
		return redirect('/')
	form = FriendForm()
	if request.method == 'GET':
		return render_template('template_friends.html',form=form,isLogged=True)
	else:
		if form.validate_on_submit():
			temp = Friends(form.name.data,form.address.data,form.age.data,session['user_id'])
			db.session.add(temp)
			db.session.commit()
			#tapa 2
			user = Users.query.get(session['user_id'])
			print(user.friends)
			return render_template('template_user.html',isLogged=True,friends=user.friends)
		else:
			flash('Give proper values to all fields')
			return render_template('template_friends.html',form=form,isLogged=True)
	

@app.route('/logout')
def logout():
    #delete user session (clear all values)
    session.clear()
    return redirect('/')
        
#print('This is not any more included in index() function. Huom this is my own print')

#This is one line comment
"""This is multiple
line comment"""