from flask import render_template, request, redirect
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
                users_repo.UserRepository().register_user(email, password_hash, salt)

                return redirect(f'/register_successful/{email}')

    return render_template('endpoints/register.html.jinja2', form=form, email_exists=email_exists)


def register_successful(prefilled_email):
    return render_template('endpoints/register_successful.html.jinja2', prefilled_email=prefilled_email)
