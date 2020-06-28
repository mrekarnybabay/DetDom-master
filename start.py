from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login_manager = LoginManager()
is_started = True

login_manager.init_app(app)


# -----------------РЕГИСТРЕЙШН-------------------------------


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    fio = StringField('ФИО', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


# -----------------МАРШРУТИЗЕЙШН-------------------------------


@app.route('/')
def home():
    if current_user.is_anonymous == False:
        user = {'name': current_user.fio}
        car = {'name': Car.name}
        return render_template('home.html', car=car, is_started=is_started, user=user)
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, fio=form.fio.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/parametrs')
def parametrs():
    parms = [{'name': 'Температура охлаждающей жидкости (°С)', 'value': '25'},
             {'name': 'Напряжение борт. сети (V)', 'value': '14.1'},
             {'name': 'Частота враащения кол. вала (об/мин)', 'value': '910'},
             {'name': 'Текущая скорость', 'value': '0'},
             {'name': 'Мгновенный расход (л/ч)', 'value': '0.8'},
             {'name': 'Мгновенный расход (л/км)', 'value': '0'},
             {'name': 'Средний расход (л/км)', 'value': '9.2'}]
    car = {'name': 'ВАЗ-2110'}
    user = {'name': 'Бычков Алексей Андреевич'}
    return render_template('parametrs.html', car=car, parms=parms, user=user)


@app.route('/errors')
def errors():
    errors = [{'code': 'P1901', 'name': 'Ошибка электроцепи питания', 'date': '24.06.20202'},
              {'code': 'P1902', 'name': 'Не заводится', 'date': '25.06.20202'}]
    car = {'name': 'ВАЗ-2110'}
    user = {'name': 'Бычков Алексей Андреевич'}
    return render_template('errors.html', car=car, errors=errors, user=user)


@app.route('/car/<id>', methods=['GET', 'POST'])
def car(id):
    if request.method == 'GET':
        pass
    else:
        # Найти нужную машину по ID car = Car.query.filter_by(id=id).first()
        #                              таблица в бд         в бд    переменная
        data = request.data  # помещаем данные из запроса
        data = request.get_json()
        var = data['модель']  # обращение к json


@app.route('/stop_engine', methods=['GET', 'POST'])
def stop_engine():
    if request.method == 'GET':
        data = request.values
        global is_started
        is_started = True
        return redirect('/')
    else:
        return 'Я ОБОСРАЛСЯ'


@app.route('/start_engine', methods=['GET', 'POST'])
def start_engine():
    if request.method == 'GET':
        data = request.values
        global is_started
        is_started = False
        return redirect('/')
    else:
        return 'Я ОБОСРАЛСЯ'

@app.route('/change_parm')
def change_parm():
    parms = [{'name': 'Температура охлаждающей жидкости (°С)', 'value': '25'},
             {'name': 'Напряжение борт. сети (V)', 'value': '14.1'},
             {'name': 'Частота враащения кол. вала (об/мин)', 'value': '910'},
             {'name': 'Текущая скорость', 'value': '0'},
             {'name': 'Мгновенный расход (л/ч)', 'value': '0.8'},
             {'name': 'Мгновенный расход (л/км)', 'value': '0'},
             {'name': 'Средний расход (л/км)', 'value': '9.2'}]
    return render_template('parametrs.html', car=car, parms=parms, user=user)
# -----------------БЭДЭЙШН-------------------------------


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fio = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(11), index=True, unique=True)
    #car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    cars = db.relationship('Car', backref='владелец')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Car {}>'.format(self.name)


# class Ebu(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
#     info_car_model = db.Column(db.String(120), index=True, unique=True)
#     info_car_make = db.Column(db.String(120), index=True, unique=True)
#     info_engine = db.Column(db.String(120), index=True, unique=True)
#     info_year = db.Column(db.Integer, index=True)
#     ebus = db.relationship('ebu')
#
#
# class Error(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
#     ebu_id = db.Column(db.Integer, db.ForeignKey('ebu.id'))
#     code_error = db.Column(db.String(120), index=True, unique=True)
#     name_error = db.Column(db.String(120), index=True, unique=True)
#     about_error = db.Column(db.String(120), index=True, unique=True)
#     error_time = db.Column(db.DateTime)
#
#
# class Engine_parameter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
#     ebu_id = db.Column(db.Integer, db.ForeignKey('ebu.id'))
#     parm_value = db.Column(db.Float, index=True)
#     name_parm = db.Column(db.String(120), index=True, unique=True)
#     parm_about = db.Column(db.String(120), index=True, unique=True)
#     error_time = db.Column(db.DateTime)
#
#
# class Sensor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
#     name_sensor = db.Column(db.String(120), index=True, unique=True)
#     sensor_value = db.Column(db.Integer, index=True)
#     sensor_time = db.Column(db.DateTime)
#
#
# class Control_rele(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
#     name_control = db.Column(db.String(120), index=True, unique=True)
#     control_pin = db.Column(db.Integer, index=True)


# добавляем экземпляр и модели базы данных в сеанс оболочки
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car}

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)