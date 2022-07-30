from peewee import *

db = SqliteDatabase('turkishdevelopers.db')

class User(Model):
    discord_id = IntegerField()
    dp_point = IntegerField()
    is_gave_dp = BooleanField()

    class Meta:
        database = db # This model uses the "turkishdevelopers.db" database.