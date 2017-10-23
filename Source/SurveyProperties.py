#!/bin/python
# coding: utf-8
from Database import Database
import yaml


class SurveyProperties:
    
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        sql = cfg["mysql"]
        db = sql['database']
        hostname = sql["hostname"]
        username = sql["username"]
        password = sql["password"]
        self._database = Database(db, hostname, username, password)
        
        def getSurveyName(self, surveyId)
    	surveyName = self._database.getSurveyName(surveyId)
    	return surveyName
