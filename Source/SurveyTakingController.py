#!/bin/python
# coding: utf-8
from Database import Database
import yaml


class SurveyTakingController:
    _database = None
    responseId = None
    survey_id = None
    survey_questions = ()
    question_number = 0

    def __init__(self, survey_id):

        self.survey_id = survey_id

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        self._database = Database(db, hostname, username, password)

    def start_survey(self, session_id):
        response_struct = self._database.createSurveyResponse(self.survey_id, str(session_id))
        self.responseId = response_struct[0]
        self.get_survey_questions()


    def send_response(self, response):
        form = self.survey_questions[self.question_number].question_type
        question_id = self.survey_questions[self.question_number].question_id

        if form == "single-response":
            if response:
                self._database.insertSurveyQuestionResponse(self.responseId, question_id, response)
        elif form == "multi-choice-response":
            if response:
                self._database.insertSurveyQuestionMultiResponse(self.responseId, question_id, response)
        elif form == "free-response":
            if response:
                self._database.insertSurveyQuestionLongFormResponse(self.responseId, question_id, response)

    def get_survey_questions(self):
        survey_id = self.survey_id
        cursor = self._database.getSurveyQuestions(survey_id)
        question_ids = cursor.fetchall()
        cursor.close()

        for qId in question_ids[1:]:
            data = self._database.getQuestion(qId)
            question = Question(qId, data[0], data[1])
            self.survey_questions += (question,)
        end_question = Question(question_ids[0],"End Survey", "single-response")
        self.survey_questions += (end_question,)

    def get_next_question(self):
        self.question_number += 1
        question = self.survey_questions[self.question_number]
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

    def get_answers(self, question):
        cursor = self._database.getResponses(question.question_id)
        responses = []
        for resp in cursor.fetchall():
            responses += Response(resp[0],resp[1])
        cursor.close()
        return responses

    def get_constraints(self, question):
        cursor = self._database.getConstraints(question)
        cursor.fetchall()


class Question:
    question_id = None
    question_text = None
    question_type = None

    def __init__(self, question_id, question_text, question_type):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type


class Response:
    response_value = None
    response_description = None

    def __init__(self, response_value, response_description):
        self.response_value = response_value
        self.response_description = response_description

