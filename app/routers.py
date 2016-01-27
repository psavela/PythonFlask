from app import app
#render_template gives you access to Jinj2 template
from flask import render_template,request, make_response

@app.route('/')
def index():
    name = 'Petri'
    address = 'Oulu'
    response = make_response(render_template('template_index.html',name=name,title=address))
    response.headers.add('Cache-Control','no-cache')
    return response

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