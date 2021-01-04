from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField
from wtforms.widgets import TextArea
from wtforms import TextAreaField
from wtforms.validators import DataRequired
# from bson import ObjectId
from pymongo import MongoClient
# from console_log import ConsoleLog
import os
import logging

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ty4425hk54a21eee5719b9s9df7sdfklx'

class PostForm(Form):
    taskbody = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
    csrf_enabled = False

# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])

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
    listDatabase()
    return render_template('index.html')
    # return "Hello World!"

def listDatabase():
    logger.info(client.list_database_names())
    # logger.info('Info logged from Python')
    # print(client.list_database_names())
    return

def addToDatabase(task):
    mydict = { "name" : task }
    # tasks = db.projects['task'][0]
    tasks = db.projects
    x = tasks.insert_one(mydict)
    logger.info(x)
    return

def updateDatabase(task):
    mydict = { "name" : task }
    tasks = db.projects
    tasks.updateOne(
        { 'task' : }
    )


if __name__ == '__main__':
    app.run(debug=True)

# app.wsgi_app = ConsoleLog(app.wsgi_app, console)



@app.route("/projects")
@app.route("/dashboard")
def projects():
    lizzie = list(db.projects.find({}))
    # for i in lizzie[0]['task']:
    #     logger.info(i['name'])
        # logger.info(lizzie[0]['task'][i])
    # logger.info(lizzie[0]['task'])
    projects = lizzie[0]['task']
    form = PostForm()
    return render_template('dashboard.html', projects = projects, form = form)

@app.route("/actiontask", methods=('GET', 'POST'))
def tasks():
    # form = ContactForm()
    lizzie = list(db.projects.find({}))
    tasks = lizzie[0]['task']
    form = PostForm(request.form)
    # logger.info(PostForm.taskbody)
    # logger.info(form.validate_on_submit())
    if form.validate_on_submit():
        # flash('Blah'.format(form.taskbody.data))
        newtask = form.taskbody.data
        # newtask = request.get_json().get('addtask', '')
        # newtask = request.data
        # newtask = request.data.decode('UTF-8')
        logger.info(newtask)
        updateDatabase(newtask)
        # logger.info(PostForm.taskbody)
        # newtask = request.form.get('addtask')
    # mytask = request.form['quicktask']
    return render_template('dashboard.html', projects = tasks, form = form)


# var =request.get_json().get('stuff', '')

# def getProject():
# #     return db.projects.find()

# @app.route('/actiontask', methods=('GET', 'POST'))
# def postform():
#     form = PostForm()
#     # if form.validate_on_submit():
#     #     return redirect(url_for('success'))
#     return render_template(
#         'index.html',
#         form=form
#     )


