from flask import Flask
from flask import request
from flask import json  #importing json cause that’s what we’re going to be working with
import configparser
import git

app = Flask(__name__)
cp = configparser.ConfigParser()
cp.read('config.ini')


@app.route('/')
def root():
  return ''

@app. route('/refresh', methods=['POST'])
def hook_root():
    if request.headers['Content-Type'] == 'application/json':
        g = git.cmd.Git("https://github.com/turkish-developers/turkish-developers-bot.git")
        status = g.pull()
        return json.dumps({'status': status})

if __name__ == '__main__':
  app.run(debug=True)