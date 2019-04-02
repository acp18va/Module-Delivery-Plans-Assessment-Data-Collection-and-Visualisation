DROP DATABASE mdp;

CREATE DATABASE mdp;

USE mdp;

-- List of users of webapp.
CREATE TABLE User (
	user_id int AUTO_INCREMENT,
	user_type ENUM('LTM', 'ACADEMIC', 'YEARTUTOR'),
	user_email char,
	user_password char,
	PRIMARY KEY (user_id),
	UNIQUE KEY unique_columns(user_email)
);

-- List of students.
CREATE TABLE Student (
	student_id int AUTO_INCREMENT,
	student_name char,
	PRIMARY KEY (student_id)
);

-- List of modules with their assigned academic.
CREATE TABLE Module (
	mod_id int AUTO_INCREMENT,
	mod_code char,
	mod_name char,
	mod_semester ENUM('FIRST', 'SECOND', 'BOTH'),
	mod_academic INT,
	PRIMARY KEY (mod_id),
	UNIQUE KEY unique_columns(mod_code, mod_semester)
);

-- List of assessments.
CREATE TABLE Assessment (
	ass_id int AUTO_INCREMENT,
	ass_format int,
	ass_name char,
	ass_marks FLOAT,
	ass_release_date DATETIME,
	ass_submit_date DATETIME,
	PRIMARY KEY (ass_id)
);

-- List of form created by LTM for each academic year.
CREATE TABLE Form (
  form_id int AUTO_INCREMENT,
  form_name char,
  form_state ENUM('CREATED', 'WAITING', 'DONE'),
  form_acad_year_start DATETIME,
  form_acad_year_end DATETIME,
  form_exam_period_start DATETIME,
  form_exam_period_end DATETIME,
	PRIMARY KEY (form_id)
);

-- List of entries in each form, one for each module.
CREATE TABLE FormEntry (
  entry_id int AUTO_INCREMENT,
  entry_module INT,
  entry_parent INT,
  entry_timestamp TIMESTAMP,
  entry_is_filled BOOLEAN,
	PRIMARY KEY (entry_id)
);

-- List of assessments for a module.
CREATE TABLE ModuleAssessments (
	ma_module int,
	ma_assessment int
);

-- List of modules each student is registered for.
CREATE TABLE StudentModules (
	sm_module int,
	sm_student int,
	PRIMARY KEY (sm_module,sm_student)
);

ALTER TABLE Module ADD CONSTRAINT Module_fk0 FOREIGN KEY (mod_academic) REFERENCES User(user_id);

ALTER TABLE FormEntry ADD CONSTRAINT FormEntry_fk0 FOREIGN KEY (entry_module) REFERENCES Module(mod_id);
ALTER TABLE FormEntry ADD CONSTRAINT FormEntry_fk1 FOREIGN KEY (entry_parent) REFERENCES Form(form_id);

ALTER TABLE StudentModules ADD CONSTRAINT StudentModule_fk0 FOREIGN KEY (sm_module) REFERENCES Module(mod_id);
ALTER TABLE StudentModules ADD CONSTRAINT StudentModule_fk1 FOREIGN KEY (sm_student) REFERENCES Student(student_id);

ALTER TABLE ModuleAssessments ADD CONSTRAINT ModuleAssessments_fk0 FOREIGN KEY (ma_module) REFERENCES Module(mod_id);
ALTER TABLE ModuleAssessments ADD CONSTRAINT ModuleAssessments_fk1 FOREIGN KEY (ma_assessment) REFERENCES Assessment(ass_id);
