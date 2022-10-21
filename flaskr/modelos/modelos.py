import enum

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime, timezone, timedelta
from sqlalchemy import DateTime

db = SQLAlchemy()

class Format(enum.Enum):
    aac = 'AAC'
    mp3 = 'MP3'
    wav = 'WAV'
    ogg = 'OGG'
    wma = 'WMA'


class Status(enum.Enum):
    uploaded = 'UPLOADED'
    processed = 'PROCESSED'


class Username(db.Model):
    __tablename__ = 'username'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128))
    task = db.relationship('Task', backref='username', cascade='all, delete, delete-orphan')


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    original_format = db.Column(db.String(128))
    new_format = db.Column(db.String(128))
    status = db.Column(db.String(128))
    timestamp = db.Column(DateTime(timezone=True), default=datetime.now())
    file = db.relationship('File', cascade='all, delete, delete-orphan')
    user = db.Column(db.Integer, db.ForeignKey("username.id"))



class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    extension = db.Column(db.String(128))
    task = db.Column(db.Integer, db.ForeignKey("task.id"))


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_fk = True
        load_instance = True

    filename = fields.String()
    extension = fields.String()


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

    original_format = fields.String()
    new_format = fields.String()
    status = fields.String()
    timestamp = fields.String()
    file = fields.List(fields.Nested(FileSchema()))


class UsernameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Username
        include_relationships = True
        include_fk = True
        load_instance = True

    username = fields.String()
    email = fields.String()
    password = fields.String()
    tasks = fields.List(fields.Nested(TaskSchema()))
