from flask import Flask, render_template, redirect, jsonify, request, make_response, session, abort
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.loginform import LoginForm
from forms.news import NewsForm
from blueprint import news_api
from flask_restful import reqparse, abort, Api, Resource
from blueprint import news_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_123'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)

    api.add_resource(news_resources.UsersListResource, '/api/v2/users')
    api.add_resource(news_resources.UsersResource, '/api/v2/users/<int:users_id>')

    app.run(port='8080', host='127.0.0.1')
