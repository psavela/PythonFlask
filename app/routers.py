from app import app

#render_template gives you access to Jinj2 template
from flask import render_template,request, make_response,flash,redirect
from app.forms import LoginForm, RegisterForm, RegisterForm
from app.db_models import Users
from app import db

@app.route('/',methods=['GET','POST'])
def index():
    login = LoginForm()
    #Check if get method
    if request.method == 'GET':
        return render_template('template_index.html',form=login)
    else:
        #check if form data is valid
        if login.validate_on_submit():
            print(login.email.data)
            print(login.passw.data)
            return render_template('template_user.html')
        #form data was not valid
        else:
            flash('Give proper information to email and password fields')
            return render_template('template_index.html',form=login)


@app.route('/register',methods=['GET','POST'])
def registerUser():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('template_register.html',form=form)
    else:
        if form.validate_on_submit():
            user = Users(form.email.data,form.passw.data)
            db.session.add(user)
            db.session.commit()
            flash("Name {0} registered".format(form.email.data))
            return redirect('/')
        else:
            flash('Invalid email address or no password given')
            return render_template('template_register.html',form=form)
            

        
@app.route('/user/<name>')
def user(name):
    print(request.headers.get('User-Agent'))
    return render_template('template_user.html',name=name)

#Example how you can define route methods
@app.route('/user',methods=['GET','POST'])
def userParams():
    name = request.args.get('name')
    return render_template('template_user.html',name=name)

#print('This is not any more included in index() function. Huom this is my own print')

#This is one line comment
"""This is multiple
line comment"""