#!/bin/python
# coding: utf-8

import sys
from Database import Database
from Test import TestSuite, TestCase
from os import urandom
from binascii import hexlify

myDB = Database('cbass_test', 'localhost', 'swflint', 'swflint')

auth = TestSuite("User Authentication")

@TestCase(auth, "Authentication W/ Valid Password")
def testCorrectPassword(printer):
    return myDB.authenticateUser('test', 'fooBar')

@TestCase(auth, "Authentication W/ Invalid Password")
def testIncorrectPassword(printer):
    return not myDB.authenticateUser('test', 'moo')

@TestCase(auth, "Authentication W/ Invalid Username")
def testInvalidUsername(printer):
    try:
        return not myDB.authenticateUser('cow', 'pig')
    except:
        e = sys.exc_info()[0]
        printer("Raises error: %s" % (e))
        return False

uname = hexlify(urandom(8))
pword = hexlify(urandom(8))
email = hexlify(urandom(16))
newPword = hexlify(urandom(8))

@TestCase(auth, "User Creation", uname, pword, email)
def testUserInsertion(printer, user, password, email):
    myDB.createUser(user, email, password)
    return myDB.authenticateUser(user, password)

@TestCase(auth, "User password change", uname, newPword)
def testUserPasswordChange(printer, user, password):
    myDB.updatePassword(user, password)
    return myDB.authenticateUser(user, password)


auth.showReport()

print("")

surveyContents = TestSuite("Survey Data and Contents")
@TestCase(surveyContents, "Returns Correct Name")
def testNameOfSurvey(printer):
    name = myDB.getSurveyName(1)
    value = "Test Survey" == name
    if not value:
        printer(type(name))
    return value

@TestCase(surveyContents, "Returns Correct Properties")
def testSurveyProperties(printer):
    testDictionary = {
        'before_text': 'Test Text Before',
        'after_text': 'Test After Text'
    }
    dictFromDB = myDB.getSurveyProperties(1)
    for key in dictFromDB.keys():
        if not key in testDictionary.keys():
            printer("%s is not in the known data." % (key))
            return False
    for key in testDictionary.keys():
        if not key in dictFromDB.keys():
            printer("%s is not in the data from the database." % (key))
            return False
    for key in dictFromDB.keys():
        if dictFromDB[key] != testDictionary[key]:
            printer("Value for key '%s' in database and dictionary are not the same." % (key))
            return False
    return True

def testSurveyQuestionRetrieval(printer):
    pass

def testQuestionResponseRetrieval(printer):
    pass

def testQuestionConstraintRetrieval(printer):
    pass

surveyContents.showReport()

print("")

surveyInsertion = TestSuite("Survey Data Insertion/Survey Creation")

def testSurveyCreation(printer):
    pass

def testQuestionCreation(printer):
    pass

def testQuestionResponseCreation(printer):
    pass

def testQuestionConstraintCreation(printer):
    pass

def testQuestionRemoval(printer):
    pass

def testQuestionResponseRemoval(printer):
    pass

def testQuestionConstraintRemoval(printer):
    pass

surveyInsertion.showReport()

print("")

surveyResponseInsertion = TestSuite("Survey Response Insertion")

responseString = hexlify(urandom(32))
responseID = 0

@TestCase(surveyResponseInsertion, "Survey Response Insertion", responseString)
def testSurveyResponseInsertion(printer, responseString):
    (temp1, temp2) = myDB.createSurveyResponse(1, responseString)
    responseID = temp2
    return temp1 == responseString

@TestCase(surveyResponseInsertion, "Insert Single Response", responseID)
def testQuestionResponseInsertionNormal(printer, responseID):
    (temp1, temp2) = myDB.insertSurveyQuestionResponse(responseID, 1, 1)
    return temp2 == 1

@TestCase(surveyResponseInsertion, "Insert Multi Response", responseID)
def testQuestionResponseInsertionMulti(printer, responseID):
    (temp1, temp2) = myDB.insertSurveyQuestionResponse(responseID, 2, [3, 4])
    return temp2 == [3, 4]

@TestCase(surveyResponseInsertion, "Insert Long Form Response", responseID)
def testQuestionResponseInsertionLongFormResponse(printer, responseID):
    (temp1, temp2) = myDB.insertSurveyQuestionLongFormResponse(responseID, 3, "Some Text")
    return temp2 == "Some Text"

@TestCase(surveyResponseInsertion, "Check Single Response", responseID)
def testQuestionResponseCheckNormal(printer):
    printer.("No method to get question single responses")
    return false

@TestCase(surveyResponseInsertion, "Check Mulit Response", responseID)
def testQuestionResponseCheckMulti(printer):
    printer.("No method to get question multi responses")
    return false

surveyResponseInsertion.showReport()
