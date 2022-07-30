from models import *
db.connect()
db.create_tables([User])

class UserView:
    def __init__(self, discord_id):
        self.user = self.create_user_if_not_exists(discord_id=discord_id)

        

    def create_user_if_not_exists(self, discord_id):
        user = User.select().where(User.discord_id == discord_id)

        if not user.exists():
            user = User.create(discord_id=discord_id,dp_point=0,is_gave_dp=False)
        else:
            user = user.get()

        return user


    def get_user_developer_point(self):
        return self.user.dp_point
         
    def increase_user_developer_point(self, other_user_discord_id):
        if not self.user.is_gave_dp:
            other_user = self.create_user_if_not_exists(other_user_discord_id)
            other_user.dp_point += 1
            other_user.save()
            self.user.is_gave_dp = True
            self.user.save()
            return True, UserView(other_user_discord_id)
        else:
            return False, ''

    @staticmethod
    def restore_all_gave_dp():
        for user in User.select():
            user.is_gave_dp = False
            user.save()


    @staticmethod
    def get_all_users_dp_point():
        users = []
        for user in User.select().limit(10).order_by(User.dp_point.desc()):
            users.append({'user_id': user.discord_id, 'dp_point': user.dp_point})

        return users