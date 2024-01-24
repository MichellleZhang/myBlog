import datetime
from flask import Blueprint, Response, jsonify, redirect, render_template, request, make_response, session, url_for 
from ..models.models_admin import *
from ..models.models import *
import time
import boto3

admin = Blueprint('admin', __name__)

s3 = boto3.client('s3')
BUCKET_NAME = 'zqc-blog-resources'

from functools import wraps
def login_require(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        userId = request.cookies.get('user_id', None)
        if userId:
            user = AdminUserModel.query.get(userId)
            request.user = user
            return fn(*args, **kwargs)
        else:
            return redirect('/admin/login/')
    return inner

@admin.route('/admin/')
@admin.route('/admin/index/')
@login_require
def index():
    # userId = request.cookies.get('user_id', None)
    # if userId:
    user = request.user
    categories = CategoryModel.query.filter()
    articles = ArticalModel.query.filter()
    accomplishments = PhotoModel.query.filter()
    return render_template('admin/index.html', 
                            username = user.name,
                            categories = categories,
                            articles = articles,
                            accomplishments = accomplishments
                        )
    
    # else:
    #     return redirect('/admin/login/')

@admin.route('/admin/login/', methods = ['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        user = AdminUserModel.query.filter_by(name =username, password = password).first()
        if user:
            response = redirect('/admin/index')
            response.set_cookie('user_id', str(user.id), max_age=7*24*3600)
            return response
        else:
            return 'Load fail'
        
@admin.route('/admin/logout/')
def logout():
    response = redirect('/admin/login/')
    response.delete_cookie('user_id')
    return response

@admin.route('/admin/category/')
@login_require
def admin_category():
    user = request.user
    categories = CategoryModel.query.all()
    return render_template('admin/category.html',
                           username = user.name,
                           categories = categories
                        )

@admin.route('/admin/addcategory/', methods = ['GET', 'POST'])
@login_require
def admin_addCategory():
    if request.method == 'POST':
        name = request.form.get('name')
        describe = request.form.get('describe')
        newCategory = CategoryModel()
        newCategory.name = name
        newCategory.describe = describe

        try:
            db.session.add(newCategory)
            db.session.commit()
        except Exception as e:
            print("e: ", e)
            db.session.rollback()
        return redirect('/admin/category/') 
    else:
        return 'Invalid Request methods'

@admin.route('/admin/deletecategory/', methods = ['GET', 'POST'])
@login_require
def admin_deleteCategory():
    if request.method == 'POST':
        id = request.form.get('id')
        category = CategoryModel.query.get(id)
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            print("e: ", e)
        return jsonify({'code': 200, 'msg': 'delete successfully! '})
    else:
        return jsonify({'code': 400, 'msg': 'delete fail! '})


@admin.route('/admin/updateCategory/<id>/', methods = ['GET', 'POST'])
@login_require
def admin_updateCategory(id):
    if request.method == 'GET':
        category = CategoryModel.query.get(id)
        return render_template('admin/category_update.html',
                               username = request.user.name,
                               category = category)
    elif request.method == 'POST':
        category = CategoryModel.query.get(id)
        name = request.form.get('name')
        describe = request.form.get('describe')
        category.name = name
        category.describe = describe
        try:
            db.session.commit()
        except Exception as e:
            print("e: ", e)
        return redirect('/admin/category/')
    else:
        return 'Invalid Request methods'
    
@admin.route('/admin/article/')
@login_require
def admin_article():
    Articles = ArticalModel.query.all()
    return render_template('admin/article.html',
                           Articles = Articles,
                           username = request.user.name
                           )

@admin.route('/admin/article/add/', methods = ['GET', 'POST'] )
@login_require
def admin_addarticle():
    if request.method == 'GET':
        categories =  CategoryModel.query.all()
        return render_template('admin/article_add.html',
                            username = request.user.name,
                            categories = categories
                            )
    elif request.method == 'POST':
        newArticle = ArticalModel()
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img')
        img_name = f'{time.time()} -- {img.filename}'
        img_url = f'articles/{img_name}'
        # wrtie the img path to db （* the same fillname will be covered）
        try:
            newArticle.name = name
            newArticle.keyWord = keywords
            newArticle.content = content
            newArticle.category_id = category
            newArticle.img = img_url
            db.session.add(newArticle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e', e )
            # store img to s3 
        else:
            localPath = f'/Users/zqc/Desktop/blogResoueces/articles/' + img.filename
            with open(localPath, "rb") as f:
                s3.upload_fileobj(f, BUCKET_NAME, img_url, ExtraArgs={"ACL":"public-read"})
    return redirect('/admin/article/')

@admin.route('/admin/article/delete/', methods=['GET', 'POST'])
@login_require
def admin_deletearticle():
    if request.method == 'POST':
        id = request.form.get('id')
        article = ArticalModel.query.get(id)
        try:
            db.session.delete(article)
            db.session.commit()
        except Exception as e:
            print ('e: ', e)
            return jsonify({'code': 500, 'msg': 'delete fail!' })
        return jsonify({'code': 200, 'msg': 'delete successfully!'})
    return jsonify({'code': 400, 'msg': 'Invalid request ethods!'})
    
@admin.route('/admin/article/update/<id>/', methods = ['GET','POST'])
@login_require
def admin_updatearticle(id):
    article = ArticalModel.query.get(id)
    if request.method == 'GET':
        categories = CategoryModel.query.all()
        return render_template('admin/article_update.html',
                            username = request.user.name,
                            categories = categories,
                            article = article)
    elif request.method == 'POST':
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img')
        img_name = f'{time.time()} -- {img.filename}'
        img_url = f'articles/{img_name}'
        try:
            article.name = name
            article.keyWord = keywords
            article.content = content
            article.category_id = category
            article.img = img_url
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e: ',e)
    return redirect('/admin/article/')

@admin.route('/admin/accomplishments/')
@login_require
def admin_accomplishments():
    photos = PhotoModel.query.all()
    return render_template('admin/accomplishments.html',
                           username = request.user.name,
                           photos = photos)

@admin.route('/admin/accomplishments/add/', methods = ['GET','POST'])
@login_require
def admin_add_accomplishments():
    newAcc = PhotoModel()
    if request.method == 'GET':
        return render_template('admin/accomplishments_add.html',
                               username = request.user.name)
    elif request.method == 'POST':
        name = request.form.get('name')
        describe = request.form.get('describe')
        img = request.files.get('img')
        img_name = f'{time.time()} -- {img.filename}'
        img_url = f'accomplishments/{img_name}'
        try:
            newAcc.name = name 
            newAcc.describe = describe 
            newAcc.url = img_url 
            db.session.add(newAcc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e: ', e)
        else:
            localPath = f'/Users/zqc/Desktop/blogResoueces/accomplishments/' + img.filename
            with open(localPath, "rb") as f:
                s3.upload_fileobj(f, BUCKET_NAME, img_url, ExtraArgs={"ACL":"public-read"})
    return redirect('/admin/accomplishments/')

@admin.route('/admin/accomplishments/update/<id>/', methods = ['GET','POST'])
@login_require
def admin_update_accomplishments(id):
    accomplishment = PhotoModel.query.get(id)
    if request.method == 'GET':
        return render_template('admin/accomplishments_update.html',
                            username = request.user.name,
                            accomplishment = accomplishment)
    elif request.method == 'POST':
        name = request.form.get('name')
        describe = request.form.get('describe')
        img = request.files.get('img')
        img_name = f'{time.time()} -- {img.filename}'
        img_url = f'accomplishments/{img_name}'
        try:
            accomplishment.name = name 
            accomplishment.describe = describe 
            accomplishment.img = img_url 
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print('e: ', e)
    return redirect('/admin/accomplishments/')
            
@admin.route('/admin/accomplishments/delete/', methods = ['GET', 'POST'])
@login_require
def admin_delete_accomplishment():
    if request.method == 'POST':
        id = request.form.get('id')
        targetAcc = PhotoModel.query.get(id)
        try:
            db.session.delete(targetAcc)
            db.session.commit()
        except Exception as e:
            print ('e: ', e)
            return jsonify({'code': 500, 'msg': 'delete fail!' })
        return jsonify({'code': 200, 'msg': 'delete successfully!'})
    return jsonify({'code': 400, 'msg': 'Invalid request ethods!'})
