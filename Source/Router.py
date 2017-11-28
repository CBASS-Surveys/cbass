#!/bin/python
# coding: utf-8

import json
import logging
import os

from flask import Flask, request, jsonify, redirect, send_from_directory
from flask import render_template, url_for
from werkzeug.contrib.cache import SimpleCache

import Config
# from Errors import NoResponse, MalformedSurvey
from MalformedSurvey import MalformedSurvey
from NoResponse import NoResponse
from SurveyCreationController import SurveyCreationController
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
    survey_creation_controller = None

    # Future Controllers here

    def __init__(self, *args):
        print("Starting Router...")

    def create_survey_taking_controller(self, survey_id):
        self.survey_taking_controller = SurveyTakingController(survey_id)

    def create_survey_creation_controller(self):
        self.survey_creation_controller = SurveyCreationController()


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# template_dir = os.path.abspath('public')
template_dir = os.path.dirname(__file__) + "/public"
app = CustomFlask("CBASS", template_folder=template_dir, static_folder='static')
cache = SimpleCache()
router = Router()


@app.route("/")
def main_page():
    survey_id = 2

    return redirect(url_for('start_survey', survey_id=survey_id))


@app.route("/create_survey", methods=['GET'])
def create_survey():
    return render_template('surveyCreator.html')


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


@app.route("/get_properties")
def get_properties():
    # survey_id = json.loads(request.data)
    survey_id = 2
    survey_properties = SurveyProperties(survey_id)
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


@app.errorhandler(MalformedSurvey)
def handled_malformed_survey(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/testing")
def testing():
    print ("Not much testing going on here")
    # you can put stuff here for quick tests


@app.route("/create-question", methods=['POST'])
def create_question(data=None):
    # this function handles an iterate method for adding questions or a single create_question from the view
    if data:
        router.survey_creation_controller.create_survey_question(data[0], data[1])
    else:
        q_data = json.loads(request.data)
        router.survey_creation_controller.create_survey_question(q_data[0], q_data[1])


# TODO: remove GET before production
@app.route("/save_survey", methods=['POST', 'GET'])
def save():
    global resp_discluded
    if request.method == 'POST':
        data = json.loads(request.data)
    else:
        json_data = open("surveyCreatorTestData.json").read()
        data = json.loads(json_data)

    if router.survey_creation_controller is None:
        router.create_survey_creation_controller()

    try:
        keys = data.keys()
        survey_name = data["survey_title"]
        author = "Author"

        if 'survey_properties' in keys:
            survey_properties = data["survey_properties"]
        else:
            survey_properties = None
        router.survey_creation_controller.create_survey(survey_name, author, survey_properties)
        for question in data['questions']:
            q_keys = question.keys()
            question_type = str(question['type'])
            question_id = router.survey_creation_controller.create_survey_question(str(question['text']), question_type)
            if not question_type == 'free-response':
                if 'answers' in q_keys:
                    answers = question['answers']
                    router.survey_creation_controller.create_multiple_answers(question_id, answers)
                if 'constraints' in q_keys:
                    for const in question['constraints']:
                        const_type = str(const['type'])
                        if const_type == 'modify':
                            question_from = const['question_from']
                            response_from = const['response_from']
                            question_to = const['question_to']
                            resp_discluded = const['responses_discluded']
                            router.survey_creation_controller.create_question_constraint_standard(question_from,
                                                                                                  response_from,
                                                                                                  const_type,
                                                                                                  question_to)
                        elif const_type == 'forbids':
                            question_from = const['question_from']
                            response_from = const['response_from']
                            question_to = const['question_to']
                            router.survey_creation_controller.create_disclusion_constraint(question_from, response_from,
                                                                                           question_to, resp_discluded)
    except KeyError:
        raise MalformedSurvey


# @app.route('/static/js/<path:path>')
# def send_static_js(path):
#     return send_from_directory('static/js', path)

# @app.route('/static/css/<path:path>')
# def send_static_css(path):
#     return send_from_directory('static/css', path)

# @app.route('/static/libs/<path:path>')
# def send_static_libs(path):
#     return send_from_directory('static/libs', path)

# @app.route('/static/media/<path:path>')
# def send_static_media(path):
#     return send_from_directory('static/media', path)
    
# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)
    
if __name__ == "__main__":
    app.config.from_object(Config.DevelopmentConfig)
    app.run(host='127.0.0.1', port=8000)
