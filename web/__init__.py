from flask import Blueprint, Flask, Response
import requests
from bs4 import BeautifulSoup
from .routes import *

def create_app():
    ap = Flask(__name__)
    ap.register_blueprint(app)
    return ap