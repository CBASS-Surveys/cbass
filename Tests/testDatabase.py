#!/bin/python
# coding: utf-8

from Database import Database
from Test import Test
from os import urandom
from binascii import hexlify

myDB = Database('cbass_test', 'localhost', 'swflint', 'swflint')

auth = Test("User Authentication")
auth.test("Correct Password", myDB.authenticateUser('test', 'fooBar'))
auth.test("Incorrect Password", not myDB.authenticateUser('test', 'moo'))
# auth.test("Invalid Username", not myDB.authenticateUser('cow', 'pig'))
auth.showReport()

print("")

userManip = Test("User Manipulation")
uname = hexlify(urandom(8))
pword = hexlify(urandom(8))
email = hexlify(urandom(16))
myDB.createUser(uname, email, pword)
userManip.test("Insert User (by verifying existence)", myDB.authenticateUser(uname, pword))
newPword = hexlify(urandom(8))
myDB.updatePassword(uname, newPword)
userManip.test("Change Password (by verifying new validity)", myDB.authenticateUser(uname, newPword))
userManip.showReport()

print("")

surveyContents = Test("Survey Data and Contents")
name = myDB.getSurveyName(1)
surveyContents.test("Check Name", name == "Test Survey")
dataTestDict = {
    'before_text': 'Test Text Before',
    'after_text': 'Test After Text'
}
theDict = myDB.getSurveyProperties(0)
surveyContents.test("Check Properties", dataTestDict == theDict)
# And add the rest of the DB tests
