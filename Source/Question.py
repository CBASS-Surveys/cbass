class Question:
    question_id = None
    question_text = None
    question_type = None
    answers = None
    constraints = None
    modify_constraints = None
    response = []

    def __init__(self, question_id, question_text, question_type):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type

    def set_answers(self, answers):
        self.answers = list(answers)

    def set_constraints(self, constraints):
        self.constraints = constraints

    def set_modify_constraints(self, modify_constraints):
        self.modify_constraints = modify_constraints

    def has_constraints(self):
        return len(self.constraints)

    def has_modify_constraints(self):
        return len(self.modify_constraints)

    def add_response(self, response):
        self.response += [response]