import config
from project import app
from flask import render_template, flash, redirect, url_for, request, render_template_string, send_file
from werkzeug.urls import url_parse
from project.forms import LoginForm, RegistrationForm, SearchForm, AddUserForm, AddGameForm, ChangeGameForm, CellForm, \
    TypeForm, TemplateForm, ReportForm
from flask_login import current_user, login_user, logout_user, login_required
from project.models import Admin, User, Game, Type, Cell, Template
from project import db
import datetime

import weasyprint


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
                    birthday=add_form.birthday.data or None)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))

    if search_form.is_submitted():
        search = '%{}%'
        if search_form.input.data == '':
            users = User.query.all()

        if search_form.type.data == '1':
            users = User.query.filter(User.name.like(search.format(search_form.input.data))).all()

        elif search_form.type.data == '2':
            users = User.query.filter(User.email.like(search.format(search_form.input.data))).all()

        elif search_form.type.data == '3':
            users = User.query.filter(User.phone.like(search.format(search_form.input.data))).all()


    return render_template('index.html', search_form=search_form, add_form=add_form, users=users)


@app.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = User.query.filter_by(id=id).first()

    add_user_form = AddUserForm()
    if add_user_form.is_submitted() and not (add_user_form.name.data is None):
        user.name = add_user_form.name.data
        user.email = add_user_form.email.data
        user.phone = add_user_form.phone.data
        user.birthday = add_user_form.birthday.data
        user.additional_comment = add_user_form.comment.data
        db.session.commit()
        return redirect(url_for('user', id=id))

    add_game_form = AddGameForm()
    if add_game_form.is_submitted():
        game = Game(cell_id=add_game_form.cell_id.data, personal_comment=add_game_form.my_comment.data,
                    user_comment=add_game_form.user_comment.data)
        game.user_id = user.id
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('user', id=id))

    games = Game.query.filter_by(user_id=user.id).all()

    return render_template('user.html', user=user, add_game_form=add_game_form, add_user_form=add_user_form,
                           games=games)


@app.route('/change_cell', methods=['GET', 'POST'])
@login_required
def change_cell():
    cell_form = CellForm()
    cell_form.type.choices = [(type.id, type.name) for type in Type.query.all()]
    cell_form.type.choices.append((0, None))

    if cell_form.is_submitted() and request.form['submit'] == 'search':
        cell = Cell.query.filter_by(id=cell_form.id.data).first()
        if cell:
            cell_form.type.default = cell.type_id
            cell_form.process()
            cell_form.description.data = cell.description
            cell_form.id.data = cell.id
            cell_form.title.data = cell.title

    elif cell_form.is_submitted() and request.form['submit'] == 'save':
        cell = Cell.query.filter_by(id=cell_form.id.data).first()
        if cell is None:
            cell = Cell()
        cell.id = cell_form.id.data
        cell.title = cell_form.title.data
        cell.description = cell_form.description.data
        cell.type_id = cell_form.type.data
        db.session.add(cell)
        db.session.commit()
        return redirect('change_cell')
    return render_template('change_cell.html', cell_form=cell_form)


@app.route('/change_type', methods=['GET', 'POST'])
@login_required
def change_type():
    type_form = TypeForm()

    types = Type.query.all()
    print(type_form.name_select.choices)
    for i in range(len(types)):
        type_form.name_select.choices.append((types[i].id, types[i].name))

    if type_form.is_submitted() and request.form['submit'] == 'search':
        type = Type.query.filter_by(id=type_form.name_select.data).first()
        if type:
            type_form.name.data = type.name
            type_form.description.data = type.description
        else:
            return redirect('change_type')

    elif type_form.is_submitted() and request.form['submit'] == 'save':
        print(type_form.name.data)
        type = Type.query.filter_by(id=type_form.name_select.data).first()
        if type is None:
            type = Type()
        type.name = type_form.name.data
        type.description = type_form.description.data
        db.session.add(type)
        db.session.commit()
        return redirect('change_type')

    return render_template('change_type.html', type_form=type_form)


@app.route('/change_template', methods=['GET', 'POST'])
@login_required
def change_template():
    template_form = TemplateForm()

    templates = Template.query.all()
    print(template_form.name_select.choices)
    for i in range(len(templates)):
        template_form.name_select.choices.append((templates[i].id, templates[i].name))

    if template_form.is_submitted() and request.form['submit'] == 'search':
        template = Template.query.filter_by(id=template_form.name_select.data).first()
        if template:
            template_form.name.data = template.name
            template_form.description.data = template.description
        else:
            return redirect('change_template')

    elif template_form.is_submitted() and request.form['submit'] == 'save':
        print(template_form.name.data)
        template = Template.query.filter_by(id=template_form.name_select.data).first()
        if template is None:
            template = Template()
        template.name = template_form.name.data
        template.description = template_form.description.data
        db.session.add(template)
        db.session.commit()
        return redirect('change_template')

    return render_template('change_template.html', type_form=template_form)


@app.route('/game/<id>', methods=['GET', 'POST'])
def edit_game(id):
    change_game_form = ChangeGameForm()
    game = Game.query.filter_by(id=id).first()

    if change_game_form.is_submitted():
        game.cell_id = change_game_form.cell_id.data
        game.user_comment = change_game_form.user_comment.data
        game.personal_comment = change_game_form.my_comment.data
        db.session.commit()
        return redirect(url_for('user', id=game.user_id))

    return render_template('edit_game.html', game=game, change_game_form=change_game_form)


@app.route('/delete_game/<id>', methods=['GET', 'POST'])
def delete_game(id):
    game = Game.query.filter_by(id=id).first()
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('user', id=game.user_id))


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


@app.route('/user/<id>/report', methods=['GET', 'POST'])
@login_required
def report(id):
    user = User.query.filter_by(id=id).first()
    games = Game.query.filter_by(user_id=id).all()

    newline = '</br>'
    bold = lambda str: f'<strong>{str}</strong>'
    i = lambda str: f'<i>{str}</i>'
    h1 = lambda str: f'<h1>{str}</h1>'

    form = ReportForm()

    if request.method == 'POST':
        pdf = weasyprint.HTML(string=form.text.data).write_pdf()
        open('project/report.pdf', 'wb').write(pdf)
        return send_file('report.pdf', as_attachment=True)

    # Creating a template
    form.text.data = h1(user.name) + h1(user.date)
    form.text.data += 'Запрос: ' + newline + i('Здесь вписывается ваш запрос') + newline + newline

    for game in games:
        form.text.data += game.cell.title
        form.text.data += game.cell.description
        if game.cell.type:
            form.text.data += bold('Тип клетки: ') + game.cell.type.name + newline
            form.text.data += i(game.cell.type.description) + newline + newline

        form.text.data += bold('Ваш комментарий: ') + newline + game.user_comment + newline + newline
        form.text.data += bold('Мой комментарий: ') + newline + game.personal_comment + newline + newline












    return render_template('report.html', user=user, form=form)

