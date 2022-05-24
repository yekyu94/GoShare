from flask import request
from flask_restx import Resource, Api, Namespace, reqparse
from DB.db import db, Dir, Files, Users
from API.auth import checkToken
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from flask_restx import abort
import json, time, werkzeug, os


FileManager = Namespace(
    name="fileManage",
    description="File Manager",
)

secret = ""
with open('.secret') as f:
    conf = json.loads(f.read())
    secret = conf['secret_key'] + str(time.time())
    upload_path = conf['upload_path']
    
@FileManager.route('/MakeFile')
class MakeDir(Resource):
    def post(self):
        try:
            pid = str(request.json.get('pid'))
            fname = str(request.json.get('fname'))
            fsize = str(request.json.get('fsize'))

            id = str(request.json.get('id'))
            token = str(request.json.get('token'))
            seed = str(request.json.get('seed'))

            if(pid.isdecimal() and fsize.isdecimal()):
                pid = int(pid)
                fsize = int(fsize)
                if(fsize < 0): return 1
            else: return 1

            checkToken(id, token, seed)

            checkId = db.session.query(Dir).filter(Dir.pid==pid).first()
            if(checkId == None): return 2   #해당하는 폴더 없음
            checkName = db.session.query(Files).filter(and_(Files.pid==pid, Files.fname == fname)).first()
            if(checkName != None): return 3     #해당하는 폴더에 동일한 파일명 존재
            user = db.session.query(Users).filter(Users.id==id).first()
            # fname, pid, fsize = 0, uid

            db.session.add(Files(fname, pid, fsize, user.uid))
            db.session.commit()

            file = db.session.query(Files).filter(and_(Files.pid == pid, Files.fname == fname, Files.uid == user.uid)).first()
            return {'fid' : file.fid}
        except BadRequest as e:
            return {'ERROR': str(e)}
        except Exception as e:
            return {'ERROR': '1'}



@FileManager.route('/Upload')
class Upload(Resource):
    def post(self):
        try:
            id = str(request.form['id'])
            token = str(request.form['token'])
            seed = str(request.form['seed'])
            fid = str(request.form['fid'])
            fsize = str(request.form['fsize'])
            fname = str(request.form['fname'])

            checkToken(id, token, seed)

            parser = reqparse.RequestParser()
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            args = parser.parse_args()
            file_opject = args['file']
            file_opject.seek(0, os.SEEK_END)
            fileSize = file_opject.tell()

            file_opject.seek(0)
            print(fileSize)

            file = db.session.query(Files).filter(and_(Files.fid == fid, Files.fsize == fsize, Files.fname == fname)).first()

            if(file == None):
                raise BadRequest('업로드 오류')
            if(fileSize != file.fsize):
                raise BadRequest('파일용량 오류')

            filename = secure_filename(file_opject.filename)
            print(filename)
            file_opject.save(upload_path + str(file.fid))

            file.fsize = fileSize

            db.session.add(file)
            db.session.commit()
            return {'upload' : 'ok'}
        except BadRequest as e:
            return {'ERROR': str(e)}
        except Exception as e:
            return {'ERROR': str(e)}
 