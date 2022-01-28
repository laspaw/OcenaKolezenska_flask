from flask import Flask
from api import login, register, classes
from flask_login import LoginManager
from repositories import users_repo

app = Flask(__name__)
#klucz szyfrujący identyfikatory sesji
app.config['SECRET_KEY']='L=q74UE:/-F_2a?;H9m)tY@*dWNY~]p<'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users_repo.UserRepository().get_by_id(user_id)


app.add_url_rule('/login', view_func=login.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=login.logout, methods=['GET'])
app.add_url_rule('/restore_password', view_func=login.restore_password, methods=['GET'])
app.add_url_rule('/register', view_func=register.register, methods=['GET', 'POST'])

app.add_url_rule('/classes', view_func=classes.classes, methods=['GET'])
