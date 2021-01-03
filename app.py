from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
# from bson import ObjectId
from pymongo import MongoClient
# from console_log import ConsoleLog
import os
import logging

app = Flask(__name__)
Bootstrap(app)

logger = logging.getLogger('werkzeug')
# console = logging.getLogger('console')
# console.setLevel(logging.DEBUG)

title = "TODO application with Flask and pymongo"
heading = "TODO reminder with Flask and pymongo"

client = MongoClient("mongodb://localhost:27017")
# Can also be written as:
# client = MongoClient('localhost', 27017)
db = client.projecttrackerdb
# Can also be written as:
# db = client['projecttrackerdb'] -> the dictionary-style
# projects = db.projects
# project_data = {
#     'title' : 'inserttitlehere',
#     'task': [
#         0
#     }]

#     }
# }

def redirect_url():
#   return request.args.get('next') or \
#   request.referrer or \
    url_for('index')

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    addToDatabase()
    return render_template('index.html')
    # return "Hello World!"

def addToDatabase():
    logger.info(client.list_database_names())
    # logger.info('Info logged from Python')
    # print(client.list_database_names())
    return

if __name__ == '__main__':
    app.run(debug=True)

# app.wsgi_app = ConsoleLog(app.wsgi_app, console)



@app.route("/projects")
@app.route("/tasks")
def projects():
    addToDatabase()
    return render_template('projects.html')