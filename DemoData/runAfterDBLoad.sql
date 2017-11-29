-- -*- mode: sql; sql-product: postgres -*-
-- Part of cbass

select setval('survey_response_id_seq', (select max(id) from survey_response));
select setval('users_id_seq', (select max(id) from users));
select setval('surveys_id_seq', (select max(id) from surveys));
select setval('question_constraints_id_seq', (select max(id) from question_constraints));
select setval('survey_question_question_id_seq', (select max(question_id) from survey_question));
select setval('question_response_id_seq', (select max(id) from question_response));
select setval('question_constraint_modify_id_seq', (select max(id) from question_constraint_modify));
