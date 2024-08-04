from flask import make_response, send_from_directory
import os
from config import config
from webApp import app


@app.route('/css/<path:path>')
def send_css(path):
    resp = make_response(send_from_directory(os.path.join(os.path.join(os.getcwd(), config['WEB_APP']['template_folder']), 'static/css'), path), 200)
    resp.headers['Cache-Control'] = 'public, max-age=31536000'
    return resp

@app.route('/js/<path:path>')
def send_js(path):
    resp = make_response(send_from_directory(os.path.join(os.path.join(os.getcwd(), config['WEB_APP']['template_folder']), 'static/js'), path), 200)
    resp.headers['Cache-Control'] = 'public, max-age=31536000'
    return resp

@app.route('/pics/<path:path>')
def send_pic(path):
    return send_from_directory(os.path.join(os.path.join(os.getcwd(), config['WEB_APP']['template_folder']), 'static/pics'), path)