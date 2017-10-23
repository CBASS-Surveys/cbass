#!/bin/python
# coding: utf-8

import time
from flask import Flask, request
from flask import render_template
from werkzeug.contrib.cache import SimpleCache
import logging
import SurveyTakingController
import uuid
import SurveyProperties

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
app = Flask("CBASS")
cache = SimpleCache()
router = Router()
sessionId = None

@app.route("/")
def main_page():
    sessionId = uuid.uuid4()
    properties = SurveyProperties()
    #Change this to get user's surveys later on
    survey_name = properties.getSurveyName(1)
    return render_template("index.html" , name = survey_name)

@app.route("/<surveyId>")
def startSurvey(surveyId)
    surveyId = request.form["surveyId"]
    
    if surveyId:
        router.createSurveyTakingController(surveyId)
    else:
        print("Error")
    
    firstQ = router.surveyTakingController.startSurvey(sessionId)
    return jsonify({'question' : firstQ})
    
@app.route("/<questionNumber>")
def getQuestion(questionNumber = None)
    if questionNumber:
        router.surveyTakingController.getQuestion(questionNumber)
    else:
        #Get the next next question
        router.surveyTakingController.getNextQuestion()
        
@app.route("/submitQuestionResponse")
def submitQuestion() 
    response =request.form["question-response"]
    if response:
        router.surveyTakingController.sendResponse(response)
    else:
        print("Error: response given")
    
class Router:
    surveyTakingController = None
    #Future Controllers here
    
    def __init__(self):
        print("Starting Router...")
        
    def createSurveyTakingController(surveyId)
        surveyTakingController = SurveyTakingController(surveyId)
    
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)

