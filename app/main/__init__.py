from flask import Blueprint

#create blueprint and initiate as main
main = Blueprint('main', __name__)

from . import functional, login