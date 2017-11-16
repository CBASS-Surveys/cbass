#!/bin/python
# coding: utf-8

import logging
import os
import json

from flask import Flask, request, jsonify, redirect
from flask import render_template, url_for
from werkzeug.contrib.cache import SimpleCache

import Config
from Errors import NoResponse
from SurveyProperties import SurveyProperties
from SurveyTakingController import SurveyTakingController



# Avoid jinja and vue conflict
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))


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
app = CustomFlask("CBASS", template_folder=template_dir)
cache = SimpleCache()
router = Router()


@app.route("/")
def main_page():
    survey_id = 2
    
    return redirect(url_for('start_survey', survey_id=survey_id))


@app.route("/survey_id=<survey_id>")
def start_survey(survey_id):
    # 
    print("survey_id = " + survey_id)
    if survey_id:
        router.create_survey_taking_controller(survey_id)
    else:
        print("Error")

    router.survey_taking_controller.start_survey()
    return render_template("vueQuestions/index.html")

@app.route("/get_properties=<survey_id>")
def get_properties(survey_id):
    survey_id = json.loads(request.data)
    survey_properties = SurveyProperties(2)
    properties = survey_properties.get_survey_properties()
    # Change this to get user's surveys later on
    survey_name = survey_properties.get_survey_name()
    return jsonify(name=survey_name,
                   properties=properties)

@app.route("/question_num=<question_num>", methods=['GET', 'POST'])
def get_question(question_num):
    question = router.survey_taking_controller.get_question(question_num)
    answers = []
    for resp in question.answers:
        answers += [{"response_id": resp.response_id, "response_value": resp.response_description}]

    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


@app.route("/get_next_question", methods=['GET', 'POST'])
def get_next_question():
    if request.method == 'POST':
        submit_response(request.data)

    question = router.survey_taking_controller.get_next_question()

    if question.question_type == "end":
        return jsonify(text=question.question_text,
                       type=question.question_type)

    answers = []
    for resp in question.answers:
        answers += [{"response_id": resp.response_id, "response_value": resp.response_description}]

    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


@app.route("/get_prev_question", methods=['GET', 'POST'])
def get_prev_question():
    # Future Implementation
    # if request.method == 'POST':
    #    submit_response(request.data)

    question = router.survey_taking_controller.get_prev_question()
    answers = []
    for resp in question.answers:
        answers += [{"response_id": resp.response_id, "response_value": resp.response_description}]

    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


def submit_response(response):
    try:
        router.survey_taking_controller.send_response_v2(response)
    except Exception:
        raise NoResponse('No response to submit', status_code=410)


@app.errorhandler(NoResponse)
def handle_no_response(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/testing")
def testing():
    print ("Not much testing going on here")
    # you can put stuff here for quick tests


if __name__ == "__main__":
    app.config.from_object(Config.DevelopmentConfig)
    app.run(host='127.0.0.1', port=8000)
