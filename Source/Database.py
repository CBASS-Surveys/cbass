#!/bin/python
# coding: utf-8

import psycopg2
from hashlib import pbkdf2_hmac
from binascii import hexlify
from os import urandom

class Database:

    _connection = false

    def __init__(database, host, username, password):
        self._connection = psycopg.connect(dbname=database, user=username, password=password, host=hostname)

    def authenticateUser(self, username, password):
        cursor = self._connection.cursor()
        cursor.execute("SELECT password_hash, password_salt FROM users WHERE username=%s;", (username))
        (hash, salt) = cursor.fetchone()
        cursor.close()
        if (hash == hexlify(pbkdf2_hmac('sha256', password, salt))):
            return True
        else:
            return False

    def createUser(self, username, email, password):
        salt = urandom(32)
        hash = hexlify(pbkdf2_hmac('sha256', password, salt))
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO users (username, user_email, password_hash, password_salt) VALUES (%s, %s, %s, %s);",
                       (username, email, hash, salt))
        self._connection.commit()
        cursor.close()

    def updatePassword(self, username, password):
        cursor = self._connection.cursor()
        salt = urandom(32)
        hash = hexlify(pbkdf2_hmac('sha256', password, salt))
        cursor.execute("UPDATE users SET password_hash=%s, password_salt=%s WHERE username = %s;",
                       (hash, salt, username))
        self._connection.commit()
        cursor.close()

    def createSurvey(self, name, authorName, **kwargs):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO surveys (name, author) VALUES (%s, (SELECT id FROM users WHERE username = %s)) RETURNING id;",
                       (name, authorName))
        (surveyId) = cursor.fetchone()
        for key in kwargs.keys():
            cursor.execute("INSERT INTO survey_properties (survey_id, name, value) VALUES (%s, %s, %s);",
                           (surveyID, key, kwargs[key]))
        self._connection.commit()
        cursor.close()
        return surveyID

    def createSurveyQuestion(self, survey, text, type):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_question (survey, question_text, question_type) VALUES (%s, %s, %s) RETURNING question_id;",
                       (survey, text, type))
        (questionID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return questionID

    def createSurveyQuestionResponse(self, question, value, description):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO question_response (survey, question, value, description) VALUES ((SELECT survey FROM survey_question WHERE question_id = %s), %s, %s, %s) RETURNING id;",
                       (question, question, value, description))
        (responseID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return responseID

    def createQuestionConstraintStandard(self, questionFrom, response, type, to):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO question_constraints (question_from, response_from, type, question_affected) VALUES (%s, %s, %s, %s) RETURNING id;",
                       (questionFrom, response, type, to))
        (constraintID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return constraintID

    def createDisclusionConstraint(self, questionFrom, responseFrom, questionTo, responsesDiscluded):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO question_constraint_modify (question_from, response_from, question_to, responses_discluded) VALUES (%s, %s, %s, %s) RETURNING id;",
                       (questionFrom, responseFrom, questionTo, responsesDiscluded));
        (constraintID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return constraintID

    def createSurveyResponse(self, survey, identifierString):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_response (survey, identifier_string) VALUES (%s, %s) RETURNING id, identifier_string;",
                    (survey, identifierString))
        (responseID, identString) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return (responseID, identString)

    def insertSurveyQuestionResponse(self, responseID, questionID, response):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_response_entry (response_id, response_to, response) VALUES (%s, %s, %s);",
                       (responseID, questionID, response))
        self._connection.commit()
        cursor.close()
        return (responseID, questionID)

    def insertSurveyQuestionMultiResponse(self, responseID, questionID, responses):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_multi_response (response_id, response_to, response) VALUES (%s, %s, %s);",
                       (responseID, questionID, responses))
        self._connection.commit()
        cursor.close()
        return (responseID, questionID)

    def insertSurveyQuestionLongFormResponse(self, responseID, questionID, responseText):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_long_form_response (response_id, response_to, response) VALUES (%s, %s, %s);"
                       (responseID, questionID, responseText))
        self.connection.commit()
        cursor.close()
        return (responseID, questionID)

    def getConstraints(self, affectedQuestion):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_from, response_from, type FROM question_constraints WHERE question_affected = %s;", (affectedQuestion,))
        return cursor

    def getModifyConstraints(self, affectedQuestion):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_from, response_from, responses_discluded FROM question_constraint_modify WHERE question_to = %s;", (affectedQuestion,))
        return cursor

    def hasResponse(self, question, response, id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_type FROM survey_question WHERE question_id = %s;", (question,))
        (type) = cursor.fetchone()
        if (type == "single-response"):
            cursor.execute("SELECT true FROM survey_response_entry WHERE response_to = %s AND response_id = %s AND response = %s;",
            (question, id, response))
            (value) = cursor.fetchone()
            return value
        elif (type == 'free-response'):
            return false
        else:
            cursor.execute("SELECT response FROM survey_multi_response WHERE response_to = %s AND response_id = %s;",
                           (question, id))
            (values) = cursor.fetchone()
            return (response in values)

    
