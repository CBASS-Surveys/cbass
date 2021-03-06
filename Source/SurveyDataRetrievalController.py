#!/bin/python
# coding: utf-8
from Database import Database
import json
import yaml
from Question import Question
from Response import Response

class SurveyDataRetrievalController:
    _database = None
    survey_id = None
    
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

    def get_survey(self):
        return self._database.getSurveyName(self.survey_id)
        
    def get_questions(self):
        survey_questions = []
        cursor = self._database.getSurveyQuestions(self.survey_id)

        question_ids = cursor.fetchall()
        cursor.close()
        for (qId,) in question_ids:
            data = self._database.getQuestion(qId)
            question = Question(qId, data[0], data[1])
            self.get_answers_for_question(question)
            survey_questions.insert(qId,question)
        return survey_questions
    
    def get_answers_for_question(self, question):
        cursor = self._database.getResponses(question.question_id)
        answers = []
        for resp in cursor.fetchall():    # want to change 'resp' to 'answ'?
            answers += [Response(resp[0], resp[1], resp[2])] # do i want 'Response'?
        cursor.close()
        question.set_answers(answers)
    
    #survey responses is now on _database

    def get_response_to_questions(self, response_id):
        responses = []
        survey_questions = self.get_questions(self.survey_id)
        for question in survey_questions:    #is this the correct way to retrieve question_id?
            resp = self._database.getIndividualResponseToQuestion(question.question_id, response_id)
            responses += [resp]
        return responses
        
    def get_list_of_survey_responses(self):
        survey_answers = []    #a list of lists - each list contains all of each respondent's answers to the survey questions
        cursor = self._database.getResponsesToSurvey(self.survey_id)
        for resp_id in cursor.fetchall():
            answers = self.get_responses_to_questions(resp_id)
            survey_answers += [answers]
        cursor.close()
        return survey_answers
    
    def export_json(self):
        responses_to_survey = self._database.getResponsesToSurvey(self.survey_id)
        survey_questions = self.get_questions()
        json_responses = []
        for resp in responses_to_survey:
            response = {}
            for quest in survey_questions:
                response[quest.question_id] = self._database.getIndividualResponseToQuestion(quest.question_id, resp)
            json_responses += [
                {"response_id": resp, "response": response}]
        json_full = {"survey_id": self.survey_id, "responses": json_responses, 'survey_description': self._database.surveyToDict(self.survey_id)}
        return json_full
        
    
    def export_csv(self):
        responses_to_survey = self.getResponsesToSurvey(self.survey_id) 
        survey_questions = self.get_questions(self.survey_id)
        #next: csv format output for all responses
    
    def export_excel(self):
        responses_to_survey = self.getResponsesToSurvey(self.survey_id) 
        survey_questions = self.get_questions(self.survey_id)
        #next: excel format output for all responses
        #use xlwt package for this?

    def export_sql(self):
        responses_to_survey = self.getResponsesToSurvey(self.survey_id) 
        survey_questions = self.get_questions(self.survey_id)
        #next: sql format output for all responses
