from ..application import create_app, db

#as stated in the README, run the file to create a database with the necessary tables
def init_db():
	"""Initialize database(s)."""
	app = create_app()
	app.app_context().push()
	db.create_all()


#run once to initialize database
init_db()