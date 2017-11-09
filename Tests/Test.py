#!/bin/python
# coding: utf-8

class Test:
    _name=''
    _totalTests=0
    _passedTests=0
    _failedTests=0

    def __init__(self, name):
        self._name = name
        print("Running Tests for: %s." % (name))

    def test(self, name, value):
        self._totalTests += 1
        printVal = 'Pass' if value else 'Fail'
        print(" (%d) %s -> %s" % (self._totalTests, name, printVal))
        if value:
            self._passedTests += 1
        else:
            self._failedTests += 1
        return value

    def showReport(self):
        print("Report:")
        print("  Total Test: %d" % (self._totalTests))
        print("  Passing Tests: %d, Rate: %.2f%%" % (self._passedTests, ((self._passedTests / self._totalTests) * 100)))
        print("  Failing Tests: %d, Rate: %.2f%%" % (self._failedTests, ((self._failedTests / self._totalTests) * 100)))
