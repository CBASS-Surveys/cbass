#!/bin/python
# coding: utf-8
from Database import Database
import yaml


class SurveyTakingController:
    _database = None
    responseId = None
    survey_id = None
    survey_questions = []
    question_number = -1
    current_question = None

    def __init__(self, survey_id):

        self.survey_id = survey_id

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        #dump(hostname, username, password)
        self._database = Database(db, hostname, username, password)

    def start_survey(self, session_id):
        response_struct = self._database.createSurveyResponse(self.survey_id, str(session_id))
        self.responseId = response_struct[0]
        self.get_survey_questions()

    def send_response(self, response):
        form = self.survey_questions[self.question_number].question_type
        question = self.current_question
        question_id = question.question_id
        if form == "free-response":
            if response:
                self._database.insertSurveyQuestionLongFormResponse(self.responseId, question_id, response)
        else:
            response_ids = []
            for resp in response:
                for answer in question.answers:
                    if resp == answer.response_description:
                        response_ids += [answer.response_id]
                question.add_response(resp)


            if len(response_ids):
                if form == "single-response":
                    if response:
                        self._database.insertSurveyQuestionResponse(self.responseId, question_id, response_ids[0])
                elif form == "multi-choice-response":
                    if response:
                        self._database.insertSurveyQuestionMultiResponse(self.responseId, question_id, response_ids)



    def get_survey_questions(self):
        survey_id = self.survey_id
        cursor = self._database.getSurveyQuestions(survey_id)
        question_ids = cursor.fetchall()
        cursor.close()

        for (qId,) in question_ids:
            data = self._database.getQuestion(qId)
            question = Question(qId, data[0], data[1])
            self.get_answers_for_question(question)
            self.get_constraints_for_question(question)
            self.survey_questions.insert(qId,question)

    def get_next_question(self):
        self.question_number += 1
        if(self.question_number >= len(self.survey_questions)):
            return Question(0,"end of survey", "end")
        question = self.survey_questions[self.question_number]

        if question.has_constraints():
            for constraint in question.constraints:
                question_from = constraint.question_from
                if self._database.hasResponse(question_from, constraint.response_from, self.responseId):
                    if constraint.type == 'forbid':
                        return self.get_next_question()
        if question.has_modify_constraints():
            responses = {}
            for response in question.answers:
                responses[response.response_id] = response
            for constraint in question.modify_constraints:
                question_from = constraint.question_from
                if self._database.hasResponse(question_from, constraint.response_from, self.responseId):
                    for remove in constraint.response_discluded:
                        if remove in responses:
                            del responses[remove]
            question.answers = responses.values()
        self.current_question = question
        return question

    def get_prev_question(self):
        question_num = self.question_number - 1
        question = self.survey_questions[question_num]
        return question

    def get_question(self, q):
        self.question_number = q
        # Check for bounds later
        question = self.survey_questions[self.question_number]
        return question

    def get_answers_for_question(self, question):
        cursor = self._database.getResponses(question.question_id)
        responses = []
        for resp in cursor.fetchall():
            responses += [Response(resp[0], resp[1], resp[2])]
        cursor.close()
        question.set_answers(responses)

    def get_constraints_for_question(self, question):

        constraints = []
        modify_constraints = []
        cursor = self._database.getConstraints(question.question_id)
        for con in cursor:
            constraints += [Constraint(con[0], con[1], con[2])]

        cursorMod = self._database.getModifyConstraints(question.question_id)
        for (qFrom, rFrom, discluded) in cursorMod:
            modify_constraints += [ModifyConstraint(qFrom, rFrom, discluded)]
        cursor.close()
        cursorMod.close()
        question.set_constraints(constraints)
        question.set_modify_constraints(modify_constraints)


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

class Response:
    response_id = None
    response_value = None
    response_description = None

    def __init__(self, response_id, response_value, response_description):
        self.response_id = response_id
        self.response_value = response_value
        self.response_description = response_description


class Constraint:
    question_from = None
    response_from = None
    type = None

    def __init__(self, question_from, response_from, type):
        self.question_from = question_from
        self.response_from = response_from
        self.type = type


class ModifyConstraint:
    question_from = None
    response_from = None
    response_discluded = None

    def __init__(self, question_from, response_from, response_discluded):
        self.question_from = question_from
        self.response_from = response_from
        self.response_discluded = response_discluded
