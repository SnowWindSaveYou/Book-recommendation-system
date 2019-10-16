from flask import Flask, url_for, render_template, jsonify, request,escape, make_response, send_from_directory, abort,Response
from flask_sqlalchemy import SQLAlchemy
import os
import base64

# from datetime import *
# import time
# import json


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#------------------------------------------------------------------------------------
# Database 
# 
#------------------------------------------------------------------------------------
app.config.from_pyfile('db_config.ini')
db = SQLAlchemy(app)

#------------------------------------------------------------------------------------
# Server apis
# 
#------------------------------------------------------------------------------------
@app.route('/home')
def home_page():

    #TEST 
    book_infos = get_book_infos([1,2,3,4,5])

    return render_template('home.html',
        recommend_list = book_infos
    )


@app.route('/test',methods=['GET'])
def test():
    a = get_book_infos([1,2,3,4,5])
    return jsonify(a)


@app.route('/book/<int:book_id>',methods=['GET'])
def book_page(book_id):
    book_info = get_book_info(book_id)
    if book_info == None:
        return render_template('404.html')
    return render_template('book.html', home_url = url_for('home_page'),
        book_id=book_id, 
        book_title = book_info['title'],
        book_authors = book_info['authors'],
        book_language = book_info['language_code'],
        book_rating = book_info['average_rating'],
        book_cover = book_info['image_url'],
        )

#------------------------------------------------------------------------------------
# DB APIs
# 
#------------------------------------------------------------------------------------
def get_book_info(book_id):
    book_info_result = db.session.execute('select * from books where book_id = {}'.format(book_id))
    keys = book_info_result.keys()
    infos = list(book_info_result)
    if len(infos)<1:
        return None
    book_info = dict((zip(keys, infos[0])))
    return book_info


def get_book_infos(book_ids):
    book_info_result = db.session.execute('select * from books where book_id in ({})'.format(str(book_ids)[1:-1]))
    keys = book_info_result.keys()
    book_infos = []
    for result in book_info_result:
        book = dict((zip(keys, result)))
        book_infos.append(book)
    return book_infos
#------------------------------------------------------------------------------------
# Models APIs
# 
#------------------------------------------------------------------------------------

def get_mf_results(user_id):
    pass

def get_item_results(user_id):
    pass

def get_simi_item_results(item_id):
    pass




#------------------------------------------------------------------------------------r
# 
# 
#------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()(debug=True)