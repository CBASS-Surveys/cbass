#!/bin/python
# coding: utf-8

from binascii import hexlify, unhexlify
from hashlib import pbkdf2_hmac
from os import urandom

import psycopg2


class Database:
    _connection = False

    def __init__(self, database, hostname, username, password):
        self._connection = psycopg2.connect(dbname=database, user=username, password=password, host=hostname)

    def authenticateUser(self, username, password):
        cursor = self._connection.cursor()
        cursor.execute("SELECT password_hash, password_salt FROM users WHERE username=%s;", (username,))
        (hash, salt) = cursor.fetchone()
        cursor.close()
        if (hash == hexlify(pbkdf2_hmac('sha256', password, unhexlify(salt), 5))):
            return True
        else:
            return False

    def createUser(self, username, email, password):
        salt = urandom(32)
        hash = hexlify(pbkdf2_hmac('sha256', password, salt, 5))
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, user_email, password_hash, password_salt) VALUES (%s, %s, %s, %s);",
            (username, email, hash, hexlify(salt)))
        self._connection.commit()
        cursor.close()

    def updatePassword(self, username, password):
        cursor = self._connection.cursor()
        salt = urandom(32)
        hash = hexlify(pbkdf2_hmac('sha256', password, salt, 5))
        cursor.execute("UPDATE users SET password_hash=%s, password_salt=%s WHERE username = %s;",
                       (hash, hexlify(salt), username))
        self._connection.commit()
        cursor.close()

    def createSurvey(self, name, authorName, **kwargs):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO surveys (name, author) VALUES (%s, (SELECT id FROM users WHERE username = %s)) RETURNING id;",
            (name, authorName))
        (surveyID) = cursor.fetchone()
        for key in kwargs.keys():
            cursor.execute("INSERT INTO survey_properties (survey_id, name, value) VALUES (%s, %s, %s);",
                           (surveyID, key, kwargs[key]))
        self._connection.commit()
        cursor.close()
        return surveyID

    def createSurveyQuestion(self, survey, text, type):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO survey_question (survey, question_text, question_type) VALUES (%s, %s, %s) RETURNING question_id;",
            (survey, text, type))
        (questionID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return questionID

    def createSurveyQuestionResponse(self, question, value, description):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO question_response (survey, question, value, description) VALUES ((SELECT survey FROM survey_question WHERE question_id = %s), %s, %s, %s) RETURNING id;",
            (question, question, value, description))
        (responseID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return responseID

    def createQuestionConstraintStandard(self, questionFrom, response, type, to):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO question_constraints (question_from, response_from, type, question_affected) VALUES (%s, %s, %s, %s) RETURNING id;",
            (questionFrom, response, type, to))
        (constraintID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return constraintID

    def createDisclusionConstraint(self, questionFrom, responseFrom, questionTo, responsesDiscluded):
        print("values sent in")
        print(questionFrom)
        print(responseFrom)
        print(questionTo)
        print(responsesDiscluded)
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO question_constraint_modify (question_from, response_from, question_to, responses_discluded) VALUES (%s, %s, %s, %s) RETURNING id;",
            (questionFrom, responseFrom, questionTo, responsesDiscluded));
        (constraintID) = cursor.fetchone()
        self._connection.commit()
        cursor.close()
        return constraintID

    def createSurveyResponse(self, survey, identifierString):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO survey_response (survey, identifier_string) VALUES (%s, %s) RETURNING id, identifier_string;",
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
        cursor.execute(
            "INSERT INTO survey_long_form_response (response_id, response_to, response) VALUES (%s, %s, %s);",
            (responseID, questionID, responseText))
        self._connection.commit()
        cursor.close()
        return (responseID, questionID)

    def getConstraints(self, affectedQuestion):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT question_from, response_from, type FROM question_constraints WHERE question_affected = %s;",
            (affectedQuestion,))
        return cursor

    def getModifyConstraints(self, affectedQuestion):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT question_from, response_from, responses_discluded FROM question_constraint_modify WHERE question_to = %s;",
            (affectedQuestion,))
        return cursor

    def hasResponse(self, question, response, id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_type FROM survey_question WHERE question_id = %s;", (question,))
        (type,) = cursor.fetchone()
        if (type == "single-response"):
            cursor.execute(
                "SELECT true FROM survey_response_entry WHERE response_to = %s AND response_id = %s AND response = %s;",
                (question, id, response))
            if cursor.rowcount == 0:
                return False
            else:
                return True
        elif (type == 'free-response'):
            return False
        else:
            cursor.execute("SELECT response FROM survey_multi_response WHERE response_to = %s AND response_id = %s;",
                           (question, id))
            (values,) = cursor.fetchone()
            return (response in values)

    def getQuestion(self, ID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_text, question_type FROM survey_question WHERE question_id = %s;", (ID,))
        question = cursor.fetchone()
        cursor.close()
        return question

    def getResponses(self, questionID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, value, description FROM question_response WHERE question = %s;", (questionID,))
        return cursor

    def getResponsesToSurvey(self, survey_id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT id FROM survey_response WHERE survey = %s;", (survey_id,))
        return cursor

    def getSurveyQuestions(self, surveyID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_id FROM survey_question WHERE survey = %s;", (surveyID,))
        return cursor

    def getSurveyProperties(self, surveyID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT name, value FROM survey_properties WHERE survey_id = %s;", (surveyID,))
        properties = {}
        for response in cursor:
            (name, value) = response
            properties[name] = value
        cursor.close()
        return properties

    def getSurveyName(self, surveyID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT name FROM surveys WHERE id = %s;", (surveyID,))
        (name,) = cursor.fetchone()
        cursor.close()
        return name

    def getIndividualResponseToQuestion(self, questionID, responseID):
        cursor = self._connection.cursor()
        cursor.execute("SELECT question_type FROM survey_question WHERE question_id = %s;", (questionID,))
        (type,) = cursor.fetchone()
        if (type == 'single-response'):
            cursor.execute("SELECT response FROM survey_response_entry WHERE response_to = %s AND response_id = %s;",
                           (questionID, responseID))
            value = cursor.fetchone()
            if value == None:
                return value
            else:
                TheValue = value[0]
                cursor.execute("SELECT value FROM question_response WHERE id = %s", (TheValue,))
                (value,) = cursor.fetchone()
                return value
        elif (type == 'free-response'):
            cursor.execute(
                "SELECT response FROM survey_long_form_response WHERE response_to = %s AND response_id = %s;",
                (questionID, responseID))
            value = cursor.fetchone()
            if value == None:
                return value
            else:
                return value[0]
        else:
            cursor.execute("SELECT response FROM survey_multi_response WHERE response_to = %s AND response_id = %s;",
                           (questionID, responseID))
            value = cursor.fetchone()
            if value == None:
                return value
            else:
                values = value[0]
                retVals = []
                for rid in values:
                    cursor.execute("SELECT value FROM question_response WHERE id = %s", (rid,))
                    (rval,) = cursor.fetchone()
                    retVals.append(rval)
                return retVals

    def changeQuestionText(self, question_id, new_text):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE survey_question SET question_text = %s WHERE question_ID = %s", (new_text, question_id))
        cursor.close()

    def changeQuestionResponseDescription(self, question_response_id, question_response_description):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE question_response SET description = %s WHERE id = %s",
                       (question_response_description, question_response_id))
        cursor.close()

    def changeQuestionResponseValue(self, question_response_id, question_response_value):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE question_respose SET value = %s WHERE id = %s",
                       (question_response_value, question_response_id))
        cursor.close()

    def createNewSurveyProperty(self, surveyID, property_name, property_value):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO survey_properties (survey_id, name, value) VALUES (%s, %s, %s)",
                       (surveyID, property_name, property_value))
        cursor.close()

    def updateSurveyProperty(self, surveyID, property_name, property_value):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE survey_properties SET value = %s WHERE survey_id = %s AND name = %s",
                       (property_value, surveyID, property_name))
        if cursor.statusmessage == 'UPDATE 0':
            return False
        else:
            return True
        cursor.close()

    def surveyToDict(self, surveyID):
        questionValues = {}
        questions = self._connection.cursor()
        questions.execute("SELECT question_id, question_text, question_type FROM survey_question WHERE survey = %s", (surveyID,))
        for question in questions:
            (id, questionText, questionType) = question
            questionValues[id] = {'text': questionText, 'type': questionType}
            if questionType in ('single-response', 'multi-choice-response'):
                responseVals = {}
                responses = self._connection.cursor()
                responses.execute("SELECT id, value, description FROM question_response WHERE question = %s", (id,))
                for response in responses:
                    (rID, val, description) = response
                    responseVals[rID] = {'description': description, 'export_value': val}
                questionValues[id]['responses'] = responseVals
        return questionValues
