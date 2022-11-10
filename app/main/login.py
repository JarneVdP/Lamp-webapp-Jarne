from app.application import create_app, login_manager, db, bcrypt
from app.main.models import User
from . import main
import flask, flask_login
import time

#Check if the user is logged in. Remember the user if the user is logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#flask-login custom unauthorized handler. If the user is not logged in, redirect to the unauthorized page where the log in and sign up forms are ready
@login_manager.unauthorized_handler
def unauthorized():
    return flask.render_template('unauthorized.html')    


#index Shows the homepage. The text is dependant on whether the user is logged in or not
@main.route('/')
def index():
    return flask.render_template('index.html')


#home template shows the user information. It's just to show the salt and hash. Tbh, it's not smart to show the salt and hash to the user. It's just for testing purposes
@main.route('/home')
@flask_login.login_required
def home():
    return flask.render_template('home.html')


#logout route. using flask-login to log out the user. Redirect to the index page. because of wekzeug, we need to use main.index instead of just index. Main is the blueprint name
@main.route("/logout")
@flask_login.login_required
def logout():
    with open('user.log', 'a') as f:
        f.write("User " + flask_login.current_user.username + " logged out at " + str(time.strftime("%d-%m-%Y %H:%M"))+ "\n")
    flask_login.logout_user()
    return flask.redirect(flask.url_for('main.index')) 

#Login route. GET methode voor weergeven login formulier. POST methode om login formulier te verwerken.
#Controleert of username & password overeen komen met database
#Roept de flask-login login_user(user) functie op indien correct, waarbij user de overeenkomende inhoud bevat volgens User model.

#login route. GET method to show the login form. POST method to process the login form. Check if the user is in the database. 
#Else, redirect to the login page.
@main.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        try:
            user = User.query.filter_by(username=flask.request.form['username']).first()
            #salt and hash password
            if user and bcrypt.check_password_hash(user.pwd, flask.request.form['password']):
                flask_login.login_user(user)
                with open('user.log', 'a') as f:
                    f.write("User " + flask_login.current_user.username + " logged in at " + str(time.strftime("%d-%m-%Y %H:%M")) + "\n")
                return flask.redirect(flask.url_for('main.index'))
            #Show popup message if the username or password is incorrect
            flask.flash('Username or password is incorrect')
            return flask.redirect(flask.url_for('main.login'))
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('login.html')


#Register route. GET method to show the register form. POST method to process the register form. When the user is created,push the new user to the database.
@main.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        try:
            newUser = User(
                username = flask.request.form['username'], 
                pwd = bcrypt.generate_password_hash(flask.request.form['password'])
            )
            db.session.add(newUser)
            db.session.commit()
            with open('user.log', 'a') as f:
                f.write("User " + flask.request.form['username'] + " registered a new account at " + str(time.strftime("%d-%m-%Y %H:%M"))+ "\n")
            return flask.redirect(flask.url_for('main.login'))
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('register.html')

