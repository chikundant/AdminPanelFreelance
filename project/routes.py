from project import app
from flask import render_template, flash, redirect, url_for, request, render_template_string
from werkzeug.urls import url_parse
from project.forms import LoginForm, RegistrationForm, SearchForm, AddUserForm, AddGameForm
from flask_login import current_user, login_user, logout_user, login_required
from project.models import Admin, User, Game, Type, Cell
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
                    additional_comment=add_form.comment.data, date=datetime.date.today(),
                    birthday=add_form.birthday.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('index.html', search_form=search_form, add_form=add_form, users=users)


@app.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    add_game_form = AddGameForm()

    if add_game_form.is_submitted():
        game = Game(cell_id=add_game_form.cell_id.data, personal_comment=add_game_form.my_comment.data, user_comment=add_game_form.user_comment.data)
        game.user_id = user.id
        db.session.add(game)
        db.session.commit()



    # type1 = Type(name='Name 3', description='Description 3')
    # type2 = Type(name='Name 4', description='Description 4')
    # type3 = Type(name='Name 5', description='Description 5')
    # type4 = Type(name='Name 6', description='Description 6')
    #
    # cell1 = Cell(title='Title 3', description='Description 3')
    # cell2 = Cell(title='Title 3', description='Description 3')
    # cell3 = Cell(title='Title 3', description='Description 3')
    # cell4 = Cell(title='Title 3', description='Description 3')
    #
    # cell1.type = type1
    # cell2.type = type2
    # cell3.type = type3
    # cell4.type = type4
    #
    # db.session.add(type1)
    # db.session.add(type2)
    # db.session.add(type3)
    # db.session.add(type4)
    #
    # db.session.add(cell1)
    # db.session.add(cell2)
    # db.session.add(cell3)
    # db.session.add(cell4)

    # db.session.commit()
    games = Game.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, add_game_form=add_game_form, games=games)


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
