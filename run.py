from webApp import app
from config import config
from flaskwebgui import FlaskUI
import os, signal

def shutdown_server():
    print('Exit app')
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    FlaskUI(app=app, server="flask", port=config['WEB_APP']['PORT'], on_shutdown=shutdown_server).run()
    #app.run(debug=True, port=config['WEB_APP']['PORT'])