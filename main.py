from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask, url_for, request, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired(),
                                                                   EqualTo("password",
                                                                           message="Passwords must match!")])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['POST', 'GET'])
def index():
    global session
    form = LoginForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('success.html', message="Такой пользователь уже существует")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return render_template('success.html', message="Вы успешно заполнили форму")
    return render_template('login.html', title='Авторизация', form=form)


def main():
    global session
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()