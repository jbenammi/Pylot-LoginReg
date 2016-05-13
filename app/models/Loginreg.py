from system.core.model import Model
import re
EMAILREGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
class Loginreg(Model):
    def __init__(self):
        super(Loginreg, self).__init__()

    def register(self, reginfo):

        errors = {}
        if len(reginfo['fname']) < 2:
            errors.update({'fname': 'The first name field must be at least two characters'})
        elif not str.isalpha(str(reginfo['fname'])):
            errors.update({'fname': 'First name cannot have number or symbols'})
        if len(reginfo['lname']) < 2:
            errors.update({'lname': 'The last name field must be at least two characters'})
        elif not str.isalpha(str(reginfo['lname'])):
            errors.update({'lname': 'Last name cannot have numbers or symbols'})
        if not EMAILREGEX.match(reginfo['email']):
            errors.update({'email': 'The E-Mail must be a valid e-mail address'})
        if len(reginfo['password']) < 8:
            errors.update({'password': 'Password must be at least 8 characters'})
        elif not any(char.isdigit() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one number'})
        elif not any(char.isupper() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one uppercase letter'})
        if reginfo['confirmpass'] != reginfo['password']:
            errors.update({'confirmpass': 'The password confirmation does not match the password'})
        if len(errors) > 0:
            return errors
        else:
            query1 = "SELECT email FROM users WHERE email = :email"
            data1 = {"email": reginfo['email']}
            if not self.db.query_db(query1, data1):
                pw_hash = self.bcrypt.generate_password_hash(reginfo['password'])
                query = "INSERT INTO users(first_name, last_name, email, password, created_on, updated_on) VALUES(:first_name, :last_name, :email, :password, now(), now())"
                info = {
                "first_name": reginfo['fname'],
                "last_name": reginfo['lname'],
                "email": reginfo['email'],
                "password": pw_hash
                }
                self.db.query_db(query, info)
                return "registered"
            else:
                errors.update({'user_registered': 'This E-Mail is already registered'})
                return errors

    def login(self, loginfo):
        errors = {}
        if not EMAILREGEX.match(loginfo['email']):
            errors.update({'email2': 'The E-Mail must be a valid e-mail address'})
        if len(loginfo['password']) < 8:
            errors.update({'password2': 'Password must be at least 8 characters'})
        if len(errors) > 0:
            return errors
        else:
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email': loginfo['email']}
            user = self.db.query_db(query, data)
            if user == []:
                errors.update({'notreg': 'E-Mail is not registered.'})
                return errors
            else:
                if self.bcrypt.check_password_hash(user[0]['password'], loginfo['password']):
                    logged_info = {'logged_info':{'id': user[0]['id'], 'first_name': user[0]['first_name'], 'last_name': user[0]['last_name']}}
                    return logged_info
                else:
                    errors.update({'passmatch': 'Incorrect password entered for registered E-Mail.'})
                    return errors