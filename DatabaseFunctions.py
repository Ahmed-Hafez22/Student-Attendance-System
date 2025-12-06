from libs import *
from DatabaseConstantData import *


def insert_date():
    today_date = database_cursor.execute("SELECT date('now')").fetchone()[0]
    today_day = datetime.strptime(today_date, "%Y-%m-%d").strftime("%A")
    information = database_cursor.execute(
        "SELECT Date, Day FROM DateTable WHERE id = (SELECT MAX (id) FROM DateTable)"
    ).fetchone()
    if information:
        if today_date == information[0] and today_day == information[1]:
            pass
        else:
            database_cursor.execute(
                "INSERT INTO DateTable(Date, Day) VALUES(?, ?)", [today_date, today_day]
            )
    else:
        database_cursor.execute(
            "INSERT INTO DateTable(Date, Day) VALUES(?, ?)", [today_date, today_day]
        )
    database_connection.commit()


def make_attendance_dict():
    row_count = database_cursor.execute("SELECT COUNT(*) FROM allStudents").fetchone()[
        0
    ]
    for row in range(row_count):
        select_query = "SELECT attendance FROM allStudents WHERE id = ?"
        flag = database_cursor.execute(select_query, ((row + 1),)).fetchone()[0]
        if flag == None:
            courses_JSON = database_cursor.execute(
                "SELECT registeredCourses FROM allStudents WHERE id = ?", ((row + 1),)
            ).fetchone()[0]
            courses_dict = json.loads(courses_JSON)
            attendance = {}
            for course in courses_dict.values():
                attendance[course] = {}
                update_query = "UPDATE allStudents SET attendance = ? WHERE id = ?"
                database_cursor.execute(update_query, (json.dumps(attendance) , (row+1)))
    database_connection.commit()


