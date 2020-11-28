from peewee import *
import settings
from playhouse.sqlite_ext import JSONField

db = SqliteDatabase(settings.database_path)

class User(Model):
    id = AutoField()
    username = TextField(null=True)
    first_name = TextField(null=True)
    second_name = TextField(null=True)
    chat_id = IntegerField(null=False)

    class Meta:
        database = db


class Vacancy(Model):
    id = AutoField()
    creator = ForeignKeyField(User)
    name = TextField()
    specialization = TextField()
    description = TextField()
    key_skills = TextField()
    income = TextField()
    test_task = TextField(null=True)

    class Meta:
        database = db


class Candidate(Model):
    id = AutoField()
    user = ForeignKeyField(User)
    vacancy = ForeignKeyField(Vacancy)
    resume_file_id = TextField()
    resume_json = JSONField()
    status = TextField()
    test_task_solution = TextField(null=True)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([User,Vacancy,Candidate,])