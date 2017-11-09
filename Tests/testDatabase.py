#!/bin/python
# coding: utf-8

from Database import Database
from Test import Test

myDB = Database('cbass_test', 'localhost', 'cbass', 'cbass')

auth = Test("User Authentication")
auth.test("Valid Creds", myDB.authenticateUser('test', 'fooBar'))
auth.test("Invalid Creds", not myDB.authenticateUser('test', 'moo'))
auth.showReport()
