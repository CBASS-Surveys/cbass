-- -*- mode: sql; sql-product: postgres -*-
-- Part of test

-- Begin Table users
CREATE TABLE IF NOT EXISTS users
(
        id SERIAL NOT NULL,
        username VARCHAR(64) NOT NULL UNIQUE,
        user_email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        password_salt VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
);
-- End Table users

-- Begin Table surveys
CREATE TABLE IF NOT EXISTS surveys
(
        id SERIAL NOT NULL,
        name VARCHAR(255) NOT NULL,
        author INTEGER REFERENCES users,
        PRIMARY KEY (id)
);
-- End Table surveys

-- Begin Table survey_properties
CREATE TABLE IF NOT EXISTS survey_properties
(
        survey_id INTEGER REFERENCES surveys NOT NULL,
        name VARCHAR(255) NOT NULL,
        value VARCHAR(1023) NOT NULL,
        PRIMARY KEY (survey_id, name)
);
-- End Table survey_properties

CREATE TYPE question_type AS ENUM ('single-response', 'free-response', 'multi-choice-response');

-- Begin Table survey_question
CREATE TABLE IF NOT EXISTS survey_question
(
        question_id SERIAL NOT NULL,
        survey INTEGER REFERENCES surveys (id),
        question_text VARCHAR(1023) NOT NULL,
        question_type question_type NOT NULL, 
        PRIMARY KEY (question_id)
);
-- End Table survey_question

-- Begin Table question_response
CREATE TABLE IF NOT EXISTS question_response
(
        id SERIAL NOT NULL,
        survey INTEGER REFERENCES surveys,
        question INTEGER REFERENCES survey_question,
        value VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
);
-- End Table question_response

CREATE TYPE constraint_type AS ENUM ('forbid', 'require');

-- Begin Table question_constraints
CREATE TABLE IF NOT EXISTS question_constraints
(
        id SERIAL NOT NULL,
        question_from INTEGER REFERENCES survey_question,
        response_from INTEGER REFERENCES question_response,
        type          constraint_type NOT NULL,
        question_affected INTEGER REFERENCES survey_question,
        PRIMARY KEY (ID)
);
-- End Table question_constraints

-- Begin Table question_constraint_modify
CREATE TABLE IF NOT EXISTS question_constraint_modify
(
        id SERIAL NOT NULL,
        question_from INTEGER REFERENCES survey_question NOT NULL,
        response_from INTEGER REFERENCES question_response NOT NULL,
        question_to INTEGER REFERENCES survey_question NOT NULL,
        responses_discluded INTEGER ARRAY,
        PRIMARY KEY (id),
        UNIQUE (question_from, response_from)
);
-- End Table question_constraint_modify

-- Begin Table survey_response
CREATE TABLE IF NOT EXISTS survey_response
(
        id SERIAL NOT NULL,
        survey INTEGER REFERENCES surveys(id),
        identifier_string varchar(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (survey, identifier_string)
);
-- End Table survey_response

-- Begin Table survey_response_entry
CREATE TABLE IF NOT EXISTS survey_response_entry
(
        response_id INTEGER REFERENCES survey_response,
        response_to INTEGER REFERENCES survey_question,
        response INTEGER REFERENCES question_response,
        PRIMARY KEY (response_id, response_to)
);
-- End Table survey_response_entry

-- Begin Table survey_long_form_response
CREATE TABLE IF NOT EXISTS survey_long_form_response
(
        response_id INTEGER REFERENCES survey_response,
        response_to INTEGER REFERENCES survey_question,
        response VARCHAR(1024) NOT NULL,
        PRIMARY KEY (response_id, response_to)
);
-- End Table survey_long_form_response

-- Begin Table survey_multi_response
CREATE TABLE IF NOT EXISTS survey_multi_response
(
        response_id INTEGER REFERENCES survey_response,
        response_to INTEGER REFERENCES survey_question,
        response INTEGER ARRAY NOT NULL,
        PRIMARY KEY (response_id, response_to)
);
-- End Table survey_multi_response

