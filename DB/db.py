from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Files(db.Model):
    __tablename__ = 'Files'

    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.Text, nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('Dir.pid'), nullable=False)
    fsize = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable=False)
    del_yn = db.Column(db.Integer, nullable=False)

    def __init__(self, fid, fname, fsize = 0, del_yn = 0):
        self.fid = fid
        self.fname = fname
        self.fsize = fsize
        self.del_yn = del_yn

    Share = db.relationship("Share", cascade = "all, delete")

class Dir(db.Model):
    __tablename__ = 'Dir'

    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.Text, nullable=False)
    ppid = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, path, ppid = 0):
        self.pid = pid
        self.path = path
        self.ppid = ppid

    Files = db.relationship("Files", cascade = "all, delete")

class Users(db.Model):
    __tablename__ = 'Users'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Text, unique=True, nullable=False)
    pw = db.Column(db.Text, nullable=False)
    mail = db.Column(db.Text, nullable=False)
    del_yn = db.Column(db.Integer, nullable=False)

    def __init__(self, uid, id, pw, mail, del_yn = 0):
        self.uid = uid
        self.id = id
        self.pw = pw
        self.mail = mail
        self.del_yn = del_yn

    def __repr__(self):
        return '<Users %r>' % (self.id)

    Files = db.relationship("Files", cascade = "all, delete")

class Logs(db.Model):
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Date)
    id = db.Column(db.Text)
    task = db.Column(db.Integer)
    data = db.Column(db.Text)

    def __init__(self, tid, time, id, task, data):
        self.tid = tid
        self.time = time
        self.id = id
        self.task = task
        self.data = data
    
class Share(db.Model):
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fid = db.Column(db.Integer, db.ForeignKey('Files.fid'), nullable=False)
    uid = db.Column(db.Integer, nullable=True)
    code = db.Column(db.Integer, nullable=True)
    pin = db.Column(db.Integer, nullable=True)

    def __init__(self, sid, fid, uid, code, pin):
        self.sid = sid
        self.fid = fid
        self.uid = uid
        self.code = code
        self.pin = pin

class Timer(db.Model):
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=True)
    id = db.Column(db.Integer, nullable=True)
    timer = db.Column(db.Integer, nullable=True)

    def __init__(self, tid, type, id, timer):
        self.tid = tid
        self.type = type
        self.id = id
        self.timer = timer