def take_attendance(scannedID):
    def getPotentialCourses(courses):
        courseLst = []
        for course_code in courses:
            if today_info[0] == courses[course_code]["Day"]:
                courseLst.append(course_code)
            else:
                pass
        return courseLst

    def check_if_student_registered_course(courses):
        for course in courses:
            for g1_course in courses_dict:
                if course == g1_course:
                    return True
                else:
                    continue
        return False

    def getCurrentCourse(courses, potCourse):
        course_time_str = []
        for course_code in potCourse:
            course_time_str.append(courses[course_code]["End Time"])

        course_time_obj = []
        for time in course_time_str:
            course_time_obj.append(
                datetime.strptime(time, "%H:%M").replace(
                    year=date_obj.year, month=date_obj.month, day=date_obj.day
                )
            )
        
        currentCourseInfo = []
        for time_obj in course_time_obj:
            gap = timedelta(minutes=15)
            time_difference = time_obj - current_time_obj
            if time_difference <= gap and time_difference > timedelta(days=0):
                if(time_obj == course_time_obj[0]):
                    currentCourseInfo.append(potCourse[0])
                    currentCourseInfo.append(time_obj)
                else:
                    currentCourseInfo.append(potCourse[1])  
                    currentCourseInfo.append(time_obj)
            else:
                continue
        return currentCourseInfo

    today_info = database_cursor.execute(
        """
                                        SELECT Day, Date
                                        FROM DateTable
                                        WHERE id = (SELECT MAX(id) FROM DateTable)
                                    """
    ).fetchone()

    date_obj = datetime.strptime(today_info[1], "%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    print(f"Current Time: {current_time}")
    current_time_obj = datetime.strptime(current_time, "%H:%M").replace(
        year=date_obj.year, month=date_obj.month, day=date_obj.day
    )

    allStudents = database_cursor.execute(
        "SELECT AcademicID, studentGroup FROM allStudents"
    ).fetchall()
    for student in allStudents:
        if student[1] == 1:
            courses_JSON = database_cursor.execute(
                "SELECT courses FROM Group1Table"
            ).fetchone()[0]
            courses_dict = json.loads(courses_JSON)

        potentialCourses = getPotentialCourses(courses_dict)
        currentCourseInfo = getCurrentCourse(courses_dict, potentialCourses)

        today_course = currentCourseInfo[0]
        course_time_obj = currentCourseInfo[1]

        studentCourses_JSON = database_cursor.execute(
            "SELECT registeredCourses FROM allStudents WHERE AcademicID = ?",
            (student[0],),
        ).fetchone()[0]
        studentCourses_dict = json.loads(studentCourses_JSON)
        attendance_JSON = database_cursor.execute(
            "SELECT attendance FROM allStudents WHERE AcademicID = ?", (student[0],)
        ).fetchone()[0]
        attendanceDict = json.loads(attendance_JSON)
        for course in studentCourses_dict.values():
            if today_info[1] not in attendanceDict[today_course]:
                attendanceDict[today_course][today_info[1]] = False
                database_cursor.execute(
                    "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                    (json.dumps(attendanceDict), student[0]),
                )
            else:
                continue
    database_connection.commit()

    student_ID = scannedID
    if student_ID:

        student_group = database_cursor.execute(
            """
                                                SELECT studentGroup
                                                FROM allStudents
                                                WHERE AcademicID = ?
                                                """,
            (student_ID,),
        ).fetchone()[0]

        if student_group == 1:
            courses_JSON = database_cursor.execute(
                "SELECT courses FROM Group1Table"
            ).fetchone()[0]
            courses_dict = json.loads(courses_JSON)


        time_difference = course_time_obj - current_time_obj
        MAX_GAP = timedelta(minutes=15)
        MIN_GAP = timedelta(minutes=0)

        if time_difference <= MAX_GAP and time_difference > MIN_GAP:
            studentCourses_Json = database_cursor.execute(
                """
                                                    SELECT registeredCourses
                                                    FROM allStudents
                                                    WHERE AcademicID = ?
                                                    """,
                (student_ID,),
            ).fetchone()[0]
            studentCourses_dict = json.loads(studentCourses_Json)

            greenLight = check_if_student_registered_course(
                studentCourses_dict.values()
            )
            if greenLight == True:
                attendance_JSON_query = (
                    "SELECT attendance FROM allStudents WHERE AcademicID = ?"
                )
                attendance_JSON = database_cursor.execute(
                    attendance_JSON_query, (student_ID,)
                ).fetchone()[0]
                studentsDict = json.loads(attendance_JSON)
                for course in studentCourses_dict.values():
                    if today_course == course:
                        studentsDict[today_course][today_info[1]] = True
                        database_cursor.execute(
                            "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                            (json.dumps(studentsDict), student_ID),
                        )
    database_connection.commit()


def make_excuse(studentID, courseCode, date):
    studentAttendanceJSON = database_cursor.execute("SELECT attendance FROM allStudents WHERE AcademicID = ?" , (studentID,)).fetchone()[0]
    studentAttendanceDict = json.loads(studentAttendanceJSON)

    if courseCode in studentAttendanceDict:
        studentAttendanceDict[courseCode][date] = True
    else:
        print(f"Student isn't enrolled in: {courseCode}")

    database_cursor.execute("UPDATE allStudents SET attendance = ? WHERE AcademicID = ?", (json.dumps(studentAttendanceDict) , studentID))
    database_connection.commit()

def getStudentInfo(studentID, courseCode):
    studentInfo = database_cursor.execute("SELECT AcademicID, name, studentGroup, registeredCourses, attendance FROM allStudents WHERE AcademicID = ?", (studentID,)).fetchone()

    studentAttendance = json.loads(studentInfo[4])
    studentregisteredCourses = json.loads(studentInfo[3])

    print(f"Student name: {studentInfo[1]}")
    print(f"Student ID: {studentInfo[0]}")
    print(f"Student group: {studentInfo[2]}")

    for course in studentregisteredCourses:
        print(f"{course} : {studentregisteredCourses[course]}")

    for course in studentAttendance:
        if (course == courseCode):
            for date in studentAttendance[course]:
                if (studentAttendance[course][date] == True):
                    print(f"On {date}, {studentInfo[1]} attended the lecture")
                else:
                    print(f"On {date}, {studentInfo[1]} didn't attended the lecture")

