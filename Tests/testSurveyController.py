#!/bin/python
# coding: utf-8

from Source.Database import Database
from Test import TestSuite, TestCase
from Source.SurveyTakingController import SurveyTakingController
# will need to change when this gets updated to dev
from Source.SurveyTakingController import Question, Response
import uuid
import json

myDB = Database('cbass_test', 'localhost', 'swflint', 'swflint')
# myDB = Database('test', 'localhost', 'postgres', 'WauPal69045!')
question = TestSuite("Question Testing")


@TestCase(question, "Test if all Questions are loaded")
def question_length(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    cursor = myDB.getSurveyQuestions(1)
    rowcount = cursor.rowcount
    cursor.close
    # subtract for null question
    return rowcount == (len(svc.survey_questions) -1)


@TestCase(question, "Test if questions match DB")
def first_question(printer):
    fq = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    fq.start_survey(session_id)
    cursor = myDB.getSurveyQuestions(1)
    flag = True
    i = 1
    for (qId,) in cursor:
        data = myDB.getQuestion(qId)
        check_q = fq.get_question(i)
        flag = check_q.question_id == qId and check_q.question_text == data[0] and check_q.question_type == data[1] and flag
        i += 1
    cursor.close()
    return flag


@TestCase(question, "Verify answers for test questions")
def get_response(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    cursor = myDB.getSurveyQuestions(1)
    i = 1
    for (qId,) in cursor:
        cursor2 = myDB.getResponses(qId)
        check_q = svc.get_question(i)
        flag = True
        j = 0
        for row in cursor2:
            dbr = Response(row[0], row[1], row[2])
            flag = (dbr == check_q.answers[j]) and flag
            j += 1
        i += 1

    return flag


@TestCase(question, "Verify single-response was recorded to DB")
def has_response(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    response_id = svc.response_id
    question_id = svc.current_question.question_id
    response = '2'
    svc.send_response_v2(response)
    return myDB.hasResponse(question_id, 2, response_id)


@TestCase(question, "Verify multi-response was recorded to DB")
def has_response(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    response_id = svc.response_id
    response = '2'
    svc.send_response_v2(response)

    svc.get_next_question()
    question_id = svc.current_question.question_id
    svc.send_response_v2('[4,5]')
    return myDB.hasResponse(question_id, 4, response_id) and myDB.hasResponse(question_id, 5, response_id)


@TestCase(question, "Verify constraint-modify works")
def test_constraint(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    svc.send_response_v2('1')
    response_id = svc.response_id
    svc.get_next_question()
    svc.send_response_v2('[4]')
    svc.get_next_question()
    svc.send_response_v2(json.dumps("free-response"))
    svc.get_next_question()
    svc.send_response_v2('8')

    question = svc.get_next_question()
    return True

@TestCase(question, "Verify Forbids Constraints Works")
def test_constraint_forbid(printer):
    svc = SurveyTakingController(1)
    session_id = "test " + str(uuid.uuid4())
    svc.start_survey(session_id)
    svc.send_response_v2('2')
    response_id = svc.response_id
    svc.get_next_question()
    svc.send_response_v2('[4]')
    svc.get_next_question()
    
    return svc.current_question.question_id == 4


question.showReport()
