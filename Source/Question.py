class Question:
    question_id = None
    question_text = None
    question_type = None
    answers = None
    constraints = []
    modify_constraints = []
    responses = []

    def __init__(self, question_id, question_text, question_type):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type

    def set_answers(self, answers):
        self.answers = list(answers)

    def set_constraints(self, constraints):
        self.constraints = constraints

    def add_constraint(self, constraint):
        self.constraints += [constraint]

    def add_modify_constraint(self, modify_constraint):
        self.modify_constraints += [modify_constraint]

    def set_modify_constraints(self, modify_constraints):
        self.modify_constraints = modify_constraints

    def has_constraints(self):
        return len(self.constraints)

    def has_modify_constraints(self):
        return len(self.modify_constraints)

    def add_response(self, response):
        self.responses.append(response)

    def get_response_ids(self):
        response_ids = []
        for resp in self.responses:
            response_ids.append(resp.response_id)
        return response_ids

    def get_response_values(self):
        response_values = []

        for resp in self.responses:
            response_values += resp.response_value
        return response_values
