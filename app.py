from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.widgets import TextArea
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ty4425hk54a21eee5719b9s9df7sdfklx'

class PostForm(FlaskForm):
    taskbody = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
    csrf_enabled = False

logger = logging.getLogger('werkzeug')

title = "TODO application with Flask and pymongo"
heading = "TODO reminder with Flask and pymongo"

client = MongoClient("mongodb://localhost:27017")
db = client.projecttrackerdb

def redirect_url(): 
    url_for('index')

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    listDatabase()
    return render_template('index.html')

def listDatabase():
    logger.info(client.list_database_names())
    return

def addToDatabase(task):
    mydict = { "name" : task }
    tasks = db.projects
    x = tasks.insert_one(mydict)
    logger.info(x)
    return

def addToCompleted(task):
    mydict = { "name" : task }
    tasks = db.completedProjects
    x = tasks.insert_one(mydict)
    return

def updateDatabase(task):
    mydict = { "name" : task }
    tasks = db.projects
    tasks.updateOne(
        { 'task' : task }
    )

def deleteProject(project):
    query = { "name" : project }
    db.projects.delete_one(query)
    return

def completeProject(project):
    addToCompleted(project)
    deleteProject(project)
    return

def deleteCompletedProject(project):
    query = { "name" : project }
    db.completedProjects.delete_one(query)
    logger.info("HELP")
    return


if __name__ == '__main__':
    app.run(debug=True)

@app.route("/projects")
@app.route("/dashboard")
def projects():
    lizzie = list(db.projects.find({}, {'_id': False}))
    completed = list(db.completedProjects.find({}, {'_id': False}))
    try:
            projects = lizzie
    except:
        projects = []
    form = PostForm()
    return render_template('dashboard.html', projects = projects, completed = completed, form = form)

@app.route("/actiontask", methods=('GET', 'POST'))
def tasks():
    form = PostForm(request.form)
    if form.validate_on_submit():
        newtask = form.taskbody.data
        logger.info(newtask)
        addToDatabase(newtask)
    lizzie = list(db.projects.find({}, {'_id': False}))
    completed = list(db.completedProjects.find({}, {'_id': False}))
    try:
            projects = lizzie
    except:
        projects = []
    return render_template('dashboard.html', projects = projects, completed = completed, form = form)

@app.route("/deletetask/<path:taskname>", methods=('GET', 'POST'))
def deletetask(taskname):
    logger.info(taskname)
    deleteProject(taskname)
    return redirect("/dashboard")

@app.route("/completetask/<path:taskname>", methods=('GET', 'POST'))
def completetask(taskname):
    logger.info(taskname)
    completeProject(taskname)
    return redirect("/dashboard")

@app.route("/deletecompletedtask/<path:taskname>", methods=('GET', 'POST'))
def deletecompletedtask(taskname):
    logger.info(taskname)
    logger.info("WTF")
    deleteCompletedProject(taskname)
    return redirect("/dashboard")

