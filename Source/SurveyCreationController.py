# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:58:28 2017

@author: hpollmann
"""

import yaml

from Constraints import Constraint, ModifyConstraint
from Database import Database
from Question import Question
from Response import Response


class SurveyCreationController:
    _database = None
    question_types = {'single-response', 'multi-choice-response', 'free-response'}
    constraint_standards = {'forbids', 'requires'}

    def __init__(self):

        self.survey_id = None
        self.survey_questions = {}
        self.zero_index = []

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        # dump(hostname, username, password)
        self._database = Database(db, hostname, username, password)

    def create_survey(self, name, author_name, survey_properties=None):
        # TODO: verify survey properties in the kwargs

        (self.survey_id,) = self._database.createSurvey(name, author_name, **survey_properties)

    def create_survey_question(self, text, question_type):
        if text and question_type in self.question_types:
            (question_id,) = self._database.createSurveyQuestion(self.survey_id, text, question_type)
            self.survey_questions[question_id] = Question(question_id, text, question_type)
            self.zero_index.append(Question(question_id, text, question_type))
            return question_id
        else:
            print("Either text is empty, or type isn't valid")
            return None

    def create_question_answer(self, question_id, value, description):
        if not self.survey_questions[question_id]:
            print ("Error no question found")
        elif value and description:
            (response_id,) = self._database.createSurveyQuestionResponse(question_id, value, description)
            response = Response(response_id, value, description)
            self.survey_questions[question_id].add_response(response)
        else:
            print ("Error: either value or description were empty")

    def create_multiple_answers(self, question_id, responses):
        for resp in responses:
            self.create_question_answer(question_id, str(resp['value']), str(resp['description']))

    def create_question_constraint_standard(self, question_from_id, response_id, constraint_type, question_to_id):
        question_from = self.zero_index[question_from_id]
        question_to = self.zero_index[question_to_id]
        print ("question_from response ids" + str(question_from.get_response_ids()))
        response_absolute = question_to.get_response_ids()[response_id]
        if not question_from:
            print ("Error no question_from found")
        elif not question_to:
            print ("Error no question_to found")
        # All good, lets make a constraint!
        else:
            constraint_id = self._database.createQuestionConstraintStandard(question_from.question_id, response_absolute,
                                                                            "forbid", question_to.question_id)
            const = Constraint(question_from.question_id, response_absolute, constraint_type)
            const.set_constraint_id(constraint_id)
            question_to.add_constraint(const)

    def create_disclusion_constraint(self, question_from_id, response_from, question_to_id, responses_discluded):
        question_from = self.zero_index[question_from_id]
        question_to = self.zero_index[question_to_id]
        response_from_id = question_from.get_response_ids()[response_from]
        responses_discluded_ids = []
        question_to_ids = question_to.get_response_ids()
        print ("question_from response ids " + str(question_from.get_response_ids()))
        print ("question_to response ids " + str(question_to.get_response_ids()))
        print ("responses_discluded: " + str(responses_discluded))
        for discluded in responses_discluded:
            responses_discluded_ids.append(question_to_ids[discluded])
        if not question_from:
            print ("Error no question_from found")
        elif not question_to:
            print ("Error not question_to found")
        # Wow this a good looking constraint, lets send it!
        else:
            constraint_modify_id = self._database.createDisclusionConstraint(question_from.question_id, response_from_id,
                                                                             question_to.question_id, responses_discluded_ids)
            mod_const = ModifyConstraint(question_from.question_id, response_from_id, responses_discluded)
            mod_const.set_modify_constraint_id(constraint_modify_id)
            question_to.add_modify_constraint(mod_const)

    def change_question_text(self, question_id, new_text):
        if self._database.getQuestion(question_id):
            self._database.changeQuestionText(question_id, new_text)
            return True
        else:
            return False

    def change_question_response(self, question_id, question_response_id, response_description=None,
                                 response_value=None):
        question_responses = self._database.getResponses(question_id)
        # TODO: Probably change this logic.
        flag = False
        for response in question_responses:
            if question_response_id == response[0]:
                flag = True
                break

        if flag and response_description:
            self._database.changeQuestionResponseDescription(question_response_id, response_description)
        if flag and response_value:
            self._database.changeQuestionResponseValue(question_response_id, response_value)
        return flag
