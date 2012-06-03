#!/usr/bin/env python2.7

## all the imports
import sqlite3
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
## configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

## http://flask.pocoo.org/docs/tutorial/dbinit/#tutorial-dbinit
## call by starting a python shell and running
## >>> from flaskr import init_db
## >>> init_db()
from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

app = Flask(__name__)
app.config.from_object(__name__)
## override configuration if envvar  FLASKR_SETTINGS  set:
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = app.config['USERNAME']
            flash('Log in erfolgreich.')
            return redirect(url_for('show_resolutions'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logout erfolgreich.')
    return redirect(url_for('show_resolutions'))

@app.route('/')
def show_resolutions():
    cur = g.db.execute('SELECT title, text, kind, passed_on, wiki_url, related_file FROM resolutions ORDER BY passed_on DESC')
    resolutions = [dict(title=row[0], text=row[1], kind=row[2],
        passed_on=row[3], wiki_url=row[4], related_file=row[5])
        for row in cur.fetchall()]
    return render_template('show_resolutions.html', resolutions=resolutions)

@app.route('/add', methods=['POST'])
def add_resolution():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into resolutions (title, text, kind, passed_on, entered_by, entered_on, wiki_url, related_file) values (?, ?, ?, ?, ?, ?, ?, ?)', [
                request.form['title'], request.form['text'], request.form['kind'],
                request.form['passed_on'], session['username'],
                datetime.now().isoformat(), request.form['wiki_url'],
                request.form['related_file']
                ] )
    g.db.commit()
    flash('Neue(r) %s erfolgreich eingetragen.' % request.form['kind'])
    return redirect(url_for('show_resolutions'))

if __name__ == "__main__":
    app.run()
    #app.run(host='0.0.0.0')
