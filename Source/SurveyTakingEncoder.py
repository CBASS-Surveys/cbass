import json

from flask.json import JSONEncoder
from SurveyTakingController import SurveyTakingController
from Question import Question
from Response import Response
from Constraints import Constraint, ModifyConstraint


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        return self.to_json(obj)

    def to_json(self, obj):
        json_questions = []
        for question in obj.survey_questions:
            answers = []
            if question.answers:
                for resp in question.answers:
                    answers += [{"response_id": resp.response_id, "value": resp.response_value,
                                 "description": resp.response_description}]
            constraints = []
            if question.constraints:
                for const in question.constraints:
                    constraints += [
                        {"question_from": const.question_from, "response_from": const.response_from,
                         "question_to": question.question_id,
                         "type": const.type}]
            if question.modify_constraints:
                for const in question.modify_constraints:
                    constraints += [
                        {"question_from": const.question_from, "response_from": const.response_from,
                         "question_to": question.question_id,
                         "type": "modify", "responses_discluded": const.response_discluded}]
            json_questions += [
                {"question_id": question.question_id, "text": question.question_text, "type": question.question_type,
                 "answers": answers,
                 "constraints": constraints}]
        json_STC = {"response_id": obj.response_id, "question_number": obj.question_number,
                    "survey_id": obj.survey_id, "questions": json_questions}
        return json_STC


def from_json(obj):
    question_number = obj['question_number']
    response_id = obj['response_id']
    survey_id = obj['survey_id']
    survey_questions = []
    for q in obj['questions']:
        question = Question(q['questin_id'], q['text'], q['type'])
    if q['answers']:
        responses = []
        for resp in q['answers']:
            responses += [Response(resp['response_id'], resp['value'], resp['description'])]
        question.set_answers(responses)
    if q['constraints']:
        constraints = []
        modify_constraints = []
        for con in q['constraints']:
            if con['type'] == 'forbids' or con['type'] == 'forbid':
                constraints += [Constraint(con['question_from'], con['response_from'], con['type'])]
            else:
                modify_constraints += [
                    ModifyConstraint(con['question_from'], con['response_from'], con['responses_discluded'])]
        question.set_constraints(constraints)
        question.set_modify_constraints(modify_constraints)
        survey_questions.append(question)
    stc = SurveyTakingController()
    stc.survey_id = survey_id
    stc.question_number = question_number
    stc.survey_questions = survey_questions
    stc.current_question = survey_questions[question_number]
    stc.response_id = response_id
    return stc


if __name__ == "__main__":
    stc = SurveyTakingController(2)
    stc.get_survey_questions()
    test = json.dumps(stc, cls=CustomEncoder)
    new_stc = from_json(test)