from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import DateTime

db = SQLAlchemy()


class Username(db.Model):
    __tablename__ = 'username'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    file = db.relationship('File', backref='username', cascade='all, delete, delete-orphan')


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1000))
    extension = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    task = db.relationship('Task', cascade='all, delete, delete-orphan')
    user = db.Column(db.Integer, db.ForeignKey("username.id"))


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    original_format = db.Column(db.String(128))
    new_format = db.Column(db.String(128))
    status = db.Column(db.String(128))
    timestamp = db.Column(DateTime(timezone=True), default=datetime.now())
    file = db.Column(db.Integer, db.ForeignKey("file.id"))


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


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_fk = True
        load_instance = True

    filename = fields.String()
    extension = fields.String()
    location = fields.String()
    task = fields.List(fields.Nested(TaskSchema()))


class UsernameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Username
        include_relationships = True
        include_fk = True
        load_instance = True

    username = fields.String()
    email = fields.String()
    password = fields.String()
    file = fields.List(fields.Nested(FileSchema()))




