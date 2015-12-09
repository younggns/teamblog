import os
import sys
from datetime import datetime
from math import ceil
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask.ext.wtf import Form
from forms import ContactForm
from flask.ext.mail import Message, Mail


reload(sys)
sys.setdefaultencoding("utf-8")
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = 'WebDesign'

'''Configuration - Debug can be removed for production use'''
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite'),
    SECRET_KEY='not a password',
    DEBUG=True,
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True,
    USERNAME='admin',
    PASSWORD='default',
    PER_PAGE=10,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'umsiwebdesign@gmail.com',
    MAIL_PASSWORD = '105sstate',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)

mail = Mail(app)


'''Data model - one (Post) to many (Comment)'''
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reply = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Comment %r>' % self.reply

'''index page showing all posts paginated'''
@app.route('/')
def default():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items
    return render_template('index.html', name="index", entries=entries, pagination=pagination)

'''index page showing all posts paginated'''
@app.route('/show_posts')
def show_posts():
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items
    return render_template('show_entries.html', name="posts", entries=entries, pagination=pagination)

'''url for each post and its guest comments'''
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    comments = post.comments.all()
    page=request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
    entries=pagination.items
    if request.method == 'POST':
        addcomments = Comment(name=request.form['name'],reply=request.form['reply'], timestamp=datetime.now(), post=post)
        db.session.add(addcomments)
        return redirect(url_for('default'))
    return render_template('post.html', name="posts", post=post, comments=comments, entries=entries, pagination=pagination)



'''add a post if the admin is logged in'''
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        post=Post(title=request.form['title'], text=request.form['text'], category=request.form['category'], timestamp=datetime.now())
        db.session.add(post)
        flash('New entry was successfully posted')
        return redirect(url_for('default'))
    return render_template('add.html', name="add")

'''edit a post if the admin is logged in'''
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('text'):
            post.title = request.form['title']
            post.text = request.form['text']
            post.cateogry = request.form['category']
            db.session.add(post)
            db.session.commit(post)
            flask('Entry was successfully edited')
            return redirect(url_for('default'))
    return render_template('edit.html', name="edit", post=post)

'''delete a post if admin is logged in'''
@app.route('/delete/<int:id>')
def delete_entry(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        flash('The post has been deleted')
        return redirect(url_for('default'))

'''login page with error message'''
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
            flash('You were logged in')
            return redirect(url_for('default'))
    return render_template('login.html', error=error, name="login")

'''log admin out; return None if key 'logged_in' doesn't exsit'''
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('default'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  form2 = ContactForm()

  if request.method == 'POST':
  	msg = Message("Hello From Flask", sender=request.form.get('email'), recipients=["younggns@umich.edu"])
  	msg2 = Message("The mail has been successfully sent", sender="younggns@umich.edu", recipients=[request.form.get('email')])
  	mail.send(msg)
  	mail.send(msg2)
  	flash('Information sent!')
  	return redirect(url_for('contact'))

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def pageNotFound(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
