from flask import Flask, g, url_for, request, render_template, make_response, abort, \
    session, redirect, jsonify, escape
import sqlite3

from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.before_request
def Before_Request():
    g.database = sqlite3.connect('User_data.db')
    g.cursor = g.database.cursor()


@app.after_request
def After_Request(response):
    g.cursor.close()
    g.database.commit()
    g.database.close()
    return response


@app.route('/')
def index():
    ID = None
    articles = None
    if 'ID' in session:
        ID = session['ID']
        g.cursor.execute('SELECT * FROM ' + session['ID'])
        articles = g.cursor.fetchall()
    return render_template('index.html', ID=ID, articles=articles)


@app.route('/write_blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'GET':
        return render_template('write_blog.html', ID=session['ID'])
    else:
        s = 'INSERT INTO ' + session['ID'] + ' values(\'' + \
            request.form['title'] + '\',\'' + \
            request.form['content'] + '\');'
        g.cursor.execute(s)
        return redirect(url_for('index', ID=session['ID']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    g.cursor.execute('SELECT * FROM users')
    Users = g.cursor.fetchall()
    if request.method == 'POST' and (request.form['ID'], request.form['Password']) in Users:
        session['ID'] = request.form['ID']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('ID')
    return redirect(url_for('index'))


@app.route('/delete_article')
def delete_article():
    title = request.args.get('title')
    ID = session['ID']
    g.cursor.execute('DELETE FROM ' + ID + '  WHERE title = \'' + title + '\';')
    return redirect(url_for('index', ID=session['ID']))


@app.route('/article_detail')
def article_detail():
    title = request.args.get('title')
    g.cursor.execute('SELECT * FROM ' + session['ID'] + ' WHERE title=' + title)
    article = g.cursor.fetchall()[0]
    return render_template('article_detail.html', title=title, content=article[0], ID=session['ID'])


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        s = 'INSERT INTO  users VALUES(\''+request.form['ID']+'\',\''+request.form['Password']+'\');'
        print(s)
        g.cursor.execute(s)
        g.cursor.execute('CREATE TABLE '+request.form['ID']+'(title text,content text);')
        session['ID'] = request.form['ID']
        return redirect(url_for('index', ID=request.form['ID']))

if __name__ == '__main__':
    app.run()
