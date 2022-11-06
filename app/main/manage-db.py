from ..application import create_app, db
from ..main.models import User


def init_db():
	"""Initialize database(s)."""
	app = create_app()
	app.app_context().push()
	db.create_all()


#run once to initialize database
init_db()