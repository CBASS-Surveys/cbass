-- -*- mode: sql; sql-product: postgres -*-
-- Part of CBASS_Demo


INSERT INTO users (id, username, user_email, password_hash, password_salt) VALUE
       (0, 'test', 'test@example.com', 'example', 'example'),
       (1, 'test', 'test@example.com', 'example', 'example');

INSERT INTO surveys (id, name, author) VALUES
       (0, 'Dummy Survey', 0),
       (1, 'Study Habits Survey', 1);

INSERT INTO survey_question (id, survey, question_text, question_type) VALUES
       (0, 0, 'End Survey', 'single-response'),
       (1, 1, 'Are you male or female?', 'single-response'),
       (2, 1, 'What is your age?', 'single-response'),
       (3, 1, 'Where do you attend college?', 'single-response'),
       (4, 1, 'What category is your primary major in?', 'single-response'),
       (5, 1, 'Where do you live?', 'single-response'),
       (6, 1, 'How many credit hours are you taking?', 'single-response'),
       (7, 1, 'On average, how much time do you spend studying in a week?', 'single-response'),
       (8, 1, 'Of this time, how much do you spend studying in your living area?', 'single-response'),
       (9, 1, 'Of this time, how much do you spend studying on campus?', 'single-response'),
       (10, 1, 'Of this time, how much do you spend studying off campus?', 'single-response'),
       (11, 1, 'Where is you favorite place to study?', 'single-response'),
       (12, 1, 'If the place where you spend the majority of your time studying and your favorite place to study are not the same, why?', 'multi-choice-response'),
       (13, 1, 'Please explain what you mean by selecting "Lacks desired comfort".', 'free-response'),
       (14, 1, 'If there was a space dedicated to studying, would you use it?', 'single-response'),
       (15, 1, 'Do you use the UNL Learning Commons to study?', 'single-response'),
       (16, 1, 'Are there any specific things that you hav found improve your ability to study?', 'free-response');


INSERT INTO question_response (id, survey, question, value, description) VALUES
       -- Dummy Responses
       (0, 0, 0, 'end', 'end'),
       -- Question 1
       (1, 1, 1, 'm', 'Male'),
       (2, 1, 1, 'f', 'Female'),
       (3, 1, 1, 'n', 'Prefer not to answer'),
       -- Question 2
       (4, 1, 2, '18', '18'),
       (5, 1, 2, '19', '19'),
       (6, 1, 2, '20', '20'),
       (7, 1, 2, '21', '21'),
       (8, 1, 2, '22', '22'),
       (9, 1, 2, '23', '23'),
       (10, 1, 2, '24', '24'),
       (11, 1, 2, '25', '25'),
       (12, 1, 2, '26', '26'),
       (13, 1, 2, '27', '27'),
       (14, 1, 2, '28', '28'),
       (15, 1, 2, '29', '29'),
       (16, 1, 2, '30', '30'),
       (17, 1, 2, 'other', 'Other'),
       -- Question 3
       (18, 1, 3, 'unl', 'UNL'),
       (19, 1, 3, 'unk', 'UNK'),
       (20, 1, 3, 'uno', 'UNO'),
       (21, 1, 3, 'neb', 'Other institution in Nebraska'),
       (22, 1, 3. 'other', 'Other institution'),
       (23, 1, 3, 'not-enrolled', 'Not currently enrolled'),
       -- Question 4
       (24, 1, 4, 'eng', 'Engineering'),
       (25, 1, 4, 'ag-sci', 'Agricultural Sciences'),
       (26, 1, 4, 'phys-sci', 'Physical Sciences'),
       (27, 1, 4, 'lib-art', 'Liberal Arts'),
       (28, 1, 4, 'mat-sci', 'Mathematical Sciences'),
       (29, 1, 4, 'fin-art', 'Fine Arts'),
       -- Question 5
       (30, 1, 5, 'on-campus', 'On Campus'),
       (31, 1, 5, 'off-campus', 'Off Campus'),
       -- Question 6
       (32, 1, 6, 'lt9', 'Less than 9'),
       (33, 1, 6, '9to15', '9 to 15'),
       (34, 1, 6, '16to21', '16 to 21'),
       (35, 1, 6, 'gt21', '22 or more'), 
       -- Question 7
       (36, 1, 7, 'lte5', '5 or less'),
       (37, 1, 7, '6to10', '6 to 10'),
       (38, 1, 7, '11to15', '11 to 15'),
       (39, 1, 7, '16to20', '16 to 20'),
       (40, 1, 7, 'gt20', 'More than 20'),
       -- Question 8
       (41, 1, 8, 'none', 'None of it'),
       (42, 1, 8, 'some', 'Some of it'),
       (43, 1, 8, 'most', 'Most of it'),
       (44, 1, 8, 'all', 'Nearly all of it'),
       -- Question 9
       (45, 1, 9, 'none', 'None of it'),
       (46, 1, 9, 'some', 'Some of it'),
       (47, 1, 9, 'most', 'Most of it'),
       (48, 1, 9, 'all', 'Nearly all of it'),
       -- Question 10
       (49, 1, 10, 'none', 'None of it'),
       (50, 1, 10, 'some', 'Some of it'),
       (51, 1, 10, 'most', 'Most of it'),
       (52, 1, 10, 'all', 'Nearly all of it'),
       -- Question 11
       (53, 1, 11, 'room', 'Room/Apartment/Dorm'),
       (54, 1, 11, 'library', 'Library'),
       (55, 1, 11, 'dept-build', 'Department Building'),
       (56, 1, 11, 'campus', 'Other Campus Building'),
       (57, 1, 11, 'off-campus', 'Coffee Shop/Restaurant/Business'),
       (58, 1, 11, 'outdoors', 'Outside/Park'),
       (59, 1, 11, 'outher', 'Other'),
       -- Question 12
       (60, 1, 12, 'na', 'Not Applicable'),
       (61, 1, 12, 'distractions', 'Distractions'),
       (62, 1, 12, 'loud', 'Too Loud'),
       (63, 1, 12, 'quiet', 'Too Quiet'),
       (64, 1, 12, 'room', 'No Room'),
       (65, 1, 12, 'distance', 'Too Far Away'),
       (66, 1, 12, 'tools', 'Insufficient Tools (no computer, whiteboard, etc.)'),
       (67, 1, 12, 'comfort', 'Location is Uncomfortable (distant bathrooms, uncomfortable furniture, etc.)'),
       (68, 1, 12, 'other', 'Other'),
       -- Question 14
       (69, 1, 14, 'yes', 'Yes'),
       (70, 1, 14, 'no', 'No'),
       (71, 1, 14, 'maybe', 'Maybe'),
       -- Question 15
       (72, 1, 15, 'often', 'Often'),
       (73, 1, 15, 'sometimes', 'Sometimes'),
       (74, 1, 15, 'rarely', 'Rarely'),
       (75, 1, 15, 'never', 'Never');

INSERT INTO question_constraints (question_from, response_from, type, question_affected) VALUES
       (2, 17, 'require', 0),
       (3, 18, 'forbid', 14),
       (3, 18, 'require', 15)
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
