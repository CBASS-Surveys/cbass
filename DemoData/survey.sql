-- -*- mode: sql; sql-product: postgres -*-
-- Part of CBASS_Demo


INSERT INTO users (id, username, user_email, password_hash, password_salt) VALUES
       (1, 'internal', 'test@example.net', 'example', 'example'),
       (2, 'test', 'test@example.com', 'example', 'example');

INSERT INTO surveys (id, name, author) VALUES
       (1, 'Dummy Survey', 1),
       (2, 'Study Habits Survey', 1);

INSERT INTO survey_properties (survey_id, name, value) VALUES
       (2, 'before_text', 'A Survey to demonstrate the features of CBASS, from following a Survey Plan to applying survey constraints correctly.  This will survey the study habits of various respondants.'),
       (2, 'after_text', 'Thank you for participating.  Have a nice day.');

INSERT INTO survey_question (question_id, survey, question_text, question_type) VALUES
       (0, 1, 'End Survey', 'single-response'),
       (1, 2, 'Are you male or female?', 'single-response'),
       (2, 2, 'What is your age?', 'single-response'),
       (3, 2, 'Where do you attend college?', 'single-response'),
       (4, 2, 'What category is your primary major in?', 'single-response'),
       (5, 2, 'Where do you live?', 'single-response'),
       (6, 2, 'How many credit hours are you taking?', 'single-response'),
       (7, 2, 'On average, how much time do you spend studying in a week?', 'single-response'),
       (8, 2, 'Of this time, how much do you spend studying in your living area?', 'single-response'),
       (9, 2, 'Of this time, how much do you spend studying on campus?', 'single-response'),
       (10, 2, 'Of this time, how much do you spend studying off campus?', 'single-response'),
       (11, 2, 'Where is you favorite place to study?', 'single-response'),
       (12, 2, 'If the place where you spend the majority of your time studying and your favorite place to study are not the same, why?', 'multi-choice-response'),
       (13, 2, 'Please explain what you mean by selecting "Lacks desired comfort".', 'free-response'),
       (14, 2, 'If there was a space dedicated to studying, would you use it?', 'single-response'),
       (15, 2, 'Do you use the UNL Learning Commons to study?', 'single-response'),
       (16, 2, 'Are there any specific things that you have found improve your ability to study?', 'free-response');


