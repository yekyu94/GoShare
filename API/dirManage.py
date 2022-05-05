from flask import request
from flask_restx import Resource, Api, Namespace
from DB.db import db, Dir
from API.auth import checkToken
from sqlalchemy import and_
import json, time

DirManager = Namespace(
    name="dirManage",
    description="Dir Manager",
)

secret = ""
with open('.secret') as f:
    conf = json.loads(f.read())
    secret = conf['secret_key'] + str(time.time())
'''
Return
   -1 : Error
    0 : 정상
    1 : 입력오류
    2 : ppid 오류
'''
@DirManager.route('/MakeDir')
class MakeDir(Resource):
    def post(self):
        try:
            ppid = str(request.json.get('ppid'))
            path = str(request.json.get('path'))
            token = str(request.json.get('token'))
            seed = str(request.json.get('seed'))
            if(ppid.isdecimal() and path.isalnum()):
                ppid = int(ppid)
            else:
                return 1
            
            # check = checkToken(id, token, seed)
            # if(check == 1):
            #     return '토큰 파기'
            # elif(check == 2):
            #     return '토큰 오류'

            checkId = db.session.query(Dir).filter(Dir.pid==ppid).first()
            if(checkId == None):
                return 2
            checkName = db.session.query(Dir).filter(and_(Dir.ppid==ppid, Dir.path == path)).first()
            if(checkName != None):
                return 3
            db.session.add(Dir(path, ppid))
            db.session.commit()
            return 0
        except:
            return -1
