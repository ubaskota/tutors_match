CREATE TABLE login_signup(
	first_name varchar,
	last_name varchar,
	j_num varchar, 
	email varchar, 
	password varchar
	);



CREATE TABLE login_signup_tutor(
	first_name varchar,
	last_name varchar,
	j_num varchar,
	secretCode varchar,
	email varchar, 
	password varchar
	);



CREATE TABLE student_code(
	first_name varchar,
	last_name varchar,
	j_num varchar,
	uniqueCode varchar
	);


CREATE TABLE admin(
	first_name varchar,
	j_num varchar,
	password varchar
	);




INSERT INTO student_code VALUES ('Ujjwal', 'Baskota', 'J00787739', 'A334411');
INSERT INTO admin VALUES ('Ujjwal', 'J00787739', '12345');
INSERT INTO admin VALUES ('John', 'J00787738', '12345');
INSERT INTO admin VALUES ('Jack', 'J00787740', '12345');
INSERT INTO login_signup_tutor VALUES ('Ujjwal', 'Baskota', 'J00787739', 'A334411', 'ujjwal.baskota@gmail.com', '123456')
INSERT INTO login_signup_tutor VALUES ('Ujj', 'Baskota', 'J00787738', 'A334411', 'ujjwal.baskota@gmail.com', '123456')






SELECT secretcode, uniquecode FROM student_code JOIN login_signup_tutor ON student_code.uniquecode = login_signup_tutor.secretcode;