INSERT INTO question_response (id, survey, question, value, description) VALUES
       -- Dummy Responses
       (0, 1, 0, 'end', 'end'),
       -- Question 1
       (1, 2, 1, 'm', 'Male'),
       (2, 2, 1, 'f', 'Female'),
       (3, 2, 1, 'n', 'Prefer not to answer'),
       -- Question 2
       (4, 2, 2, '18', '18'),
       (5, 2, 2, '19', '19'),
       (6, 2, 2, '20', '20'),
       (7, 2, 2, '21', '21'),
       (8, 2, 2, '22', '22'),
       (9, 2, 2, '23', '23'),
       (10, 2, 2, '24', '24'),
       (11, 2, 2, '25', '25'),
       (12, 2, 2, '26', '26'),
       (13, 2, 2, '27', '27'),
       (14, 2, 2, '28', '28'),
       (15, 2, 2, '29', '29'),
       (16, 2, 2, '30', '30'),
       (17, 2, 2, 'other', 'Other'),
       -- Question 3
       (18, 2, 3, 'unl', 'UNL'),
       (19, 2, 3, 'unk', 'UNK'),
       (20, 2, 3, 'uno', 'UNO'),
       (21, 2, 3, 'neb', 'Other institution in Nebraska'),
       (22, 2, 3, 'other', 'Other institution'),
       (23, 2, 3, 'not-enrolled', 'Not currently enrolled'),
       -- Question 4
       (24, 2, 4, 'eng', 'Engineering'),
       (25, 2, 4, 'ag-sci', 'Agricultural Sciences'),
       (26, 2, 4, 'phys-sci', 'Physical Sciences'),
       (27, 2, 4, 'lib-art', 'Liberal Arts'),
       (28, 2, 4, 'mat-sci', 'Mathematical Sciences'),
       (29, 2, 4, 'fin-art', 'Fine Arts'),
       -- Question 5
       (30, 2, 5, 'on-campus', 'On Campus'),
       (31, 2, 5, 'off-campus', 'Off Campus'),
       -- Question 6
       (32, 2, 6, 'lt9', 'Less than 9'),
       (33, 2, 6, '9to15', '9 to 15'),
       (34, 2, 6, '16to21', '16 to 21'),
       (35, 2, 6, 'gt21', '22 or more'), 
       -- Question 7
       (36, 2, 7, 'lte5', '5 or less'),
       (37, 2, 7, '6to10', '6 to 10'),
       (38, 2, 7, '11to15', '11 to 15'),
       (39, 2, 7, '16to20', '16 to 20'),
       (40, 2, 7, 'gt20', 'More than 20'),
       -- Question 8
       (41, 2, 8, 'none', 'None of it'),
       (42, 2, 8, 'some', 'Some of it'),
       (43, 2, 8, 'most', 'Most of it'),
       (44, 2, 8, 'all', 'Nearly all of it'),
       -- Question 9
       (45, 2, 9, 'none', 'None of it'),
       (46, 2, 9, 'some', 'Some of it'),
       (47, 2, 9, 'most', 'Most of it'),
       (48, 2, 9, 'all', 'Nearly all of it'),
       -- Question 10
       (49, 2, 10, 'none', 'None of it'),
       (50, 2, 10, 'some', 'Some of it'),
       (51, 2, 10, 'most', 'Most of it'),
       (52, 2, 10, 'all', 'Nearly all of it'),
       -- Question 11
       (53, 2, 11, 'room', 'Room/Apartment/Dorm'),
       (54, 2, 11, 'library', 'Library'),
       (55, 2, 11, 'dept-build', 'Department Building'),
       (56, 2, 11, 'campus', 'Other Campus Building'),
       (57, 2, 11, 'off-campus', 'Coffee Shop/Restaurant/Business'),
       (58, 2, 11, 'outdoors', 'Outside/Park'),
       (59, 2, 11, 'outher', 'Other'),
       -- Question 12
       (60, 2, 12, 'na', 'Not Applicable'),
       (61, 2, 12, 'distractions', 'Distractions'),
       (62, 2, 12, 'loud', 'Too Loud'),
       (63, 2, 12, 'quiet', 'Too Quiet'),
       (64, 2, 12, 'room', 'No Room'),
       (65, 2, 12, 'distance', 'Too Far Away'),
       (66, 2, 12, 'tools', 'Insufficient Tools (no computer, whiteboard, etc.)'),
       (67, 2, 12, 'comfort', 'Location is Uncomfortable (distant bathrooms, uncomfortable furniture, etc.)'),
       (68, 2, 12, 'other', 'Other'),
       -- Question 14
       (69, 2, 14, 'yes', 'Yes'),
       (70, 2, 14, 'no', 'No'),
       (71, 2, 14, 'maybe', 'Maybe'),
       -- Question 15
       (72, 2, 15, 'often', 'Often'),
       (73, 2, 15, 'sometimes', 'Sometimes'),
       (74, 2, 15, 'rarely', 'Rarely'),
       (75, 2, 15, 'never', 'Never');

INSERT INTO question_constraints (question_from, response_from, type, question_affected) VALUES
       (2, 17, 'require', 0),
       (3, 18, 'forbid', 14),
       (3, 18, 'require', 15),
       (3, 22, 'require', 0),
       (3, 23, 'require', 0),
       (5, 30, 'forbid', 9),
       (6, 31, 'forbid', 10),
       (12, 67, 'require', 13);

INSERT INTO question_constraint_modify (question_from, response_from, question_to, responses_discluded) VALUES
       (8, 43, 9, '{47, 48}'),
       (8, 44, 9, '{47, 48}'),
       (8, 43, 10, '{51, 52}'),
       (8, 44, 10, '{51, 52}');
