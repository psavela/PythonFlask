from flask import Blueprint,session,redirect,request,render_template,url_for,flash
from app.forms import FriendForm
from app import db
from app.db_models import Users,Friends
from werkzeug import secure_filename
#Create blueprint
#First argument is the name of the blueprint folder
#second is always __name__ attribute
#third parameter tells what folder contains your templates
ud = Blueprint('ud',__name__,template_folder='templates',url_prefix=('/app/'))

#/app/delete
@ud.route('delete/<int:id>')
def delete(id):
	friend = Friends.query.get(id)
	db.session.delete(friend)
	db.session.commit()
	user = Users.query.get(session['user_id'])
	return render_template('template_user.html',isLogged=True,friends=user.friends)

@ud.route('update/<int:id>')
def update():
    return "Update"

@ud.route('friends',methods=['GET','POST'])
def friends():
	form = FriendForm()
	if request.method == 'GET':
		return render_template('template_friends.html',form=form,isLogged=True)
	else:
		if form.validate_on_submit():
		
			temp = Friends(form.name.data,form.address.data,form.age.data,session['user_id'])
			#Save the image if present
			if form.upload_file.data:
				filename = secure_filename(form.upload_file.data.filename)
				form.upload_file.data.save('app/static/images/' + filename)
				temp.filename = '/static/images/' + filename
			db.session.add(temp)
			db.session.commit()
			#tapa 2
			user = Users.query.get(session['user_id'])
			friends = Friends.query.filter_by(user_id=user.id).paginate(1,10,False)
			return render_template('template_user.html',isLogged=True,friends=friends)
		else:
			flash('Give proper values to all fields')
			return redirect(url_for('ud.friends'))
	

def before_request():
    if not 'isLogged' in session:
        return redirect('/')
    
ud.before_request(before_request)
        