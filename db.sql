/* Table creation */
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(45) UNIQUE NOT NULL,
	full_name VARCHAR(45) NOT NULL,
    salt VARCHAR(6) UNIQUE,
	password VARCHAR(45) NOT NULL,
	session_id VARCHAR(45),
	session_time VARCHAR(20)
	);
CREATE TABLE access (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL
	);
CREATE TABLE project (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(4000) NOT NULL
	);
CREATE TABLE task (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
	name VARCHAR(40) NOT NULL,
	description VARCHAR(255),
	creation_date DATE NOT NULL,
	due_date DATE
    );
CREATE TABLE property (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL
	);
CREATE TABLE property_value (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	property_id INTEGER NOT NULL,
	order INTEGER UNIQUE NOT NULL,
	name VARCHAR(255),
	UNIQUE(property_id,name) ON CONFLICT ABORT
	);
CREATE TABLE task_value (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	task_id INTEGER,
	property_value_id INTEGER NOT NULL,
	UNIQUE(task_id,property_value_id) ON CONFLICT ABORT
	);
CREATE TABLE user_access (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    access_id INTEGER NOT NULL,
    project_id INTEGER,
    task_id INTEGER
	);
CREATE TABLE task_view (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
	sort_property_id INTEGER,
	group_property_id INTEGER,
	global_access INTEGER,
    name VARCHAR(40)
    );
CREATE TABLE view_property (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_view_id INTEGER NOT NULL,
	property_id INTEGER
    );

/* Views */
CREATE VIEW get_project_users AS
	SELECT user.id AS user_id,project.name AS project,user.full_name AS name,access.id AS useraccess
	FROM user
	LEFT JOIN user_access ON user_access.user_id=user.id
	LEFT JOIN project ON project.id = user_access.project_id
	LEFT JOIN access ON user_access.access_id=access.id;

CREATE VIEW all_tasks AS
	SELECT DISTINCT project.name AS 'Project',task.id AS taskid,task.name AS 'Task',
		task.creation_date as 'Creation date',task.due_date AS 'Due date',
		COALESCE(user.full_name,'') AS 'Name',COALESCE(access.name,'') AS 'Access',
		property.name AS property,COALESCE(property_value.name,'') AS property_value
	FROM project,task
	LEFT JOIN task_value ON task_value.task_id = task.id
	LEFT JOIN property_value ON task_value.property_value_id = property_value.id
	LEFT JOIN property ON property.id = property_value.property_id
	LEFT JOIN user_access ON user_access.task_id = task.id
	LEFT JOIN user ON user.id = user_access.user_id
	LEFT JOIN access ON access.id = user_access.access_id
	WHERE project.id=task.project_id;

CREATE VIEW created_views AS
	SELECT task_view.id,user.id AS user_id, global_access, name
	FROM user,task_view
	WHERE user.id=task_view.user_id;

CREATE VIEW all_properties AS
	SELECT DISTINCT property.name AS property,property_value.name AS property_value
	FROM property,property_value
	WHERE property.id=property_value.property_id
	ORDER BY property.id,property_value.id;

/*


CREATE VIEW created_views AS
	SELECT DISTINCT tv.id,tv.name,tv.user_id,project_view,created_date_view,due_date_view,
		(SELECT name 
			FROM property 
			WHERE tv.sort_property_id=property.id),
		sort_property_order,
		(SELECT name 
			FROM property 
			WHERE tv.group_property_id=property.id),
	group_property_order,global_access,property.name
	FROM task_view tv,task_property,property
	WHERE tv.id=task_property.task_view_id
	AND task_property.property_property_id=property.id;


CREATE VIEW get_view AS
	SELECT task_view.id,user_id,task_view.name,task_view.global_access,property_value.name,
	property.name,task_view.sort_property_order,task_view.group_property_order
	FROM task_view,task_property,property,property_value
	WHERE task_view.id=task_property.task_view_id
	AND task_property.task_view_id=property_value.id
	AND task_view.sort_property_id=property.id
	AND task_view.group_property_id=property.id;
*/

/* Inserts */
INSERT INTO access(id,name) VALUES
	(1,'Administrator');
INSERT INTO access(id,name) VALUES
	(2,'Project leader');
INSERT INTO access(id,name) VALUES
	(3,'Project advisor');
INSERT INTO access(id,name) VALUES
	(4,'Project owner');
INSERT INTO access(id,name) VALUES
	(5,'Developer');
INSERT INTO access(id,name) VALUES
	(6,'viewer');
INSERT INTO property(id,name) VALUES
	(1,'Status');
INSERT INTO property_value(property_id,name) VALUES
	(1,'ToDo');
INSERT INTO property_value(property_id,name) VALUES
	(1,'Doing');
INSERT INTO property_value(property_id,name) VALUES
	(1,'Done');
INSERT INTO property_value(property_id,name) VALUES
	(1,'Struck');
INSERT INTO property(id,name) VALUES
	(2,'Priority');
INSERT INTO property_value(property_id,name) VALUES
	(2,'On hold');
INSERT INTO property_value(property_id,name) VALUES
	(2,'Low');
INSERT INTO property_value(property_id,name) VALUES
	(2,'Moderate');
INSERT INTO property_value(property_id,name) VALUES
	(2,'High');
INSERT INTO property_value(property_id,name) VALUES
	(2,'Critical');
INSERT INTO property(id,name) VALUES
	(3,'Milestone');
INSERT INTO property_value(property_id,name) VALUES
	(3,'MS1');
INSERT INTO property_value(property_id,name) VALUES
	(3,'MS2');
INSERT INTO property_value(property_id,name) VALUES
	(3,'MS3');
INSERT INTO property_value(property_id,name) VALUES
	(3,'MS4');
INSERT INTO property_value(property_id,name) VALUES
	(3,'MS5');
