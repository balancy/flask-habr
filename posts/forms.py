from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={"class": "form-control mt-3"},
    )
    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={"class": "form-control mt-3"},
    )
    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-outline-dark mt-3"},
    )
