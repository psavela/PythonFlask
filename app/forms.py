from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import Required,Email

class LoginForm(Form):
    email = StringField('Enter your email',validators=[Required(),Email()])
    passw = PasswordField('Enter password',validators=[Required()])
    submit = SubmitField('Login');

class RegisterForm(Form):
    email = StringField('Enter your email',validators=[Required(),Email()])
    passw = PasswordField('Enter password',validators=[Required()])
    submit = SubmitField('Register');
	
class AddFriendForm(Form):
    name = StringField('Enter friend´s name',validators=[Required()])
    address = StringField('Enter friend´s address',validators=[Required()])
    age = IntegerField('Enter friend´s age',validators=[Required()])
    submit = SubmitField('Add new friend')
