#!/bin/python
# coding: utf-8
from Database import Database
import yaml


class SurveyTakingController:
    _view = None
    _database = None

    def __init__(self):

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        self._database = Database(db, hostname, username, password)

    def sendResponse(self):
        form = self._view.getQuestionForm
        responseId = self._view.getResponseId()
        questionId = self._view.getQuestionId()
        response = self._view.getResponse()
        if form == "single-response":
            if response:
                self._database.createSingleResponse(responseId, questionId, response)
        elif form == "multi-choice-response":
            if response:
                self._database.createMultiResponse(responseId, questionId, response)
        elif form == "free-response":
            if response:
                self._database.createLongResponse(responseId, questionId, response)

    def getNextQuestion(self):
        current = self._view.getCurrentQuestion()
        surveyId = self._view.getSurveyId()
        self._database.getNextQuestion(surveyId, current)


if __name__ == "__main__":
    view = None
    database = None
    controller = SurveyTakingController()
