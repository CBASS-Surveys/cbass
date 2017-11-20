#!/bin/python
# coding: utf-8
import yaml

from Database import Database

survey_properties_types = {'before-text', 'after-text'}


class SurveyProperties:
    before_text = None
    after_text = None
    survey_id = None

    def __init__(self, survey_id):

        self.survey_id = survey_id
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        self._database = Database(db, hostname, username, password)

    def get_survey_name(self):

        survey_name = self._database.getSurveyName(self.survey_id)
        return survey_name

    def get_survey_properties(self):

        properties = self._database.getSurveyProperties(self.survey_id)
        if properties:
            return properties
        else:
            return None

    def create_property(self, survey_id, property_name, property_value):
        if property_name in survey_properties_types:
            self._database.createNewSurveyProperty(survey_id, property_name, property_value)
            return True
        else:
            print ("Error: property_name {%s} not found")
            return False

    def update_property(self, survey_id, property_name, property_value):
        if property_name in survey_properties_types:
            self._database.updateSurveyProperty(survey_id, property_name, property_value)
            return True
        else:
            print ("Error: property_name {%s} not found")
            return False


if __name__ == "__main__":
    sp = SurveyProperties(2)
    p = sp.get_survey_properties()
    print
