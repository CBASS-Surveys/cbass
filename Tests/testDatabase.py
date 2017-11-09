#!/bin/python
# coding: utf-8

from Database import Database
from Test import TestSuite, TestCase
from os import urandom
from binascii import hexlify

myDB = Database('cbass_test', 'localhost', 'swflint', 'swflint')

auth = TestSuite("User Authentication")

@TestCase(auth, "Correct Password")
def testCorrectPassword():
    return myDB.authenticateUser('test', 'fooBar')

@TestCase(auth, "Incorrect Password")
def testIncorrectPassword():
    return not myDB.authenticateUser('test', 'moo')

@TestCase(auth, "Invalid Username")
def testInvalidUsername():
    try:
        return myDB.authenticateUser('cow', 'pig')
    except:
        return False

auth.showReport()

print("")

userManip = TestSuite("User Manipulation")
uname = hexlify(urandom(8))
pword = hexlify(urandom(8))
email = hexlify(urandom(16))
newPword = hexlify(urandom(8))

@TestCase(userManip, "User Insertion (by existence verification)", uname, pword, email)
def testUserInsertion(user, password, email):
    myDB.createUser(user, email, password)
    return myDB.authenticateUser(user, password)

@TestCase(userManip, "Change Password (by validity verification)", uname, newPword)
def testUserPasswordChange(user, password):
    myDB.updatePassword(user, password)
    return myDB.authenticateUser(user, password)

userManip.showReport()

print("")

surveyContents = TestSuite("Survey Data and Contents")
@TestCase(surveyContents, "Returns Correct Name")
def testNameOfSurvey():
    return "Check Name" == myDB.getSurveyName(1)

@TestCase(surveyContents, "Returns Correct Properties")
def testSurveyProperties():
    testDictionary = {
        'before_text': 'Test Text Before',
        'after_text': 'Test After Text'
    }
    dictFromDB = myDB.getSurveyProperties(0)
    for key in dictFromDB.keys():
        if not key in testDictionary.keys():
            return False
    for key in testDictionary.keys():
        if not key in dictFromDB.keys():
            return False
    for key in dictFromDB.keys():
        if dictFromDB[key] != testDictionary[key]:
            return False
    return True

surveyContents.showReport()
