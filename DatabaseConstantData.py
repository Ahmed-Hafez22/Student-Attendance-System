from libs import *

database_connection = connect("test.db")
database_cursor = database_connection.cursor()
# database_cursor.execute(
#     """
#                         CREATE TABLE IF NOT EXISTS DateTable(
#                             id INTEGER PRIMARY KEY,
#                             Date TEXT,
#                             Day TEXT
#                         )
#                         """
# )

# g1_4_courses_dict = {
#     "BS213": {
#         "Course Name": "Project Management",
#         "Day": "Saturday",
#         "End Time": "13:30",
#     },
#     "CF225": {
#         "Course Name": "Computer Architecture",
#         "Day": "Tuesday",
#         "End Time": "10:40"
#     },
#     "CF216" : {
#         "Course Name" : "Data Structure",
#         "Day" : "Tuesday",
#         "End Time" : "12:30"
#     }
# }

# database_cursor.execute(
#     """
#                         CREATE TABLE IF NOT EXISTS Group1Table(
#                         id INTEGER PRIMARY KEY,
#                         courses TEXT
#                         )
#                         """
# )


# database_cursor.execute(
#     "INSERT INTO Group1Table(courses) VALUES(?)",
#     (json.dumps(g1_4_courses_dict),),
# )

# database_cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS allStudents(
#         id INTEGER PRIMARY KEY,
#         AcademicID INTEGER,
#         name TEXT,
#         studentGroup INTEGERS,
#         registeredCourses TEXT,
#         attendance TEXT
#     )
# """
# )

# s1_109_dict = {"Course 1": "BS213", "Course 2": "CF225", "Course 3" : "CF216"}

# s2_118_dict = {"Course 1": "BS213", "Course 2": "CF225", "Course 3" : "CF216"}

# s3_103_dict = {"Course 1": "BS213", "Course 2": "CF225", "Course 3" : "CF216"}


# database_cursor.execute(
#     "INSERT INTO allStudents(AcademicID, name, studentGroup, registeredCourses) VALUES(?,?,?,?)",
#     (24030109, "Ahmed", 1, json.dumps(s1_109_dict)),
# )
# database_cursor.execute(
#     "INSERT INTO allStudents(AcademicID, name, studentGroup, registeredCourses) VALUES(?,?,?,?)",
#     (24030118, "Ibrahim", 1, json.dumps(s2_118_dict)),
# )

# database_cursor.execute(
#     "INSERT INTO allStudents(AcademicID, name, studentGroup, registeredCourses) VALUES(?,?,?,?)",
#     (24030103, "Elbatrek", 1, json.dumps(s3_103_dict)),
# )

# database_cursor.execute("UPDATE allStudents SET registeredCourses = ? WHERE AcademicID = ?" , (json.dumps(s2_118_dict), 24030118))

# courses = {"Course1" : "CF225", "Courses2" : "BS213"}

# database_cursor.execute("""CREATE TABLE IF NOT EXISTS collegeStaff(
#                         id INTEGER PRIMARY KEY,
#                         name TEXT,
#                         email TEXT,
#                         password TEXT,
#                         courses TEXT
#                         )""")

# database_cursor.execute("INSERT INTO collegeStaff(name, email, password, courses) VALUES('Ahmed', 'ahmed@gmail.com', '123', ?)", (json.dumps(courses),))
database_connection.commit()