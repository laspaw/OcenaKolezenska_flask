from wtforms import Form, StringField, PasswordField, validators

# validator presets
email_validator = [validators.InputRequired(message='E-mail nie może być pusty.'), validators.Email(message='Podaj prawidłowy adres e-mail.')]
password_validator = [validators.InputRequired(message='Hasło nie może być puste.'), validators.length(min=4, message='Podaj hasło spełniające wymagania.')]
confirm_password_validator = password_validator + [validators.EqualTo('password', message='Podane hasła różnią się od siebie.\nPodaj dwa identyczne hasła.')]


class RegisterForm(Form):
    email = StringField('Podaj e-mail: ', email_validator)
    password = PasswordField('Podaj hasło: ', password_validator)
    confirm_password = PasswordField('Powtórz hasło: ', confirm_password_validator)


class LoginForm(Form):
    email = StringField('Podaj e-mail: ', email_validator)
    password = PasswordField('Podaj hasło: ', password_validator)
