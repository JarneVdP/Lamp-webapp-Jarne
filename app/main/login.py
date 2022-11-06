from app.application import create_app, login_manager, db, bcrypt, ConfigParser
from app.main.models import User
from . import main
import flask, flask_login


#flask-login user_loader functie controleert bij elk pagina verzoek de geldigheid van de sessie
@login_manager.user_loader
def load_user(user_id):
    print("flask-login: user_loader functie opgeroepen om geldigheid user sessie %s te controleren." % user_id)
    return User.query.get(int(user_id))


#flask-login custom unauthorized handler. Wordt uitgevoerd indien niet ingelogd of ongeldig...
#@main.route('/unauthorized', methods=['GET', 'POST'])
@login_manager.unauthorized_handler
def unauthorized():
    # if flask.request.method == 'POST':
    #     try:
    #         return flask.redirect(flask.url_for('main.register'))
    #     except Exception as e:
    #         print(e)
    #         return(e)
    # else:
    return flask.render_template('unauthorized.html')    



#index template geeft andere inhoud afhankelijk of gebruiker is ingelogd of niet. Bekijk template...
@main.route('/')
def index():
    return flask.render_template('index.html')


#home template geeft bepaalde inhoud van de user sessie.
#enkel toegankelijk indien gebruiker ingelogd.
@main.route('/home')
@flask_login.login_required
def home():
    return flask.render_template('home.html')

#logout route. Roept de flask-login logout_user() functie op om de gebruikersessie te stoppen.
@main.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out <a href="' + flask.url_for('main.index') + '">Index</a>'

#Login route. GET methode voor weergeven login formulier. POST methode om login formulier te verwerken.
#Controleert of username & password overeen komen met database
#Roept de flask-login login_user(user) functie op indien correct, waarbij user de overeenkomende inhoud bevat volgens User model.
@main.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        try:
            user = User.query.filter_by(username=flask.request.form['username']).first()
            #salt and hash password
            if user and bcrypt.check_password_hash(user.pwd, flask.request.form['password']):
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('main.indexlamp'))
            return "Invalid username or password..."
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('login.html')

#Register route. GET methode voor weergeven register formulier. POST methode om register formulier te verwerken.
#Maakt nieuwe user aan.
#Nieuwe user wordt daarbij ook gepusht naar database.
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
            return flask.redirect(flask.url_for('main.login'))
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('register.html')

