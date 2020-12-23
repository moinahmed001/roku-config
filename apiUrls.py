from flask import Flask, render_template, Blueprint
from flask import jsonify
from flask import request
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_bootstrap import Bootstrap
import subprocess
import time, re
import delegator, json
from getter import simple_get, simple_get_json, get_tariff
from bs4 import BeautifulSoup
from deepdiff import DeepDiff
import os
import requests
import datetime
from appFunctions import *

api_urls = Blueprint('api_urls', __name__)

@api_urls.route('/api/octopus/agile/tariff')
def fetch_new_tariff():
    parsed = updated_tariff_data()
    result = jsonify(parsed)
    return result

@api_urls.route('/api/octopus/agile/consumption')
def fetch_new_consumption():
    parsed = consumption_data()
    result = jsonify(parsed)
    return result

@api_urls.route('/api/octopus/agile/consumption/daily')
def fetch_new_consumption_daily():
    parsed = consumption_data_daily()
    result = jsonify(parsed)
    return result

@api_urls.route('/api/meross/<device>/<switch>')
def run_file(device, switch):
    cmd = "python3 plug.py {0} {1}".format(device,switch)
    os.system(cmd)
    return "test"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
