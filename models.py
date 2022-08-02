from peewee import *

db = SqliteDatabase('turkishdevelopers.db')

class User(Model):
    discord_id = IntegerField()
    dp_point = IntegerField()
    is_gave_dp = BooleanField()

    class Meta:
        database = db # This model uses the "turkishdevelopers.db" database.


class Question(Model):
    question = TextField()
    answer = CharField(max_length=1)
    answered = BooleanField(default=False)
    answered_by = TextField(default='')
    is_published = BooleanField(default=False)

    class Meta:
        database = db # This model uses the "turkishdevelopers.db" database.