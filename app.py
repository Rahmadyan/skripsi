from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os
from werkzeug.utils import secure_filename

# from test import data_result
from test3 import results
from test2 import jumlah_query
import mysql.connector


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'news'
#seting ouputdata dari database ke dictionary
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# init MYSQL
mysql = MySQL(app)

# Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

#Kumpulan Artikel
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM news_tb")

    articles = cur.fetchall()

    # print()
    # print(articles)
    # for i in range(0, len(articles)):
    #     for word in articles[i]:
    #         # print(word)
    #         print([word]['content'])
            # print(str(word[0]['id']))
        # print(i)
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()

# @app.route('/article/open')
# def articless():
#     cur = mysql.connection.cursor()
#     result = cur.execute("SELECT * FROM show_data")
#     articless = cur.fetchall()
#     if result > 0:
#         return render_template('r_article.html', articless=articless)
#     else:
#         msg = 'No Articles Found'
#         return render_template('r_article', msg=msg)

    # ambil id yang sesuai dengan id pembanding di tabel
#Buka Artikel

@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get article
    result = cur.execute("SELECT * FROM news_tb WHERE id = %s", [id])
    article = cur.fetchone()
    # print(article)
    # print(article)'
    # print(id)
    b = int(id)
    # ambil metode result di clas test3
    hasil = results(b)
    cur.execute("TRUNCATE TABLE show_data")
    sql = "INSERT INTO show_data (id, title, author, time, imagelink, content) VALUES (%s, %s, %s, %s, %s, %s)"
    data = hasil
    cur.executemany(sql, data)
    mysql.connection.commit()


    # print(artikels)
    # print(articles)
    result = cur.execute("SELECT * FROM show_data limit 5 offset 1")
    articless = cur.fetchall()
    # real_id = hasil()

    # list_id_real_id = []
    # for i in enumerate(real_id):
    #     list_id_real_id.append(i)
    # print(list_id_real_id)
    # print(id)
    # parsing id artikel dan tetntukan urutan dari id tersebut berapa?
    # masukan urutan id ke dalam sql
    # terakhir panggil
    # for i in list_id_real_id:
    #     for x in range(o, len(hasil_sorting)):
    #         if
    #     print(i[0])
    # cur = mysql.connection.cursor()
    # result = cur.execute("SELECT * FROM news_tb")
    # articles = cur.fetchall()
    # print(articles)
    # result = cur.execute("SELECT * FROM result_tb WHERE id_query = %s", [id])
    # a=cur.fetchall()
    # a = str(a[0]['content'])

    return render_template('article.html', article=article, articless=articless)

#Class Registrasi USER
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

#Satpam / Mengecek apakah sudah login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
# Dashboard ADMIN
@app.route('/dashboard')
@is_logged_in #dikasih Satpam
def dashboard():
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM news_tb")

    articles = cur.fetchall()

    if result > 0:
        return render_template('admin_dash.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('admin_dash.html', msg=msg)
    # Close connection
    cur.close()

    # Create cursor
    # cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in
    # result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])
    #
    # articles = cur.fetchall()
    #
    # if result > 0:
    #     return render_template('dashboard.html', articles=articles)
    # else:
    #     msg = 'No Articles Found'
    # return render_template('dashboard.html', msg=msg)
    # Close connection
    # cur.close()

#Add Class Article
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=30)])

#pengecekan file degan menggunakan rsplit
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Add Article
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in #dikasih Satpam
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        file = request.files['file']

        if 'file' not in request.files:
            return render_template('add_article.html')

        if file.filename == '':
            return render_template('add_article.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return 'file ' + filename + ' di simpan' + ' <a href="/upload">kembali</a>'

        title = form.title.data
        content=form.content.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO news_tb(title, imagelink, content, author) VALUES(%s,%s,%s,%s)",(title, filename, content, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form = form)

# Edit Artikel
@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in #dikasih Satpam
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM news_tb WHERE id = %s", [id])
    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.content.data = article['content']

    if request.method == 'POST' and form.validate():
        file = request.files['file']

        if 'file' not in request.files:
            return render_template('add_article.html')

        if file.filename == '':
            return render_template('add_article.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return 'file ' + filename + ' di simpan' + ' <a href="/upload">kembali</a>'
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO news_tb(title, imagelink, content, author) VALUES(%s,%s,%s,%s)",(title, filename, content, session['username']))
        cur.execute("UPDATE news_tb SET title=%s, imagelink=%s, content=%s WHERE id=%s",(title, filename, content, id))
        mysql.connection.commit()
        cur.close()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form = form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM news_tb WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
@is_logged_in #dikasih Satpam
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    #membuat secret key untuk register
    app.secret_key='secret123'
    app.run(debug=True)
