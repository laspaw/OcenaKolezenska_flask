import db
# UserMixin : klasa zawierająca wszystkie metody potrzebne faskowi do działania w kontekście zaloowanego użytkownika
from flask_login import UserMixin


class LoggedUser(UserMixin):
    pass


class UserRepository(db.PGRepository):
    def email_exists(self, email):
        self.cursor.execute('SELECT id FROM users WHERE email=%s', (email,))
        if self.cursor.fetchone() is not None:
            return True
        return False

    def register_user(self, email, password_hash, salt):
        self.cursor.execute('INSERT INTO users(email, password_hash, password_salt) VALUES (%s, %s, %s) RETURNING id;',
                            (email, password_hash, salt))
        added_record = self.cursor.fetchone()
        self.connection.commit()
        return added_record['id']

    def get_salt(self, email):
        self.cursor.execute('SELECT password_salt FROM users WHERE email=%s ', (email,))
        return self.cursor.fetchone()['password_salt']

    def check_credentials(self, email, password_hash):
        self.cursor.execute('SELECT id FROM users WHERE email=%s AND password_hash=%s', (email, password_hash))
        return self.cursor.fetchone()

    def map_db_user_to_obj_user(self, row):
        user = LoggedUser()
        user.id = row['id']
        user.email = row['email']
        return user

    def get_by_id(self, id):
        self.cursor.execute('SELECT * FROM users WHERE id=%s', (id,))
        return self.map_db_user_to_obj_user(self.cursor.fetchone())







    # trash code
    def get_all(self):
        self.cursor.execute('SELECT class_id, class_name, class_short FROM classes')
        return self.cursor.fetchall()

    def add_class(self, data):
        self.cursor.execute(
            'INSERT INTO classes(class_name, class_short) VALUES (%s, %s) RETURNING class_id',
            (data['class_name'], data['class_short']))
        added_class = self.cursor.fetchone()
        self.connection.commit()
        return added_class['class_id']

    def class_exists(self, class_id):
        self.cursor.execute('SELECT class_id FROM classes WHERE class_id=%s', (class_id,))
        if self.cursor.fetchone() is not None:
            return True
        return False

    def delete_class(self, class_id):
        self.cursor.execute('DELETE FROM classes WHERE class_id=%s', (class_id,))
        self.connection.commit()
