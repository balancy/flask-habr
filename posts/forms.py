from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, PasswordField, SubmitField)
from wtforms.validators import EqualTo, DataRequired, Length


class LoginForm(FlaskForm):
    """Form used for login.
    """

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
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={"class": "form-check-input"},
    )


class RegisterForm(FlaskForm):
    """Form used for register.
    """

    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(message="Поле должно быть заполнено"),
            Length(
                min=4, max=25,
                message='Имя пользователя должно '
                        'быть длиной от 4 до 25 символов'
            ),
        ],
        render_kw={"class": "form-control mt-3"},
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message="Поле должно быть заполнено"),
            EqualTo('confirm', message='Пароли должны совпадать'),
            Length(
                min=6,
                message='Пароль должен быть длиной от 6 символов'
            ),
        ],
        render_kw={"class": "form-control mt-3"},
    )
    confirm = PasswordField(
        'Повторите пароль',
        render_kw={"class": "form-control mt-3"},
    )
    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-outline-dark mt-3"},
    )
