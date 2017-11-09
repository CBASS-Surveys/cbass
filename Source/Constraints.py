class Constraint:
    question_from = None
    response_from = None
    type = None

    def __init__(self, question_from, response_from, constraint_type):
        self.question_from = question_from
        self.response_from = response_from
        self.type = constraint_type


class ModifyConstraint:
    question_from = None
    response_from = None
    response_discluded = None

    def __init__(self, question_from, response_from, response_discluded):
        self.question_from = question_from
        self.response_from = response_from
        self.response_discluded = response_discluded
