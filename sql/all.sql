CREATE TABLE course_info (
	course_id varchar(30),			# 课程ID，人为构成
	course_term varchar(20),		# 课程学期
	course_name varchar(255),		# 课程名
	course_for_student varchar(20),	# 开课对象的年级
	course_teacher varchar(100),	# 开课老师

	PRIMARY KEY (course_id)
) default charset=utf8;


CREATE TABLE course_schedule (
	course_id varchar(30),			# 课程ID
	course_start_week int,			# 第几周开始
	course_end_week int,			# 第几周结束
	course_date int,				# 周几
	course_start_lesson int,		# 第几节开始
	course_end_lesson int,			# 第几节结束
	course_type int,				# 单双周，0-全，1-单，2-双
	course_place varchar(255),		# 上课地点

	PRIMARY KEY (course_id, course_date, course_start_lesson, course_end_lesson),
	FOREIGN KEY (course_id) REFERENCES course_info(course_id)
) default charset=utf8;


CREATE TABLE exam_schedule (
	exam_term varchar(100),			# 考试学期
	exam_campus varchar(100),		# 考试校区
	exam_place varchar(100),		# 考试地点
	exam_date int,					# 考试日期，格式组织为 YYYY-MM-DD
	exam_time int					# 考试时间，上午（0），下午（1），晚上（2）
) default charset=utf8;