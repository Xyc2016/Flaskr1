from flask import Flask, g, url_for, request, render_template, make_response, abort, \
    session, redirect, jsonify, escape
import sqlite3

from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SECRET_KEY'

# @app.before_request
# def before_request():
#     g.database = sqlite3.connect('User_Password.db')
#     g.cursor = g.database.cursor()
#
#
# @app.after_request
# def after_request():
#     g.cursor.close()
#     g.database.commit()
#     g.database.close()
#
    

@app.route('/')
def index():
    ID = None
    articles = None
    if 'ID' in session:
        ID = session['ID']
        connect = sqlite3.connect('Users_Passwords.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM ' + session['ID'])
        articles = cursor.fetchall()
        cursor.close()
        connect.close()
        print(articles)
    return render_template('index.html', ID=ID, articles=articles)


@app.route('/write_blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'GET':
        return render_template('write_blog.html', ID=session['ID'])
    else:
        theConnect = sqlite3.connect('Users_Passwords.db')
        theCursor = theConnect.cursor()
        s = 'INSERT INTO ' + session['ID'] + ' values(\'' + \
            request.form['title'] + '\',\'' + \
            request.form['content'] + '\');'
        theCursor.execute(s)
        theCursor.close()
        theConnect.commit()
        return redirect(url_for('index',ID = session['ID']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('Users_Passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    Users = cursor.fetchall()
    if request.method == 'POST' and (request.form['ID'], request.form['Password']) in Users:
        session['ID'] = request.form['ID']
        print('logged in')
        return redirect(url_for('index'))
    else:
        print('--')
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('ID')
    return redirect(url_for('index'))


@app.route('/delete_article')
def delete_article():
    title = request.args.get('title')
    ID = session['ID']
    connect = sqlite3.connect('Users_Passwords.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM '+ID+'  WHERE title = \''+title+'\';')
    cursor.close()
    connect.commit()
    connect.close()
    return redirect(url_for('index',ID = session['ID']))



@app.route('/article_detail')
def article_detail():
    title = request.args.get('title')
    connect = sqlite3.connect('Users_Passwords.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM ' + session['ID'] + ' WHERE title=' + title)
    article = cursor.fetchall()[0]
    return render_template('article_detail.html', title=title, content=article[0], ID=session['ID'])


if __name__ == '__main__':
    app.run()
