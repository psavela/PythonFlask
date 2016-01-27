from flask import Flask

app = Flask(__name__)
#Näin pystyy conffaan suoraan ilman erillistä config fileä
#app.config([SERVER_NAME]='localhost:3000') 
#This lines configures our app using the config.py file
app.config.from_object('config')
from app import routers