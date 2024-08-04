from flask import Flask
import os
from config import config


app = Flask(__name__, instance_relative_config=True, template_folder=os.path.join(os.getcwd(), config['WEB_APP']['template_folder']))


__version__ = '0.0.1.0'

app.config['SECRET_KEY'] = '2qwtq2'
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

from webApp.evals.area import Vision

vision = Vision()

from webApp.helpers import jinjaHelper

from webApp.interfaces import *