from flask import Flask, request, render_template, flash, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import redirect

from posts import config
from posts.forms import LoginForm
from posts.models import Tag, User
from posts.models.database import db
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


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('habr_app.posts'))

    title = "Авторизация"
    all_tags = db.session.query(Tag).all()
    login_form = LoginForm()

    if request.method == 'GET':
        return render_template(
            'login.html',
            title=title,
            tags=all_tags,
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
    if current_user.is_authenticated:
        logout_user()
        flash('Вы вышли из своей учетной записи')
    return redirect(url_for('habr_app.posts'))
