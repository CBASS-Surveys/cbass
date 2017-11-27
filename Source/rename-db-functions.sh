#!/bin/sh

sed -e 's/authenticateUser/authenticate_user/' \
    -e 's/createUser/create_user/' \
    -e 's/updatePassword/update_password/' \
    -e 's/createSurveyQuestionResponse/create_survey_question_response/' \
    -e 's/createSurveyQuestion/create_survey_question/' \
    -e 's/createSurvey/create_survey/' \
    -e 's/createQuestionConstraintStandard/create_question_constraint_standard/' \
    -e 's/createDisclusionConstraint/create_disclusion_constraint/' \
    -e 's/createSurveyResponse/create_survey_response/' \
    -e 's/insertSurveyQuestionResponse/insert_survey_question_response/' \
    -e 's/insertSurveyQuestionMultiResponse/insert_survey_question_multi_response/' \
    -e 's/insertSurveyQuestionLongFormResponse/insert_survey_question_long_form_response/' \
    -e 's/getConstraints/get_constraints/' \
    -e 's/getModifyConstraints/get_modify_constraints/' \
    -e 's/hasResponse/has_response/' \
    -e 's/getQuestion/get_question/' \
    -e 's/getResponsesToSurvey/get_responses_to_survey/' \
    -e 's/getResponses/get_responses/' \
    -e 's/getSurveyQuestions/get_survey_questions/' \
    -e 's/getSurveyProperties/get_survey_properties/' \
    -e 's/getSurveyName/get_survey_name/' \
    -e 's/getIndividualResponseToQuestion/get_individual_response_to_question/' \
    -e 's/changeQuestionText/change_question_text/' \
    -e 's/changeQuestionResponseDescription/change_question_response_description/' \
    -e 's/changeQuestionResponseValue/change_question_response_value/' \
    -e 's/createNewSurveyProperty/create_new_survey_property/' \
    -e 's/updateSurveyProperty/update_survey_property/' \
    -i $1
