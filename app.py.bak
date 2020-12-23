from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_bootstrap import Bootstrap
import subprocess
import time
import delegator, json
from getter import simple_get, simple_get_json
from bs4 import BeautifulSoup
from deepdiff import DeepDiff

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
FlaskJSON(app)
Bootstrap(app)
CORS(app)
cache.init_app(app)

@app.route('/api/config/<territory>/<env>')
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
@app.route('/api/config/<territory>/<env>/<version>')
def load_config(territory, env, version):
    base_url = "http://uat.config.sky.com"
    if (env.startswith('PROD')):
        base_url="http://config.ott.sky.com"

    url = base_url + "/{0}/NowTV/NowTV/Roku/{1}/{2}/config.json".format(territory, env, version)

    response = simple_get_json(url)
    diff_result = jsonify(json.loads(response))
    return diff_result

@app.route("/config/feature/<version>")
def load_config_ui(version):
    try:
        return render_template("feature.html", version=version)
    except Exception, e:
        return str(e)

@app.route("/config/envDiff/<string:version>")
def load_config_ui_for_env(version):
    try:
        return render_template("envDiff.html", version=version)
    except Exception, e:
        return str(e)

@app.route("/config/<territory>/<env>")
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
    except Exception, e:
        return str(e)

@app.route("/prayer_timetable")
@cross_origin()
@cache.cached(timeout=43200)
def prayer_time():
    print(time.time())
    prayers = []
    raw_html = simple_get('https://eastlondonmosque.org.uk')
    html = BeautifulSoup(raw_html, 'html.parser')

    for i, li in enumerate(html.select('.salah-time-row')):
        if i==1:
            to_print = li.text.replace("\n\nBegins\n", "").split("\n")

            try:
                prayers.append({"Fajr": to_print[0]})
                prayers.append({"Dhuhr": to_print[1]})
                prayers.append({"Asr": to_print[2]})
                prayers.append({"Maghrib": to_print[3]})
                prayers.append({"Isha": to_print[4]})
                prayerDict = {"data":{"timings":{"Fajr":str(to_print[0]), "Dhuhr": to_print[1], "Asr": to_print[2], "Maghrib": to_print[3], "Isha": to_print[4]}}};

            except Exception ,e:
                print str(e)

    return jsonify(prayers)

@app.route("/")
def hello():
    print "Called turn_off at ", time.strftime('%d/%m/%Y %H:%M:%S')
    if tv_is_off():
        return "TV is OFF!"
    else:
        return "TV is ON!"

@app.route("/turn_on")
def turn_on():
    print "turn on is called at ", time.strftime('%d/%m/%Y %H:%M:%S')
    if tv_is_off():
        print "attempt to turn the TV on!"
        subprocess.call('pm2 restart omx_stream1', shell=True)
        subprocess.call('tvservice -p', shell=True)
        subprocess.call('fbset -accel true', shell=True)
        return "Turning on TV"
    else:
        print "ERROR!! TV is currently ON!"
        return "ERROR!! TV is currently ON!"

@app.route("/turn_off")
def turn_off():
    print "turn on is called at ", time.strftime('%d/%m/%Y %H:%M:%S')
    if tv_is_off():
        print "ERROR!! TV is currently OFF!"
        return "ERROR!! TV is currently OFF!"
    else:
        print "attempt to turn the TV off!"
        subprocess.call('pm2 stop omx_stream1', shell=True)
        subprocess.call('fbset -accel false', shell=True)
        subprocess.call('tvservice -o', shell=True)
        return "Turning off TV"

@app.route("/reboot")
def reboot():
    print "attempt to reboot!"
    subprocess.call('pm2 stop omx_stream1', shell=True)
    subprocess.call('pm2 stop MagicMirror', shell=True)
    time.sleep(3)
    subprocess.call('sudo reboot', shell=True)
    return "Will restart the device!"

@app.route("/restart-pi")
def restart_pi():
    print "attempt to restart magic mirror!"
    subprocess.call('pm2 stop omx_stream1', shell=True)
    subprocess.call('pm2 restart MagicMirror', shell=True)
    subprocess.call('pm2 start omx_stream1', shell=True)
    return "Will restart the magic mirror!"

def tv_is_off():
    p = delegator.run('tvservice -s')
    if "TV is off" in p.out:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
