#import os
#import sys
#fpath = os.path.join(os.path.dirname(__file__), 'app')
#sys.path.append(fpath)

from hello import hello
from flask import Flask
import os

application = Flask(__name__)
@application.route('/')
def index():
    endpoint = os.environ['API_ENDPOINT']
    return hello(f'AWS EB! {endpoint}')

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)