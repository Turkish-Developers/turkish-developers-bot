class QuestionSerializer:
    def __init__(self, args):
        self.args = args
        self._validated_data = ''
        self.validated = False


    @property
    def validated_data(self):
        return self._validated_data


    def validate(self):
        status, question, choices, answer, code = ('', '', '', '', '')

        data = self.args.split('$')

        if len(data) not in [3,4]:
            return False

        question = data[0].strip()
        choices = data[1].strip().replace('\n', '').replace('(', '').replace(')', '').split(',')
        if len(choices) != 4:
            return False

        answer = data[2]

        if answer.lower() not in ['a', 'b', 'c', 'd']:
            return False

        if(len(data) == 4):
            code = data[3]

        self.validated = True
        return True


    def is_valid(self):
        return self.validate()

    @validated_data.getter
    def validated_data(self):
        import re
        regex = r',(?![^(]*\)) '

        question, choices, answer, code = ('', '', '', '')

        data = self.args.split('$')

        question = data[0].strip()
        choices = data[1].strip().replace('\n', '').replace('(', '').replace(')', '').split(',')

        answer = data[2]

        if(len(data) == 4):
            code = data[3]

        return {'question': question, 'choices': choices, 'answer': answer, 'code': code}
