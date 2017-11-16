# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:58:28 2017

@author: hpollman
"""

from Database import Database
import yaml
from Question import Question
from Response import Response
from Constraints import Constraint, ModifyConstraint


class SurveyCreationController:
    _database = None
    question_types = {'single-response', 'multi-choice-response', 'free-response'}
    constraint_standards = {'forbids','requires'}
    
    def __init__(self):
        
        self.survey_id = None
        self.survey_questions = {}

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        # dump(hostname, username, password)
        self._database = Database(db, hostname, username, password)
        
    def create_survey(self, name, authorName, **kwargs):
        self.survey_id=self._database.createSurvey(name, authorName, **kwargs)
        
    def create_survey_question(self, text, question_type):
        if text and question_type in self.question_types:
            question_id=self._database.createSurveyQuestion(self.survey_id, text, question_type)
            self.survey_questions[question_id]=Question(question_id, text, question_type)
            return question_id
        else:
            print("Either text is empty, or type isn't valid")
            return None
        
    def create_question_response(self, question_id, value, description): 
        if not self.survey_questions[question_id]:
            print ("Error no question found")
        elif value and description: 
            response_id=self._database.createSurveyQuestionResponse(question_id, value, description)
            response=Response(response_id, value, description)
            self.survey_questions[question_id].add_response(response)
        else:
            print ("Error: either value or description were empty")
    
    def create_multiple_responses(self, question_id, responses):
        for resp in responses:
            self.create_question_response(question_id, resp[0], resp[1])
            
    def create_question_constraint_standard(self, question_from_id, response_id, constraint_type, question_to_id):
        question_from=self.survey_questions[question_from_id]
        question_to=self.survey_questions[question_to_id]
        if not question_from:
            print ("Error no question_from found")
        elif not question_to:
            print ("Error no question_to found")
        elif not constraint_type in self.constraint_standards:
            print("Error no constraint of that type found")
        elif not response_id in question_from.get_response_ids:
            print("Error no response id found in the question_form")
        # All good, lets make a constraint!
        else:
            constraint_id=self._database.createQuestionConstraintStandard(question_from_id, response_id, constraint_type, question_to_id)
            const=Constraint(question_from_id, response_id, constraint_type)
            const.set_constraint_id(constraint_id)
            question_to.add_constraint(const)
    
    def create_disclusion_constraint(self, question_from_id, response_from, question_to_id, responses_discluded):
        question_from=self.survey_questions[question_from_id]
        question_to=self.survey_questions[question_to_id]
        if not question_from:
            print ("Error no question_from found")
        elif not question_to:
            print ("Error not question_to found")
        elif not response_from in question_from.get_response_values:
            print("Error no response value found in the question_form")
        elif not responses_discluded in question_to.get_response_values:
            print("Error one or many or many responses_discluded do not exist")
        # Wow this a good looking constraint, lets send it!
        else:
            constraint_modify_id=self._database.createDisclusionConstraint(question_from_id, response_from, question_to_id, responses_discluded)
            mod_const=ModifyConstraint(question_from_id,response_from,responses_discluded)
            mod_const.set_modify_constraint_id(constraint_modify_id)
            question_to.add_modify_constraint(mod_const)
            
        