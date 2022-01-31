from flask import Flask
from api import login, register, classes, welcome
from flask_login import LoginManager
from repositories import users_repo
import crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = crypt.mksalt(crypt.METHOD_SHA512)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return users_repo.UserRepository().get_by_id(user_id)


# endpoint definitions
app.add_url_rule('/', view_func=welcome.welcome, methods=['GET'])

app.add_url_rule('/login', view_func=login.login, methods=['GET', 'POST'])
app.add_url_rule('/login/<prefilled_email>', view_func=login.login_prefilled_email, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=login.logout, methods=['GET'])
app.add_url_rule('/restore_password', view_func=login.restore_password, methods=['GET'])

app.add_url_rule('/register', view_func=register.register, methods=['GET', 'POST'])
app.add_url_rule('/register_successful/<prefilled_email>', view_func=register.register_successful, methods=['GET'])

app.add_url_rule('/classes', view_func=classes.classes, methods=['GET'])
