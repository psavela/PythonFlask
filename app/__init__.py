from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
#Näin pystyy conffaan suoraan ilman erillistä config fileä
#app.config([SERVER_NAME]='localhost:3000') 
#This lines configures our app using the config.py file
app.config.from_object('config')
bootstrap = Bootstrap(app)
from app import routers