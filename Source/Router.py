#!/bin/python
# coding: utf-8

import os
from flask import Flask, request, jsonify, redirect
from flask import render_template, url_for
from werkzeug.contrib.cache import SimpleCache
import logging
from SurveyTakingController import SurveyTakingController, Question
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
template_dir = os.path.abspath('public')
app = Flask("CBASS", template_folder=template_dir)
cache = SimpleCache()
router = Router()
sessionId = uuid.uuid4()
survey_id = None


@app.route("/")
def main_page():
    properties = SurveyProperties()
    # Change this to get user's surveys later on
    survey_name = properties.get_survey_name(1)
    survey_id = 1
    return redirect(url_for('start_survey', survey_id=survey_id))


@app.route("/<survey_id>")
def start_survey(survey_id):
    # survey_id = request.form["surveyId"]
    print(survey_id)
    if survey_id:
        router.create_survey_taking_controller(survey_id)
    else:
        print("Error")

    router.survey_taking_controller.start_survey(sessionId)
    return render_template("vueQuestions/index.html")


@app.route("/survey_id=<survey_id>/question_num=<question_num>", methods=['GET', 'POST'])
def get_question(question_num):
    question = None
    answers = None

    question = router.survey_taking_controller.get_question(question_num)
    answers = router.survey_taking_controller.get_answers(question)


    return jsonify(text=question.question_text,
               type=question.question_type,
               answers=answers)


@app.route("/survey_id=<survey_id>/get_next_question")
def get_next_question():
    question = None
    answers = None
    question = router.survey_taking_controller.get_next_question()
    answers = router.survey_taking_controller.get_answers(question)


    return jsonify(text=question.question_text,
               type=question.question_type,
               answers=answers)

@app.route("/survey_id=<survey_id>/get_prev_question")
def get_prev_question():
    question = None
    answers = None
    question = router.survey_taking_controller.get_prev_question()
    answers = router.survey_taking_controller.get_answers(question)


    return jsonify(text=question.question_text,
               type=question.question_type,
               answers=answers)

@app.route("/submit-question-response")
def submit_question():
    response = request.form["question-response"]
    if response:
        router.survey_taking_controller.send_response(response)
    else:
        print("Error: response given")
    redirect(url_for('get_question', survey_id=survey_id))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
