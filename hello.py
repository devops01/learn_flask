# coding:utf-8
import sys, os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap
# Flask-Moment本地化日期和时间
from flask_moment import Moment
# 表单
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# 数据库
from flask_sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf-8')

basedir = os.path.abspath(os.path.dirname(__file__))
# 创建flask实例类
app = Flask(__name__)
# 设置安全key
app.config['SECRET_KEY'] = 'Hard to guess string'
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# SQLAlchemy类实例
db = SQLAlchemy(app)

manager = Manager(app)
# 引用bootstrap框架
bootstrap = Bootstrap(app)
# 本地化本地日期和时间类实例
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<p> 你的浏览器是: %s</p>' % user_agent
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            print '#' * 20
            flash('Looks like you have changed your name')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class Role(db.Model):
    '''
	定义表role模型
	'''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    '''
    定义表users模型
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.name

if __name__ == '__main__':
    manager.run()
