from project import app
from flask import render_template, flash, redirect, url_for, request, render_template_string
from werkzeug.urls import url_parse
from project.forms import LoginForm, RegistrationForm, SearchForm, AddUserForm
from flask_login import current_user, login_user, logout_user, login_required
from project.models import Admin, User
from project import db
import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search_form = SearchForm()
    add_form = AddUserForm()
    users = User.query.all()

    if add_form.validate_on_submit():
        user = User(name=add_form.name.data, email=add_form.email.data or None, phone=add_form.phone.data or None,
                    additional_comment=add_form.comment.data, date=datetime.date.today())
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('index.html', search_form=search_form, add_form=add_form, users=users)


@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    print(user)
    return 'Информация по юзеру'


@app.route('/delete/user/<id>')
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = Admin(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
