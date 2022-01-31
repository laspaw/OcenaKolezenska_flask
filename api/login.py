import flask
from flask import render_template, request, redirect
from forms import LoginForm
from repositories import users_repo
import bench
from flask_login import login_user, logout_user

def login_prefilled_email(prefilled_email):
    return login(prefilled_email)

def login(prefilled_email=None):
    form = LoginForm(request.form)
    if prefilled_email is not None:
        form.email.data = prefilled_email
    error = None

    if request.method == "POST":
        if form.validate():
            # collect data from form
            user_email = form.email.data
            user_password = form.password.data

            # try to authorize
            unauthorized_user = users_repo.UserRepository()
            if not unauthorized_user.email_exists(user_email):
                error = '''Nie mamy takiego adresu e-mail w bazie użytkowników.<br><br>
                        Upewnij się, czy nie pomyliła(e)ś się przy wpisywaniu adresu e-mail.<br>
                        Jeżeli jeszcze nie posiadasz konta, <a href="/register">zarejestruj się</a>.<br>
                        Jeżeli masz już konto, być może podczas rejestracji użyła(e)ś innego adresu e-mail.<br>
                        Jeżeli nie pamiętasz hasła, użyj opcji <a href="/restore_password">odzyskiwania hasła</a>.'''
            else:
                salt = unauthorized_user.get_salt(user_email)
                password_hash = bench.PasswordHash(user_password, salt).get_hex()
                user = unauthorized_user.check_credentials(user_email, password_hash)
                if user is None:
                    error = 'Podane hasło jest nieprawidłowe'
                else:  # user is authorized
                    flask.flash('Pomyślnie zalogowano użytkownia.')
                    login_user(unauthorized_user.get_by_id(user['id']))
                    return redirect('/classes')

    # if request.method ! = "POST":
    return render_template('endpoints/login.html.jinja2', form=form, error=error)


def logout():
    logout_user()
    return redirect('/login')


def restore_password():
    return render_template('endpoints/restore_password.html.jinja2')
