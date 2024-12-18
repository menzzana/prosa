/* Test data */
INSERT INTO user(email,full_name,password) VALUES
	('user1@mail.com','Testuser 1','pass1');
INSERT INTO user(email,full_name,password) VALUES
	('user2@mail.com','Testuser 2','pass2');
INSERT INTO user(email,full_name,password) VALUES
	('user3@mail.com','Testuser 3','pass3');
INSERT INTO user(email,full_name,password) VALUES
	('user4@mail.com','Testuser 4','pass4');
INSERT INTO user(email,full_name,password) VALUES
	('user5@mail.com','Testuser 5','pass5');
INSERT INTO project(name,description) VALUES
	('First test project','This is the first test project');
INSERT INTO project(name,description) VALUES
	('second test project','This is another test project');
INSERT INTO project(name,description) VALUES
	('third test project','This is another test project');
INSERT INTO project(name,description) VALUES
	('forth test project1','This is another test project');
INSERT INTO project(name,description) VALUES
	('fifth test project','This is another test project');
INSERT INTO project(name,description) VALUES
	('Sixth test project','This is another test project');
INSERT INTO task(project_id,name,description,creation_date,due_date) VALUES
	(1,'My first task','This a milestone1','2024-11-17','2025-01-01');
INSERT INTO task(project_id,name,description,creation_date,due_date) VALUES
	(1,'My 2 task','This a milestone2','2024-11-17','2025-04-01');
INSERT INTO task(project_id,name,description,creation_date,due_date) VALUES
	(2,'My 3 task','This a milestone3','2024-11-17','2025-03-01');
INSERT INTO task(project_id,name,description,creation_date,due_date) VALUES
	(3,'My 4 task','This a milestone4','2024-11-17','2025-02-01');
INSERT INTO task_value(task_id,property_value_id) VALUES
	(4,10);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(1,11);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(3,2);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(4,13);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(2,4);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(3,7);
INSERT INTO task_value(task_id,property_value_id) VALUES
	(1,6);
INSERT INTO user_access(project_id,access_id,user_id) VALUES
	(3,3,3);
INSERT INTO user_access(project_id,access_id,user_id) VALUES
	(3,4,1);
INSERT INTO user_access(project_id,access_id,user_id) VALUES
	(3,5,2);
INSERT INTO user_access(project_id,access_id,user_id) VALUES
	(3,6,3);
INSERT INTO user_access(task_id,access_id,user_id) VALUES
	(2,4,4);
INSERT INTO user_access(task_id,access_id,user_id) VALUES
	(2,2,5);
INSERT INTO user_access(task_id,access_id,user_id) VALUES
	(4,3,2);
