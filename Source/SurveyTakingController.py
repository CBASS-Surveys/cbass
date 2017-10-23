#!/bin/python
# coding: utf-8
from Database import Database
import yaml


class SurveyTakingController:
    _database = None
    responseId = None
    surveyId = None
    surveyQuestions = ()
    questionNumber = 0

    def __init__(self, surveyId):
        
        self.surveyId = surveyId

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        self._database = Database(db, hostname, username, password)
        
    def startSurvey(self, sessionId):
    	    responseStruct = self._database.createSurveyResponse(self.surveyId, sessionId)
    	    self.responseId = responseStruct[0]
    	    self.getSurveyQuestions()
    	    # Return first question to the view
    	    question = self.getQuestion(questionNumber)
    	    return question 
    	    

    def sendResponse(self, response):
        form = self.surveyQuestions(questionNumber).question_type
        questionId = self.surveyQuestions(questionNumber).question_id
        
        if form == "single-response":
            if response:
                self._database.insertSurveyQuestionResponse(self.responseId, questionId, response)
        elif form == "multi-choice-response":
            if response:
                self._database.insertSurveyQuestionMultiResponse(self.responseId, questionId, response)
        elif form == "free-response":
            if response:
                self._database.insertSurveyQuestionLongFormResponse(self.responseId, questionId, response)

    def getSurveyQuestions(self):
        surveyId = self.surveyId
        cursor = self._database.getSurveyQuestions(surveyId)
        questionIds = cursor.fetchall()
        cursor.close()
        
        for qId in questionIds:
            data = self._database.getQuestion(qId)
            question = Question(qId, data[0], data[1])
            self.surveyQuestions += question 
        
        
    def getNextQuestion(self)
    	questionNumber += 1
    	question = surveyQuestions[questionNumber]
    	return question
    	
    def getQuestion(q)
    	self.questionNumber = q
    	#Check for bounds later
    	question = self.surveyQuestions[questionNumber]
    	return question

class Question:
    question_id = None
    question_text = None
    question_type = None
    
    def __init__(self, question_id, question_text, question_type)
        
