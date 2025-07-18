CREATE DATABASE quiz_app;

USE quiz_app;

CREATE TABLE users(
	id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255)
);

CREATE TABLE quizzes(
	id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    description TEXT
);

CREATE TABLE questions(
	id INT PRIMARY KEY AUTO_INCREMENT,
    quiz_id INT,
	question TEXT,
	option_a TEXT,
	option_b TEXT,
	option_c TEXT,
	option_d TEXT,
	correct_ans CHAR(1),
	FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);

CREATE TABLE user_answers(
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT,
	question_id INT,
	selected_option CHAR(1),
	is_correct BOOLEAN,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO quizzes (title, description) VALUES
('Python Basics', 'A quiz on basic Python concepts.'),
('General Knowledge', 'Test your general knowledge.');

select * from questions;

ALTER TABLE user_answers
ADD quiz_id INT AFTER user_id;

SELECT * FROM questions WHERE quiz_id = 1;

SELECT * FROM user_answers;
SELECT * FROM users;
