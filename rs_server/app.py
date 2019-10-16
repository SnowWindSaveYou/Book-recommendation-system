from flask import Flask, url_for, render_template, jsonify, request,escape, make_response, send_from_directory, abort,Response
from flask_sqlalchemy import SQLAlchemy
import json
import os
import base64
import torch
from models import NeuMF

# from datetime import *
# import time



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#------------------------------------------------------------------------------------
# Database model
# 
#------------------------------------------------------------------------------------
app.config.from_pyfile('db_config.ini')
db = SQLAlchemy(app)


class UserRating(db.Model):
    __tablename__ = 'rating_record'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    def __init__(self, user_id, book_id,rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating

#------------------------------------------------------------------------------------
# 
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

# def get_user_rating_count(user_id):
#     return count

def get_user_ratings(user_id):
    rating_result = UserRating.query,filter(UserRating.user_id == user_id)
    ratings = []
    for result in rating_result:
        record = dict((zip(keys, result)))
        ratings.append(record)
    return ratings

def add_user_rating(user_id,book_id,rating):
    record = UserRating.query,filter(user_id = user_id, book_id = book_id, rating = rating)
    db.session.add(record)
    db.session.commit()
    return ratings

#------------------------------------------------------------------------------------
# Server apis
# 
#------------------------------------------------------------------------------------
@app.route('/')
def home_page():
    # req = json.loads(request.data)
    # user_id = req['user_id']
    # recommend_list = get_recommend_list(user_id)
    # recommend_info = get_book_infos(recommend_list)
    recommend_info = get_book_infos([1,2,3,4,5])
    return render_template('home.html',
        recommend_info = recommend_info
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
# Models 
# 
#------------------------------------------------------------------------------------

# NeuMF_RS = torch.load('./models')

def get_mf_results(user_id):
    pass

def get_item_results(user_id):
    pass

def get_simi_item_results(item_id):
    pass


def get_recommend_list(user_id):
    user_ratings = get_user_ratings(user_id)
    recommend_list = []
    if user_ratings >30:
        result = get_mf_results(user_id)
    else:
        recommend_list = [1,2,3,4,5,6,7,8,9,10]
    return recommend_list
#------------------------------------------------------------------------------------r
# 
# 
#------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()(debug=True)