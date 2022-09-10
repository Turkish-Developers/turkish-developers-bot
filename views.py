from models import *
from serializers import QuestionSerializer
db.connect()
db.create_tables([User])
db.create_tables([Question])
db.create_tables([DPLogger])

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
            self.create_dp_log(other_user)
            self.user.is_gave_dp = True
            self.user.save()
            return True, UserView(other_user_discord_id)
        else:
            return False, ''

    def create_dp_log(self, user):
        DPLogger.create(user=user)


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


class QuestionView:
    def __init__(self) -> None:
        self.serializer_class = QuestionSerializer


    @staticmethod
    def get_random_question():
        import random
        question = random.choice(Question.select().where(Question.is_published == False))
        if question:
            question.is_published = True
            question.save()
            return question.question, question.id
        
        return False,False

    @staticmethod
    def check_question_answer(id, answer, user_id):
        question = Question.select().where(Question.id == id).get()
        if question.answered:
            return 'Soru cevaplanmış!'
        
        if str(user_id) in question.answered_by:
            return 'Daha önce seçim yaptın ve bilemedin.'

        if question.answer.lower() == answer.lower():
            question.answered = True
            question.answered_by += str(user_id) + ','
            question.save()
            User = UserView(user_id)
            User.user.dp_point += 1
            User.user.save()
            return 'exit'

        question.answered_by += str(user_id) + ','
        question.save()

        return 'Cevabın maalesef yanlış :('
            

    def save(self, args):
        serializer = self.serializer_class(args)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            question_string = ''
            question_string += validated_data.get('question') + '\n'

            if validated_data['code']:
                question_string += '<code>' + validated_data['code'] + '<code>' + '\n\n'


            choices = ['A','B','C','D']
            counter = 0
            for choice in validated_data.get('choices'):
                question_string += f'{choices[counter]}){choice} \n'
                counter += 1

            answer = validated_data['answer']

            Question.create(question=question_string, answer=answer)
            return True

        else:
            return False
            

class DPLoggerView:
    def __init__(self) -> None:
        self.monthly_leaderboard = self._get_month_user_dp_leaderboard()

    def _get_month_user_dp_leaderboard(self, mounth=0):
        import datetime
        now_month = datetime.datetime.now().month
        if not mounth:
            mounth = now_month
        
        users = []


        queryset = DPLogger.select(DPLogger.user, fn.Count(DPLogger.user).alias('count')).where(DPLogger.created_date.month == mounth).group_by(DPLogger.user).limit(10).order_by(fn.COUNT(DPLogger.user).desc())

        for log in queryset:
            users.append({'user_id': log.user.discord_id, 'dp_point': log.count})

        return users

    def get_mounthly_winners(self):
        import datetime
        now_month = datetime.datetime.now().month
        return self._get_month_user_dp_leaderboard(mounth=9)[:2]

