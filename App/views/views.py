import datetime
from flask import Blueprint, Response, jsonify, redirect, render_template, request, make_response, session, url_for 
from ..models.models import *

blog = Blueprint('blog', __name__)

@blog.route('/home/')
@blog.route('/')
def home():
    photos = PhotoModel.query.limit(6)
    categories = CategoryModel.query.all()
    articles = ArticalModel.query.all()
    return render_template('home/index.html',
                           photos = photos,
                           categories = categories,
                           articles = articles,
                           renderAbout = True,
                           renderSearch = False)

@blog.route('/accomplishments/')
def blog_photo():
    photos = PhotoModel.query.all()
    return render_template('home/photos.html',
                           photos = photos
                        )

@blog.route('/article/<categoryId>/')
@blog.route('/article/')
def blog_articles(categoryId = None):
    if categoryId: 
        categories = CategoryModel.query.filter_by(id = categoryId).all()
        articles = ArticalModel.query.filter_by(category_id = categoryId).all()
    else:
        categories = CategoryModel.query.all()
        articles = ArticalModel.query.all()
    # renderSearch = True after finishing search function
    return render_template('home/article.html',
                           categories = categories,
                           articles = articles,
                           renderAbout = False,
                           renderSearch = False)

@blog.route('/about/')
def blog_about():
    categories = CategoryModel.query.all()
    return render_template('home/about.html',
                           categories = categories,
                           renderAbout = True,
                           renderSearch = False
                           )