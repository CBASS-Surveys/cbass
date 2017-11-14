-- -*- mode: sql; sql-product: postgres -*-
-- Part of CBASS

----------------------------------------------------------------
-- Note!  This file must be inserted into an empty database!! --
----------------------------------------------------------------

-- Inserts user test, password fooBar
INSERT INTO users (id, username, user_email, password_hash, password_salt) VALUES
       (1, 'test', 'test@example.net', '6ead55ed0b622d11ebd6120d7c849080467acd139774dff8d568255e0adaddff', '7614cc80b221c38797cc82cf2ee3ec5a0d47c35233f91400ce0594e97652ccbf');

-- Create a test survey, number 1
INSERT INTO surveys (id, name, author) VALUES
       (1, 'Test Survey', 1);

-- Add some basic test properties
INSERT INTO survey_properties (survey_id, name, value) VALUES
       (1, 'before_text', 'Test Text Before'),
       (1, 'after_text', 'Test After Text');

-- Define a few questions
INSERT INTO survey_question (question_id, survey, question_text, question_type) VALUES
       (1, 1, 'Single Response 1', 'single-response'),
       (2, 1, 'Multi Response 1', 'multi-choice-response'),
       (3, 1, 'Free Response 1', 'free-response'),
       (4, 1, 'Single Response 2', 'single-response'),
       (5, 1, 'Multi Response 2', 'multi-choice-response'),
       (6, 1, 'Free Response 2', 'free-response');

-- Define some responses for the various questions
INSERT INTO question_response (id, survey, question, value, description) VALUES
       -- Question 1
       (1, 1, 1, 'foo', 'Foo'),
       (2, 1, 1, 'barfoo', 'Bar'),
       -- Question 2
       (3, 1, 2, 'blahfoo', 'blah'),
       (4, 1, 2, 'tweetfoo', 'moo'),
       (5, 1, 2, 'bazfoo', 'quux'),
       -- Question 4
       (6, 1, 4, 'moo', 'Cow'),
       (7, 1, 4, 'blue', 'green'),
       (8, 1, 4, 'orange', 'Blue'),
       (9, 1, 4, 'blab', 'Moo'),
       -- Question 5
       (10, 1, 5, 'zippidy', 'doo-dah'),
       (11, 1, 5, 'zippity', 'hey'),
       (12, 1, 5, 'my', 'oh my'),
       (13, 1, 5, 'what', 'a wonderful day');

-- Add some basic constraints
INSERT INTO question_constraints (question_from, response_from, type, question_affected) VALUES
       (1, 1, 'require', 3),    -- If question one has answer Foo, Ask question 3
       (1, 2, 'forbid', 3);     -- If question one has answer Bar, Don't ask question 3

-- And add some modification constraints
INSERT INTO question_constraint_modify (question_from, response_from, question_to, responses_discluded) VALUES
       (1, 2, 4, '{5, 6}'),     -- If question one has answer Bar, remove Cow and green from question 4
       (2, 4, 5, '{10, 11}');   -- If question two has answer blah, remove doo-dah and hey from question 5

-- Add some actual test data
INSERT INTO survey_response (survey, identifier_string) VALUES
       (1, 'a849c7d14099380f2905f643c678b87b');

INSERT INTO survey_response_entry (response_id, response_to, response) VALUES
       (1, 1, 1),
       (1, 4, 6);

INSERT INTO survey_multi_response (response_id, response_to, response) VALUES
       (1, 2, '{3, 4}'),
       (1, 5, '{12, 13}');

INSERT INTO survey_long_form_response (response_id, response_to, response) VALUES
       (1, 6, 'fooo');
