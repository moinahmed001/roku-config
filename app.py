from flask import Flask, render_template, url_for
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
from octopusModel import *

from apiUrls import api_urls
from configUrls import config_urls

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
app.register_blueprint(api_urls)
app.register_blueprint(config_urls)

FlaskJSON(app)
Bootstrap(app)
CORS(app)
cache.init_app(app)


@app.route('/octopus/agile/tariff')
def display_tariff():
    data = updated_tariff_data()
    meross_data = []
    if len(data) > 0:
        valid_from = data[0]['valid_from']
        valid_to = data[-1]['valid_to']
        add_meross_data_to_tariff(valid_from, valid_to, data)
    try:
        links = []
        for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append(url)
        return render_template("displayTariff.html", tariffs=data, urls=links)
    except Exception as e:
        return str(e)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)
    # links is now a list of url, endpoint tuples
    return jsonify(links)

@app.route("/tv_status")
def tv_status():
    print ("Called root url at ", time.strftime('%d/%m/%Y %H:%M:%S'))
    if tv_is_off():
        return "TV is OFF!"
    else:
        return "TV is ON!"

@app.route("/mm")
def mm_start():
    print ("mm is called at ", time.strftime('%d/%m/%Y %H:%M:%S'))
    subprocess.call('cd /home/pi/MagicMirror && DISPLAY=:0 npm start', shell=True)
    return "starting mm"

@app.route("/turn_on")
def turn_on():
    print ("turn on is called at ", time.strftime('%d/%m/%Y %H:%M:%S'))
    if tv_is_off():
        print ("attempt to turn the TV on!")
      #  subprocess.call('pm2 start mm', shell=True)
        subprocess.call('vcgencmd display_power 1', shell=True)
     #   subprocess.call('fbset -accel true', shell=True)
        return "Turning on TV"
    else:
        print ("ERROR!! TV is currently ON!")
        return "ERROR!! TV is currently ON!"

@app.route("/turn_off")
def turn_off():
    print ("turn on is called at ", time.strftime('%d/%m/%Y %H:%M:%S'))
    if tv_is_off():
        print ("ERROR!! TV is currently OFF!")
        return "ERROR!! TV is currently OFF!"
    else:
        print ("attempt to turn the TV off!")
       # subprocess.call('fbset -accel false', shell=True)
        subprocess.call('vcgencmd display_power 0', shell=True)
        return "Turning off TV"

@app.route("/reboot")
def reboot():
    print ("attempt to reboot!")
    subprocess.call('pm2 stop mm', shell=True)
    time.sleep(3)
    subprocess.call('sudo reboot', shell=True)
    return "Will restart the device!"

@app.route("/restart-pi")
def restart_pi():
    print ("attempt to restart magic mirror!")
    subprocess.call('pm2 restart mm', shell=True)
    return "Will restart the magic mirror!"

# @app.route("/prayer_timetable")
# @cross_origin()
# @cache.cached(timeout=43200)
# def prayer_time():
#     print(time.time())
#     prayers = []
#     raw_html = simple_get('https://eastlondonmosque.org.uk')
#     html = BeautifulSoup(raw_html, 'html.parser')
#
#     for i, li in enumerate(html.select('.salah-time-row')):
#         if i==1:
#             to_print = li.text.replace("\n\nBegins\n", "").split("\n")
#
#             try:
#                 prayers.append({"Fajr": to_print[0]})
#                 prayers.append({"Dhuhr": to_print[1]})
#                 prayers.append({"Asr": to_print[2]})
#                 prayers.append({"Maghrib": to_print[3]})
#                 prayers.append({"Isha": to_print[4]})
#                 prayerDict = {"data":{"timings":{"Fajr":str(to_print[0]), "Dhuhr": to_print[1], "Asr": to_print[2], "Maghrib": to_print[3], "Isha": to_print[4]}}};
#
#             except Exception as e:
#                 print(e)
#
#     return jsonify(prayers)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
