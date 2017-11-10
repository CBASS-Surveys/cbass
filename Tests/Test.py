#!/bin/python
# coding: utf-8

class TestSuite:
    _name=''
    _testsRun = False
    _passedTests=0
    _failedTests=0
    _tests = []

    def __init__(self, name):
        self._testsRun = False
        self._passedTests=0
        self._failedTests=0
        self._tests = []
        self._name = name
        print("Running Tests for: %s." % (name))

    def addTest(self, test):
        self._tests.append(test)

    def runTests(self):
        self._testsRun = True
        i = 0
        for test in self._tests:
            i += 1
            name = test.getName()
            value = test.test()
            printValue = 'Pass' if value else 'Fail'
            print(" (%d) %s -> %s" % (i, name, printValue))
            if value:
                self._passedTests += 1
            else:
                self._failedTests += 1
            if test.getOutput() != "":
                print(test.getOutput())

    def showReport(self):
        if not self._testsRun:
            self.runTests()
        print("Report:")
        print("  Total Test: %d" % (len(self._tests)))
        print("  Passing Tests: %d, Rate: %.2f%%" %
              (self._passedTests, ((self._passedTests / float(len(self._tests)))) * 100))
        print("  Failing Tests: %d, Rate: %.2f%%" %
              (self._failedTests, ((self._failedTests / float(len(self._tests)))) * 100))

class TestCase:
    def __init__(self, testSuite, name, *args, **kwargs):
        self._name = name
        self._args = args
        self._kwargs = kwargs
        self._output = ""
        self._seenOutput = False
        testSuite.addTest(self)

    def __call__(self, function):
        self._function = function
        return function

    def __printer__(self, value):
        if self._seenOutput:
            self._output = self._output + "\n     %s"%(value)
        else:
            self._output = "     %s"%(value)
            
    def test(self):
        return self._function(self.__printer__, *self._args, **self._kwargs)

    def getName(self):
        return self._name

    def getOutput(self):
        return self._output
