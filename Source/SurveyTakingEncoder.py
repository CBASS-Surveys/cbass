import json
from flask.json import JSONEncoder
from SurveyTakingController import SurveyTakingController

class CustomEncoder(JSONEncoder):
    def default(self, obj):
        return self.to_json(obj)

    def to_json(self, obj):
        json_questions = []
        for question in obj.survey_questions:
            answers = []
            if question.answers:
                for resp in question.answers:
                    answers += [{"value": resp.response_value, "description": resp.response_description}]
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
            json_questions += [{"text": question.question_text, "type": question.question_type, "answers": answers,
                                "constraints": constraints}]
        json_STC = {"response_id": obj.response_id, "question_number": obj.question_number,
                    "survey_id": obj.survey_id, "questions": json_questions}
        return json_STC

    def from_json(self, obj):
        current_question = obj['question_number']
        response_id = obj['response_id']
        survey_id = obj['survey_id']
        for question in obj['questions']:


