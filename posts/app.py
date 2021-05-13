from flask import Flask, request, render_template, flash, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import redirect

from posts import config
from posts.forms import LoginForm, RegisterForm
from posts.models import User
from posts.models.database import db
from posts.utils import get_popular_tags
from posts.views.habr import habr_app

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(habr_app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    """View for register a new user.
    """

    if current_user.is_authenticated:
        return redirect(url_for('habr_app.posts'))

    title = 'Регистрация'
    popular_tags = get_popular_tags()
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        user = User.query.filter_by(username=register_form.username.data).first()
        if user:
            flash('Такой пользователь уже есть')
            return redirect(url_for('register'))

        user = User(username=register_form.username.data)
        user.set_password(register_form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Вы успешно зарегистрировались')
        return redirect(url_for('login'))

    if request.method == 'POST':
        flash('Проверьте требования полей в форме.')

    return render_template(
        'register.html',
        title=title,
        tags=popular_tags,
        form=register_form,
        current_user=current_user,
    )


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    """View for login.
    """

    if current_user.is_authenticated:
        return redirect(url_for('habr_app.posts'))

    title = 'Авторизация'
    popular_tags = get_popular_tags()
    login_form = LoginForm()

    if request.method == 'GET':
        return render_template(
            'login.html',
            title=title,
            tags=popular_tags,
            form=login_form,
            current_user=current_user,
        )

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            flash('Вы успешно вошли в свою учетную запись')
            return redirect(url_for('habr_app.posts'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))


@app.route('/logout', endpoint='logout')
def logout():
    """View for logout.
    """

    if current_user.is_authenticated:
        logout_user()
        flash('Вы вышли из своей учетной записи')
    return redirect(url_for('habr_app.posts'))
