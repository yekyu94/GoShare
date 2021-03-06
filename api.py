from flask import Flask
from flask_restx import Resource, Api
from DB.db import db
from API.auth import Auth
from API.dirManage import DirManager
from API.fileManage import FileManager
import os, json

app = Flask(__name__)

with open('.secret') as f:
    conf = json.loads(f.read())
    app.config['SQLALCHEMY_DATABASE_URI'] = conf['db_config']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = conf['secret_key']
    app.config['UPLOAD_FOLDER'] = conf['upload_path']
    app.config['MAX_CONTENT_LENGTH'] = 1000000000

db.init_app(app)
db.app = app
db.create_all()

api = Api(
    app,
    version='0.1',
    title="API Server",
    description="API Server!",
    terms_url="/",
    contact="youngq.tistory.com",
    license="MIT"
)

api.add_namespace(Auth, '/auth')
api.add_namespace(DirManager, '/dir')
api.add_namespace(FileManager, '/file')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)