from system.core.controller import *

class Loginregs(Controller):
    def __init__(self, action):
        super(Loginregs, self).__init__(action)
  
        self.load_model('Loginreg')
        self.db = self._app.db

    def index(self):
         return self.load_view('index.html')
    
    def success(self):
         return self.load_view('success.html')

    def register(self):
        reginfo = {
                    'fname': request.form['fname'],
                    'lname': request.form['lname'],
                    'email': request.form['email'],
                    'password': request.form['password'],
                    'confirmpass': request.form['confirmpass'],
        }
        datainfo = self.models['Loginreg'].register(reginfo)
        print datainfo
        if datainfo == 'registered':
            session['registered'] = 'Thank you for Registering. Please Log in'
            print session
        else:
            errors = datainfo
            flash(errors)
        return redirect('/')

    def login(self):
        loginfo = {
                    'email': request.form['email'],
                    'password': request.form['password'],                   
        }
        loggedin = self.models['Loginreg'].login(loginfo)
        if 'logged_info' in loggedin:
            session['logged_info'] = loggedin['logged_info']
            return redirect('/success')
        else:
            errors = loggedin
            flash(errors)
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')