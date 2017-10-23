#!/bin/python
# coding: utf-8

from flask import Flask, request, jsonify
from flask import render_template
from werkzeug.contrib.cache import SimpleCache
import logging
from SurveyTakingController import SurveyTakingController
import uuid
from SurveyProperties import SurveyProperties


class Router:
    survey_taking_controller = None

    # Future Controllers here

    def __init__(self):
        print("Starting Router...")

    def create_survey_taking_controller(self, survey_id):
        self.survey_taking_controller = SurveyTakingController(survey_id)


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
app = Flask("CBASS")
cache = SimpleCache()
router = Router()
sessionId = uuid.uuid4()


@app.route("/")
def main_page():
    properties = SurveyProperties()
    # Change this to get user's surveys later on
    survey_name = properties.get_survey_name(1)
    return render_template("test.html", name=survey_name)


@app.route("/<surveyId>")
def start_survey():
    survey_id = request.form["surveyId"]

    if survey_id:
        router.create_survey_taking_controller(survey_id)
    else:
        print("Error")

    first_question = router.survey_taking_controller.start_survey(sessionId)
    return jsonify({'question': first_question})


@app.route("/<questionNumber>")
def get_question(question_num=None):
    if question_num:
        router.survey_taking_controller.get_question(question_num)
    else:
        # Get the next next question
        router.survey_taking_controller.get_next_question()


@app.route("/submitQuestionResponse")
def submit_question():
    response = request.form["question-response"]
    if response:
        router.survey_taking_controller.send_response(response)
    else:
        print("Error: response given")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
