from flask import request
from flask_restx import Resource, Api, Namespace
from DB.db import db, Users
from werkzeug.exceptions import BadRequest
import bcrypt, jwt, random, json, time

Auth = Namespace(
    name="Auth",
    description="Auth & Make Key",
)

TokenGroup = dict()
Timer = dict()

secret = ""
with open('.secret') as f:
    conf = json.loads(f.read())
    secret = conf['secret_key'] + str(time.time())

@Auth.route('/getToken')
class GetToken(Resource):
    def post(self):
        try:
            id = str(request.json.get('id'))
            pw = str(request.json.get('pw'))

            user = db.session.query(Users).filter(Users.id==id).first()     # 사용자의 계정정보 확인
            if(bcrypt.checkpw(pw.encode("utf-8"), user.pw)):                # 사용자의 계정암호가 동일한지 확인
                global tokenGroup, Timer
                seed = str(int(random.random() * 100000))
                token = jwt.encode({'user':id}, secret+seed, algorithm="HS256").decode("utf-8")
                TokenGroup[id] = token
                Timer[id] = time.time()
                return { 'Auth' : token, 'seed' : seed}
            return {'Auth' : '0', 'seed' : '0'}
        except:
            return {'ERROR': '01'}

@Auth.route('/APITest')
class APITest(Resource):
    def post(self):
        try:
            id = request.json.get('id')
            token = request.json.get('token')
            seed = request.json.get('seed')
            
            checkToken(id, token, seed)
        except:
            return 'Error'


'''
Return
   -1 : Error
    0 : 정상
    1 : 토큰 파기
    2 : 토큰 오류
'''
def checkToken(id, token, seed):
    return True
    try:
        abort(400, custom='value')
        global Timer, TokenGroup

        if((time.time() - Timer[id]) > 600):    # 토큰 만료
            Timer.pop(id)
            TokenGroup.pop(id)
            raise BadRequest('토큰 만료')

        if(TokenGroup[id] == token):        # 토큰 확인 
            if(jwt.decode(token.encode("utf-8"), secret+seed, algorithm="HS256")['user'] == id):
                Timer[id] = time.time()     # 최종 접속시간 갱신
                return True         # 인증 성공
            else:
                raise BadRequest('토큰 오류')        # 토큰 정보 틀림
        else:
            raise BadRequest('토큰 오류')
    except:
        raise BadRequest('인증 오류')


#db.session.commit()
#encrypted_password = bcrypt.hashpw("cocoa".encode("utf-8"), bcrypt.gensalt())
#x.pw = encrypted_password
#db.session.commit()