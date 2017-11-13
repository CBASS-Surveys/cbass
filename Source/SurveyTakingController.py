#!/bin/python
# coding: utf-8
from Database import Database
import yaml
from Response import Response
from Constraints import Constraint, ModifyConstraint
from Question import Question
from Utils import deprecated
import json


class SurveyTakingController:
    _database = None
    response_id = None
    survey_id = None
    survey_questions = []
    question_number = -1
    current_question = None

    def __init__(self, survey_id):

        self.survey_id = survey_id
        self.survey_questions = []

        with open("config-test.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        # dump(hostname, username, password)
        self._database = Database(db, hostname, username, password)

    def start_survey(self, session_id):
        response_struct = self._database.createSurveyResponse(self.survey_id, str(session_id))
        self.response_id = response_struct[0]
        self.get_survey_questions()

    @deprecated
    def send_response(self, response):
        question_type = self.survey_questions[self.question_number].question_type
        question = self.current_question
        question_id = question.question_id
        if question_type == "free-response":
            if response:
                self._database.insertSurveyQuestionLongFormResponse(self.response_id, question_id, response)
        else:
            response_ids = []
            for resp in response:
                for answer in question.answers:
                    if resp == answer.response_description:
                        response_ids += [answer.response_id]
                question.add_response(resp)

            if len(response_ids):
                if question_type == "single-response":
                    if response:
                        self._database.insertSurveyQuestionResponse(self.response_id, question_id, response_ids[0])
                elif question_type == "multi-choice-response":
                    if response:
                        self._database.insertSurveyQuestionMultiResponse(self.response_id, question_id, response_ids)
    
    def send_response_v2(self, response):
        question_type = self.survey_questions[self.question_number].question_type
        question = self.current_question
        question_id = question.question_id
        answers = json.loads(response)
        if isinstance(answers, int):
                self._database.insertSurveyQuestionResponse(self.response_id, question_id, answers)
        elif isinstance(answers, list):
                    # "multi-response send all items selected
                    self._database.insertSurveyQuestionMultiResponse(self.response_id, question_id, answers)
        elif isinstance(answers, unicode) or isinstance(answers, str):
            # send the text
            self._database.insertSurveyQuestionLongFormResponse(self.response_id, question_id, str(answers))
        else:
            raise Exception

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
            self.survey_questions.insert(qId, question)

        self.current_question = self.survey_questions[0]

    def get_next_question(self):
        self.question_number += 1
        if self.question_number >= len(self.survey_questions):
            return Question(0, "end of survey", "end")
        question = self.current_question

        if question.has_constraints():
            for constraint in question.constraints:
                question_from = constraint.question_from
                if self._database.hasResponse(question_from, constraint.response_from, self.response_id):
                    if constraint.type == 'forbid':
                        return self.get_next_question()
        if question.has_modify_constraints():
            responses = {}
            for response in question.answers:
                responses[response.response_id] = response
            for constraint in question.modify_constraints:
                question_from = constraint.question_from
                if self._database.hasResponse(question_from, constraint.response_from, self.response_id):
                    for remove in constraint.response_discluded:
                        if remove in responses:
                            del responses[remove]
            question.answers = responses.values()
        self.current_question = question
        return question

    def get_prev_question(self):
        if self.question_number == 0:
            return None
        else:
            self.question_number += -1
            question = self.survey_questions[self.question_number]
            self.current_question = question
            return question

    def get_question(self, q):
        self.question_number = q
        question = self.survey_questions[self.question_number]
        self.current_question = question
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

        cursor_mod = self._database.getModifyConstraints(question.question_id)
        for (qFrom, rFrom, discluded) in cursor_mod:
            modify_constraints += [ModifyConstraint(qFrom, rFrom, discluded)]
        cursor.close()
        cursor_mod.close()
        question.set_constraints(constraints)
        question.set_modify_constraints(modify_constraints)
