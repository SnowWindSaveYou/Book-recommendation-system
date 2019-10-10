from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort,Response
import os
import base64

from datetime import *
import time
import json


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#------------------------------------------------------------------------------------
# Server apis
# 
#------------------------------------------------------------------------------------
@app.route('/')
def home():
    return 'welcome'


@app.route('/test',methods=['GET'])
def test():
    return jsonify("test")





#------------------------------------------------------------------------------------
# 
# 
#------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()(debug=True)