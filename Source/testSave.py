import json

json_data = open("surveyCreatorTestData.json").read()

data = json.loads(json_data)
try:
    keys = data.keys()
    survey_name = data["survey_title"]
    author = "Author"

    if 'survey_properties' in keys:
        survey_properties = data["survey_properties"]
    else:
        survey_properties = None
        # router.survey_creation_controller.create_survey(survey_name, author, survey_properties)
    for question in data['questions']:
        q_keys = question.keys()
        question_type = str(question['type'])
        #   question_id = router.survey_creation_controller.create_survey_question(str(question['text']), question_type)
        question_id = 1
        if not question_type == 'free-response':
            if 'answers' in q_keys:
                answers = question['answers']
                #  router.survey_creation_controller.create_multiple_answers(question_id, answers)
            if 'constraints' in q_keys:
                for const in question['constraints']:
                    const_type = str(const['type'])
                    if const_type == 'modify':
                        question_from = const['question_from']
                        response_from = const['response_from']
                        question_to = const['question_to']
                        resp_discluded = const['responses_discluded']
                        router.survey_creation_controller.create_question_constraint_standard(question_from,response_from,const_type, question_to)
                    elif const_type == 'forbids':
                        question_from = const['question_from']
                        response_from = const['response_from']
                        question_to = const['question_to']
                        router.survey_creation_controller.create_disclusion_constraint(question_from, response_from,question_to, resp_discluded)
except KeyError:
    raise MalformedSurvey
