import enum

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum

db = SQLAlchemy()


class Format(Enum):
    aac = 'AAC'
    mp3 = 'MP3'
    wav = 'WAV'
    ogg = 'OGG'
    wma = 'WMA'


class Status(Enum):
    uploaded = 'UPLOADED'
    processed = 'PROCESSED'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    task = db.relationship('Task', cascade='all, delete, delete-orphan')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_format = db.Column(Enum(Format))
    new_format = db.Column(Enum(Format))
    status = db.Column(Enum(Status))
    timestamp = db.Column(db.String(128))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    file = db.relationship('File', cascade='all, delete, delete-orphan')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    extension = db.Column(Enum(Format))
    task = db.Column(db.Integer, db.ForeignKey("task.id"))


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    filename = fields.String()
    extension = fields.String()


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        include_fk = True
        load_instance = True

    original_format = fields.String()
    new_format = fields.String()
    status = fields.String()
    timestamp = fields.String()
    file = fields.List(fields.Nested(FileSchema()))


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        include_fk = True
        load_instance = True

    username = fields.String()
    email = fields.String()
    password = fields.String()
    tasks = fields.List(fields.Nested(TaskSchema()))