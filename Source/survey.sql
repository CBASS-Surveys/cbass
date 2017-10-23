-- -*- mode: sql; sql-product: postgres -*-
-- Part of CBASS

INSERT INTO users (username, user_email, password_hash, password_salt) VALUES
       ('test', 'test@example.com', 'example', 'example');

INSERT INTO surveys (name, author) VALUES
       ('Study Habits Survey', currval(pg_get_serial_sequence('users', 'id'))) RETURNING id INTO currentSurvey.surveyID;

INSERT INTO survey_properties (survey_id, name, value) VALUES
       (currval(pg_get_serial_sequence('surveys', 'id')), 'before_text', 'A Survey to demonstrate the features of CBASS, from following a Survey Plan to applying survey constraints correctly.  This will survey the study habits of various respondants.'),
       (currval(pg_get_serial_sequence('surveys', 'id')), 'after_text', 'Thank you for participating.  Have a nice day.');

INSERT INTO survey_question (survey, question_text, question_type) VALUES
       (currval(pg_get_serial_sequence('surveys', 'id')), 'Are you male or female?', 'single-response');

INSERT INTO question_response (survey, question, value, description) VALUES
       (currval(pg_get_serial_sequence('surveys', 'id')), currval(pg_get_serial_sequence('survey_question', 'question_id')), 'm', 'Male'),
       (currval(pg_get_serial_sequence('surveys', 'id')), currval(pg_get_serial_sequence('survey_question', 'question_id')), 'f', 'Female'),
       (currval(pg_get_serial_sequence('surveys', 'id')), currval(pg_get_serial_sequence('survey_question', 'question_id')), 'n', 'Prefer Not to Answer');

INSERT INTO survey_properties (survey_id, name, value) VALUES
       (currval(pg_get_serial_sequence('surveys', 'id')), 'first_question', to_char(currval(pg_get_serial_sequence('survey_question', 'question_id')), '999'));

INSERT INTO survey_question (survey, question_text, question_type) VALUES
       (currval(pg_get_serial_sequence('survey_question', 'question_id')), 'What is your age?', 'single-response');

INSERT INTO question_response (survey, question, value, description) VALUES
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '18', '18'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '19', '19'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '20', '20'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '21', '21'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '22', '22'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '23', '23'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '24', '24'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '25', '25'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '26', '26'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '27', '27'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '28', '28'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '29', '29'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), '30', '30'),
       (currval(pg_get_serial_sequence('surveys', 'id'), currval(pg_get_serial_sequence('survey_question', 'question_id')), 'other', 'other');

