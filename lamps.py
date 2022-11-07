#!/bin/env python
from app.application import create_app, SOCKETIO
import flask
APP = create_app()

#add errorhandler here. It doesn't work when applied to werkzeug @main
@APP.errorhandler(404)
def not_found_error(error):
    return flask.render_template('404.html'),404

#run the app via socketio on port 8080
if __name__ == '__main__':
    SOCKETIO.run(APP, host='localhost', port=8080, use_reloader=False)
