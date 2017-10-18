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
