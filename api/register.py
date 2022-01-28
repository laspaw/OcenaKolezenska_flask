from flask import render_template, request
from forms import RegisterForm
from repositories import users_repo
import bench
import crypt


def register():
    form = RegisterForm(request.form)
    email_exists = None

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            salt = crypt.mksalt(crypt.METHOD_SHA512)
            password_hash = bench.PasswordHash(form.password.data, salt).get_hex()

            if users_repo.UserRepository().email_exists(email):
                email_exists = 'True'
            else:
                user_id = users_repo.UserRepository().register_user(email, password_hash, salt)

                return f'user successfully created with id={user_id}'

    return render_template('register.html.jinja2', form=form, email_exists=email_exists)
