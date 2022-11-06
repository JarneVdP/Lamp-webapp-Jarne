#!/bin/env python
from app.application import create_app, SOCKETIO

APP = create_app()

if __name__ == '__main__':
    SOCKETIO.run(APP, host='localhost', port=8080, debug=True, use_reloader=False)
