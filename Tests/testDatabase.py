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

@TestCase(surveyContents, "Question Retrieved Correctly")
def testSurveyQuestionRetrieval(printer):
    (text, qType) = myDB.getQuestion(1)
    value = (text == "Single Response 1") and (qType == 'single-response')
    if not value:
        printer(text)
        printer(qType)
    return value

@TestCase(surveyContents, "Responses Retrieved Correctly")
def testQuestionResponseRetrieval(printer):
    expectedValues = [(1, 'foo', 'Foo'), (2, 'barfoo', 'Bar')]
    retrievedValues = []
    cursor = myDB.getResponses(1)
    for val in cursor:
        retVal = val in expectedValues
        retrievedValues.append(val)
        if not retVal:
            printer("Retrieved value (%s, '%s', '%s') not in expected values." % (val[0], val[1], val[2]))
            return False
    for val in expectedValues:
        retVal = val in retrievedValues
        if not retVal:
            printer("Expected value (%s, '%s', '%s') not in retrieved values." % (val[0], val[1], val[2]))
            return False
    return True

@TestCase(surveyContents, "Normal Constraints Retrieved Correctly")
def testQuestionConstraintRetrievalNormal(printer):
    expectedConstraints = [(1, 1, 'require'), (1, 2, 'forbid')]
    retrievedConstraints = []
    cursor = myDB.getConstraints(3)
    for val in cursor:
        retVal = val in expectedConstraints
        retrievedConstraints.append(val)
        if not retVal:
            printer("Retrieved constraint (%s, %s, '%s') not in expected constraints." % (val[0], val[1], val[2]))
            return False
    for val in expectedConstraints:
        retVal = val in retrievedConstraints
        if not retVal:
            printer("Expected constraint (%s, %s, '%s') not in retrieved constraints." % (val[0], val[1], val[2]))
            return False
    return True

@TestCase(surveyContents, "Modify Constraints Retrieved Correctly")
def testQuestionConstraintRetrievalModify(printer):
    expectedConstraint = (1, 2, [5, 6])
    value = myDB.getModifyConstraints(4).fetchone()
    ret = value == expectedConstraint
    if not value:
        printer("Retrieved constraint (%s, %s, %s) not expected." % value)
    return ret
    
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
    responseID = temp1
    return temp2 == responseString

@TestCase(surveyResponseInsertion, "Insert Single Response", responseID)
def testQuestionResponseInsertionNormal(printer, responseID):
    try:
        (temp1, temp2) = myDB.insertSurveyQuestionResponse(responseID, 1, 1)
        return temp2 == 1
    except:
        e = sys.exc_info()[0]
        printer("Raises error: %s" % (e))
        return False

@TestCase(surveyResponseInsertion, "Insert Multi Response", responseID)
def testQuestionResponseInsertionMulti(printer, responseID):
    try:
        (temp1, temp2) = myDB.insertSurveyQuestionResponse(responseID, 2, [3, 4])
        return temp2 == [3, 4]
    except:
        e = sys.exc_info()[0]
        printer("Raises error: %s" % (e))
        return False

@TestCase(surveyResponseInsertion, "Insert Long Form Response", responseID)
def testQuestionResponseInsertionLongFormResponse(printer, responseID):
    try:
        (temp1, temp2) = myDB.insertSurveyQuestionLongFormResponse(responseID, 3, "Some Text")
        return temp2 == "Some Text"
    except:
        e = sys.exc_info()[0]
        printer("Raises error: %s" % (e))
        return False

@TestCase(surveyResponseInsertion, "Check Single Response", responseID)
def testQuestionResponseCheckNormal(printer, responseID):
    printer("No method to get question single responses")
    return False

@TestCase(surveyResponseInsertion, "Check Mulit Response", responseID)
def testQuestionResponseCheckMulti(printer, responseID):
    printer("No method to get question multi responses")
    return False

surveyResponseInsertion.showReport()
