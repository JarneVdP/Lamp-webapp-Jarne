#!/bin/env python
from app.application import create_app, SOCKETIO
import flask
APP = create_app()

@APP.errorhandler(404)
def not_found_error(error):
    return flask.render_template('404.html'),404

if __name__ == '__main__':
    SOCKETIO.run(APP, host='localhost', port=8080, use_reloader=False)
