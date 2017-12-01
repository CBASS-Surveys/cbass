#!/bin/python
# coding: utf-8

import json
import logging
import os

from flask import Flask, request, jsonify, redirect
from flask import render_template, url_for, session
from werkzeug.contrib.cache import SimpleCache

import uuid
import Config
# from Errors import NoResponse, MalformedSurvey
from MalformedSurvey import MalformedSurvey
from NoResponse import NoResponse
from SurveyCreationController import SurveyCreationController
from SurveyProperties import SurveyProperties
from SurveyTakingController import SurveyTakingController
from SurveyTakingEncoder import CustomEncoder, from_json


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
app = CustomFlask("CBASS", template_folder=template_dir)
cache = SimpleCache()

app.secret_key = '7\xe81\x8a\x84\xd5\xc8\xf1vw\xde\x97\xaa\x8a\xf3"A\x14.\x0e~l\xa5\xd4+\x9b\x06Sf\x81\xdcJ'


@app.route("/")
def main_page():
    survey_id = 2
    session['survey_id'] = survey_id
    return redirect(url_for('start_survey', survey_id=survey_id))


@app.route("/create_survey", methods=['GET'])
def create_survey():
    return render_template('surveyCreator.html')


@app.route("/survey/<survey_id>")
def start_survey(survey_id):
    session['survey_id'] = survey_id
    survey = None
    print("survey_id = " + survey_id)
    if survey_id:
        survey = SurveyTakingController(survey_id)
    else:
        print("Error")
    session['session_id'] = uuid.uuid4()
    survey.start_survey(session['session_id'])
    session['survey'] = json.dumps(survey, cls=CustomEncoder)
    return render_template("vueQuestions/index.html")


@app.route("/get_properties")
def get_properties():
    survey_id = session['survey_id']
    survey_properties = SurveyProperties()
    properties = survey_properties.get_survey_properties(survey_id)
    # Change this to get user's surveys later on
    survey_name = survey_properties.get_survey_name(survey_id)
    return jsonify(name=survey_name,
                   properties=properties)


@app.route("/question_num=<question_num>", methods=['GET', 'POST'])
def get_question(question_num):
    survey = from_json(session['survey'])
    question = survey.get_question(question_num)
    session['survey'] = json.dumps(survey, cls=CustomEncoder)
    answers = []
    for resp in question.answers:
        answers += [{"response_id": resp.response_id, "response_value": resp.response_description}]

    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


@app.route("/get_next_question", methods=['GET', 'POST'])
def get_next_question():
    survey = from_json(session['survey'])
    if request.method == 'POST':
        submit_response(request.data)

    question = survey.get_next_question()

    if question.question_type == "end":
        return jsonify(text=question.question_text,
                       type=question.question_type)
    answers = []
    if question.answers:
        for resp in question.answers:
            answers += [{"response_id": resp.response_id, "response_value": resp.response_value}]

    session['survey'] = json.dumps(survey, cls=CustomEncoder)
    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


@app.route("/get_prev_question", methods=['GET', 'POST'])
def get_prev_question():
    # Future Implementation
    # if request.method == 'POST':
    #    submit_response(request.data)
    survey = from_json(session['survey'])
    question = session['survey'].get_prev_question()
    answers = []
    for resp in question.answers:
        answers += [{"response_id": resp.response_id, "response_value": resp.response_description}]

    session['survey'] = json.dumps(survey, cls=CustomEncoder)
    return jsonify(text=question.question_text,
                   type=question.question_type,
                   answers=answers)


def submit_response(response):
    try:
        survey = from_json(session['survey'])
        survey.send_response_v2(response)
        session['survey'] = json.dumps(survey, cls=CustomEncoder)
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
        session['router'].survey_creation_controller.create_survey_question(data[0], data[1])
    else:
        q_data = json.loads(request.data)
        session['router'].survey_creation_controller.create_survey_question(q_data[0], q_data[1])


# TODO: remove GET before production
@app.route("/save_survey", methods=['POST', 'GET'])
def save():
    if request.method == 'POST':
        data = json.loads(request.data)
    else:
        json_data = open("surveyCreatorTestData.json").read()
        data = json.loads(json_data)

    survey_creator = SurveyCreationController()

    try:
        keys = data.keys()
        survey_name = data["title"]
        author = "Author"

        if 'properties' in keys:
            survey_properties = data["properties"]
        else:
            survey_properties = []
        survey_creator.create_survey(survey_name, author, survey_properties)
        for question in data['questions']:
            q_keys = question.keys()
            question_type = str(question['type'])
            question_id = survey_creator.create_survey_question(str(question['text']), question_type)
            if not question_type == 'free-response':
                if 'answers' in q_keys:
                    answers = question['answers']
                    survey_creator.create_multiple_answers(question_id, answers)
        for const in question['constraints']:
            const_type = str(const['type'])
            if const_type == 'modify':
                question_from = const['question_from']
                response_from = const['response_from']
                question_to = const['question_to']
                survey_creator.create_question_constraint_standard(question_from, response_from, const_type,
                                                                   question_to)
            elif const_type == 'forbids':
                question_from = const['question_from']
                response_from = const['response_from']
                question_to = const['question_to']
                resp_discluded = const['responses_discluded']
                survey_creator.create_disclusion_constraint(question_from, response_from, question_to, resp_discluded)
    except KeyError:
        raise KeyError
        return jsonify(flag=False)
    print (str(survey_creator.survey_id))
    return jsonify(flag=True, survey_id=survey_creator.survey_id)


# TODO: Not working currently
@app.route("/load_survey=<survey_id>", methods=['GET'])
def load(survey_id):
    property_manager = SurveyProperties()
    survey_name = property_manager.get_survey_name(survey_id)
    properties = property_manager.get_survey_properties(survey_id)
    session['survey'] = SurveyTakingController(survey_id)
    session['survey'].get_survey_questions()
    questions = session['survey'].survey_questions
    json_questions = []
    counter = 1
    for question in questions[1:]:
        answers = []
        ids = {}
        i = 0
        if question.answers:
            for resp in question.answers:
                answers += [{"value": resp.response_value, "description": resp.response_description}]
                ids[resp.response_id] = i
                i += 1
        constraints = []
        if question.constraints:
            for const in question.constraints:
                response_from = ids[const.response_from]
                constraints += [
                    {"question_from": const.question_from, "response_from": response_from, "question_to": counter,
                     "type": const.type}]
        if question.modify_constraints:
            for const in question.modify_constraints:
                response_from = ids[const.response_from]
                # TODO load responses discluded
                constraints += [
                    {"question_from": const.question_from, "response_from": response_from, "question_to": counter,
                     "type": "modify", "responses_discluded": const.response_discluded}]
        json_questions += [{"text": question.question_text, "type": question.question_type, "answers": answers,
                            "constraints": constraints}]
        counter += 1
    return jsonify(title=survey_name, questions=json_questions, properties=properties)


@app.route("/publish=<survey_id>", methods=['POST'])
def publish(survey_id):
    property_manager = SurveyProperties()
    property_manager.publish(survey_id)


if __name__ == "__main__":
    app.config.from_object(Config.DevelopmentConfig)
    app.run(host='127.0.0.1', port=8000)
