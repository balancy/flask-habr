from getpass import getpass
import sys

from posts.app import app
from posts.models import User
from posts.models.database import db

with app.app_context():
    username = input('Введите имя пользователя: ')

    if db.session.query(User).filter_by(username=username).count():
        sys.exit('Такой пользователь уже есть')

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit('Пароли должны совпадать')

    new_user = User(username=username, is_admin=True)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f'{ new_user } added')
