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
CREATE TABLE tag (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL
	);
CREATE TABLE tagvalue (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tag_id INTEGER NOT NULL,
	name VARCHAR(255),
	UNIQUE(tag_id,name) ON CONFLICT ABORT
	);
CREATE TABLE task_tagvalue (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	task_id INTEGER,
	tagvalue_id INTEGER NOT NULL,
	UNIQUE(task_id,tagvalue_id) ON CONFLICT ABORT
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
	sort_tag_id INTEGER,
	sort_tag_order INTEGER,
	group_tag_id INTEGER,
	group_tag_order INTEGER,
	global_access INTEGER,
    name VARCHAR(40)
    );
CREATE TABLE task_property (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_view_id INTEGER NOT NULL,
	property_tag_id INTEGER
    );

/* Views */
CREATE VIEW get_project_users AS
	SELECT user_id,project.name AS project,user.full_name AS name,access.id AS useraccess
    FROM user,project,user_access,access
    WHERE user.id=user_access.user_id
    AND project.id=user_access.project_id
    AND access.id=user_access.access_id
	UNION
	SELECT user_id,project.name AS project,user.full_name AS name,access_id AS useraccess
    FROM user,project,user_access
    WHERE user.id=user_access.user_id
    AND user_access.access_id=1;

CREATE VIEW created_views AS
	SELECT DISTINCT tv.id,tv.name,tv.user_id,project_view,created_date_view,due_date_view,
		(SELECT name 
			FROM tag 
			WHERE tv.sort_tag_id=tag.id),
		sort_tag_order,
		(SELECT name 
			FROM tag 
			WHERE tv.group_tag_id=tag.id),
	group_tag_order,global_access,tag.name
	FROM task_view tv,task_property,tag
	WHERE tv.id=task_property.task_view_id
	AND task_property.property_tag_id=tag.id;

CREATE VIEW all_tasks AS
	SELECT DISTINCT project.name AS project,task.id AS taskid,task.name AS task,task.creation_date,task.due_date,tag.name AS tag,tagvalue.name AS tagvalue
	FROM project,task,tag,tagvalue,task_tagvalue
	WHERE tag.id=tagvalue.tag_id
	AND task_tagvalue.tagvalue_id=tagvalue.id
	AND task_tagvalue.task_id=task.id
	AND project.id=task.project_id;

CREATE VIEW all_tags AS
	SELECT DISTINCT tag.name AS tag,tagvalue.name AS tagvalue
	FROM tag,tagvalue
	WHERE tag.id=tagvalue.tag_id
	ORDER BY tag.id,tagvalue.id;
	
/*


CREATE VIEW get_view AS
	SELECT task_view.id,user_id,task_view.name,task_view.global_access,tagvalue.name,
	tag.name,task_view.sort_tag_order,task_view.group_tag_order
	FROM task_view,task_property,tag,tagvalue
	WHERE task_view.id=task_property.task_view_id
	AND task_property.task_view_id=tagvalue.id
	AND task_view.sort_tag_id=tag.id
	AND task_view.group_tag_id=tag.id;
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
INSERT INTO tag(id,name) VALUES
	(1,'Status');
INSERT INTO tagvalue(tag_id,name) VALUES
	(1,'');
INSERT INTO tagvalue(tag_id,name) VALUES
	(1,'ToDo');
INSERT INTO tagvalue(tag_id,name) VALUES
	(1,'Doing');
INSERT INTO tagvalue(tag_id,name) VALUES
	(1,'Done');
INSERT INTO tagvalue(tag_id,name) VALUES
	(1,'Struck');
INSERT INTO tag(id,name) VALUES
	(2,'Priority');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'On hold');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'Low');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'Moderate');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'High');
INSERT INTO tagvalue(tag_id,name) VALUES
	(2,'Critical');
INSERT INTO tag(id,name) VALUES
	(3,'Milestone');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'MS1');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'MS2');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'MS3');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'MS4');
INSERT INTO tagvalue(tag_id,name) VALUES
	(3,'MS5');
INSERT INTO task_view(user_id,sort_tag_id,sort_tag_order,group_tag_id,group_tag_order,global_access,name) VALUES
	(1,1,1,2,0,1,'All');
INSERT INTO task_property(task_view_id,property_tag_id) VALUES
	(1,1);
INSERT INTO task_property(task_view_id,property_tag_id) VALUES
	(1,2);
INSERT INTO task_property(task_view_id,property_tag_id) VALUES
	(1,3);
INSERT INTO task_property(task_view_id,property_tag_id) VALUES
	(1,4);
