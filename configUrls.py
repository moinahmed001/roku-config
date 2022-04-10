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
from bs4 import BeautifulSoup
from deepdiff import DeepDiff
import os
import requests
import datetime
from appFunctions import *
from request_getter import simple_get, simple_get_json, get_tariff
# from .appFunctions import *
# from .request_getter import simple_get, simple_get_json, get_tariff

config_urls = Blueprint('config_urls', __name__)



@config_urls.route("/config/feature/<version>")
def load_config_ui(version):
    try:
        return render_template("feature.html", version=version)
    except Exception as e:
        return str(e)

@config_urls.route("/peacock/config/feature/<version>")
def load_peacock_config_ui(version):
    try:
        return render_template("peacockFeature.html", version=version)
    except Exception as e:
        return str(e)

@config_urls.route("/config/envDiff/<string:version>")
def load_config_ui_for_env(version):
    try:
        return render_template("envDiff.html", version=version)
    except Exception as e:
        return str(e)

@config_urls.route("/config/<territory>/<env>")
def config_check(territory, env):
    config_version_from = request.args.get('config_version_from', default = '5.0', type = str)
    config_version_to = request.args.get('config_version_to', default = '5.0', type = str)
    base_url = "http://uat.config.sky.com"
    if (env.startswith('PROD')):
        base_url="http://config.ott.sky.com"

    url = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, config_version_from)
    url_to_compare = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, config_version_to)

    old_url_fetched_response = simple_get_json(url)
    new_url_fetched_response = simple_get_json(url_to_compare)

    diff_result = DeepDiff(json.loads(old_url_fetched_response), json.loads(new_url_fetched_response), ignore_order=True)

    try:
        return render_template("config_diff.html", diff_result = diff_result, territory=territory, config_version_from=config_version_from, config_version_to=config_version_to, env=env, url=url, url_to_compare=url_to_compare)
    except Exception as e:
        return str(e)

@config_urls.route("/peacock/config/<territory>/<env>")
def peacock_config_check(territory, env):
    # https://config.clients.peacocktv.com/US/NBCU/Peacock/Roku/PROD/3.2.10/config.json
    # https://config.clients.stable-int.peacocktv.com/US/NBCU/Peacock/Roku/STABLE_INT/3.2.10/config.json

    config_version_from = request.args.get('config_version_from', default = '3.4.10', type = str)
    config_version_to = request.args.get('config_version_to', default = '3.5.10', type = str)
    base_url = "https://config.clients.stable-int.peacocktv.com/US/NBCU/Peacock/Roku"
    if (env.startswith('PRO')):
        base_url="https://config.clients.peacocktv.com/US/NBCU/Peacock/Roku"

    if territory == "SHOWTIME":
        base_url = "http://uat.config.sky.com"

        if (env.startswith('PROD')):
            base_url="http://config.ott.sky.com"

    url = base_url + "/{0}/{1}/config.json".format(env, config_version_from)
    url_to_compare = base_url + "/{0}/{1}/config.json".format(env, config_version_to)

    old_url_fetched_response = simple_get_json(url)
    new_url_fetched_response = simple_get_json(url_to_compare)

    diff_result = DeepDiff(json.loads(old_url_fetched_response), json.loads(new_url_fetched_response), ignore_order=True)

    try:
        return render_template("peacock_config_diff.html", diff_result = diff_result, territory=territory, config_version_from=config_version_from, config_version_to=config_version_to, env=env, url=url, url_to_compare=url_to_compare)
    except Exception as e:
        return str(e)

@config_urls.route("/web/config/<territory>/<env>")
def web_config_check(territory, env):
    config_version_from = request.args.get('config_version_from', default = '4cf564f', type = str)
    config_version_to = request.args.get('config_version_to', default = 'aa1dfa9', type = str)
    if territory == 'es':
        if env == 'prod':
            full_url = 'https://www.sky.es/international/static/{0}/config/es/nowtv/nowtv/web/production/config.json'
    elif territory == 'gb':
        if env == 'prod':
            full_url = 'https://www.nowtv.com/international/static/{0}/config/gb/nowtv/nowtv/web/production/config.json'
    elif territory == 'ie':
        if env == 'prod':
            full_url = 'https://www.nowtv.com/international/static/{0}/config/ie/nowtv/nowtv/web/production/config.json'
    elif territory == 'it':
        if env == 'prod':
            full_url = 'https://www.nowtv.it/international/static/{0}/config/it/nowtv/nowtv/web/production/config.json'
    elif territory == 'de':
        if env == 'prod':
            full_url = 'https://skyticket.sky.de/international/static/{0}/config/de/nowtv/nowtv/web/production/config.json'



    url = full_url.format(config_version_from)
    url_to_compare = full_url.format(config_version_to)

    old_url_fetched_response = simple_get_json(url)
    new_url_fetched_response = simple_get_json(url_to_compare)

    diff_result = DeepDiff(json.loads(old_url_fetched_response), json.loads(new_url_fetched_response), ignore_order=True)

    try:
        return render_template("config_diff_web.html", live_config_hash = all_config_hash(), diff_result = diff_result, territory=territory, config_version_from=config_version_from, config_version_to=config_version_to, env=env, url=url, url_to_compare=url_to_compare)
    except Exception as e:
        return str(e)

# Config API urls

@config_urls.route('/api/config/<territory>/<env>')
def config_check_api(territory, env):
    config_version_from = request.args.get('config_version_from', default = '*', type = str)
    config_version_to = request.args.get('config_version_to', default = '*', type = str)
    base_url = "http://uat.config.sky.com"
    if (env.startswith('PROD')):
        base_url="http://config.ott.sky.com"

    url = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, config_version_from)
    url_to_compare = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, config_version_to)

    old_url_fetched_response = simple_get_json(url)
    new_url_fetched_response = simple_get_json(url_to_compare)

    diff_result = DeepDiff(json.loads(old_url_fetched_response), json.loads(new_url_fetched_response), ignore_order=True)
    diff_result2 = jsonify(diff_result)
    return diff_result2

@cross_origin()
@config_urls.route('/api/config/<territory>/<env>/<version>')
def load_config(territory, env, version):
    base_url = "http://uat.config.sky.com"
    if (env.startswith('PROD')):
        base_url="http://config.ott.sky.com"

    url = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, version)

    response = simple_get_json(url)
    diff_result = jsonify(json.loads(response))
    return diff_result

@cross_origin()
@config_urls.route('/peacock/api/config/<env>/<version>')
def load_config_peacock(env, version):
    # https://config.clients.peacocktv.com/US/NBCU/Peacock/Roku/PROD/3.2.10/config.json
    # https://config.clients.stable-int.peacocktv.com/US/NBCU/Peacock/Roku/STABLE_INT/3.2.10/config.json
    base_url = "https://config.clients.stable-int.peacocktv.com/US/NBCU/Peacock/Roku"
    if (env.startswith('PRO')):
        base_url="https://config.clients.peacocktv.com/US/NBCU/Peacock/Roku"

    url = base_url + "/{0}/{1}/config.json".format(env, version)

    response = simple_get_json(url)
    diff_result = jsonify(json.loads(response))
    return diff_result



@config_urls.route("/web/config/hash")
@cross_origin()
def web_config_hash():
    return jsonify(all_config_hash())





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
