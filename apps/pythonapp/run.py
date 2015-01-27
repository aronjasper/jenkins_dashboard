from flask import Flask
from flask import render_template
import requests
import json
from operator import itemgetter

app = Flask(__name__)

base_url = 'http://54.148.201.225:8080/'
#base_url = 'http://builds.apache.org/'

@app.route('/')
def get_all_jobs():
    try:
        r = requests.get(base_url + 'api/json?pretty=true')
        data = r.json()['jobs']
        #temp = json.dumps(data)
        #temp = json.loads(temp)
        data = sorted(data, key=itemgetter('color'), reverse=True)
        #return json.dumps(data)
        return render_template("dashboard.html", jobs=data)
    except requests.exceptions.HTTPError, e:
        #return e
        return render_template("error.html", error=e)
    except requests.exceptions.ConnectionError, e:
        #return e
        return render_template("error.html", error=e)

@app.route('/<jobname>')
def get_job_details(jobname):
    try:
        r = requests.get(base_url + 'job/' + jobname + '/api/json?pretty=true')
        data = r.json()

        return render_template("job-details.html", details=data)
    except requests.exceptions.HTTPError, e:
        return render_template("error.html", error=e)
    except requests.exceptions.ConnectionError, e:
        return render_template("error.html", error=e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
