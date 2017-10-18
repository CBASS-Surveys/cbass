#!/bin/python
# coding: utf-8
import Database


class SuveyTakingController:

    _view = None
    _database = None
    _qCounter = 0

    def __init__(self, view, database):
        self._view = view
        self._database = database
        # view.getUser, view.getPassword
        if not database.authenticateUser():
            database.authenticateUser()

    def sendResponse(self):
        responseId = self._view.getResponseId()
        questionId = self._view.getQuestionId()
        response = self._view.getResponse()

        if response:
            self._database.createResponse(responseId,questionId,response)

    def getNextQuestion(self):
        self._qCounter += 1
        surveyId = self._view.getSurveyId()
        self._database.getNextQuestion(surveyId, self._qCounter)


