from app import app
from flask import Flask, render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def default():
    return render_template('index.html', name='index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                            title='Sign In',
                            form=form)
