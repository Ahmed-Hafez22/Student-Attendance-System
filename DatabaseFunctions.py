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


def take_attendance():
    def get_today_course(courses):
        for course_code in courses:
            if today_info[0] == courses[course_code]["Day"]:
                print(course_code)
                return course_code
            else:
                pass

    def check_if_student_registered_course(courses):
        for course in courses:
            for g1_course in courses_dict:
                if course == g1_course:
                    print(True)
                    return True
                else:
                    continue
        return False

    def get_course_time(courses):
        course_time_str = []
        for course_code in courses:
            course_time_str.append(courses[course_code]["End Time"])

        course_time_obj = []
        for time in course_time_str:
            course_time_obj.append(
                datetime.strptime(time, "%H:%M").replace(
                    year=date_obj.year, month=date_obj.month, day=date_obj.day
                )
            )
        print(course_time_obj)
        for time_obj in course_time_obj:
            gap = timedelta(minutes=15)
            print(f"Current Time: {current_time}")
            print(f"Time OBJ: {time_obj}")
            time_difference = time_obj - current_time_obj
            print(f"Time Difference: {time_difference}")
            if time_difference <= gap:
                print(f"Time difference: {time_difference} | Gap: {gap}")
                return time_obj
            else:
                continue

    today_info = database_cursor.execute(
        """
                                        SELECT Day, Date
                                        FROM DateTable
                                        WHERE id = (SELECT MAX(id) FROM DateTable)
                                    """
    ).fetchone()

    date_obj = datetime.strptime(today_info[1], "%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
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
        elif student[1] == 2:
            courses_JSON = database_cursor.execute(
                "SELECT courses FROM Group2Table"
            ).fetchone()[0]
            courses_dict = json.loads(courses_JSON)

        today_course = get_today_course(courses_dict)

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
                attendanceDict[course][today_info[1]] = False
                database_cursor.execute(
                    "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                    (json.dumps(attendanceDict), student[0]),
                )
            else:
                continue
    database_connection.commit()

    student_ID = input("Waiting for scan: ")
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
        elif student_group == 2:
            courses_JSON = database_cursor.execute(
                "SELECT courses FROM Group2Table"
            ).fetchone()[0]
            courses_dict = json.loads(courses_JSON)

        course_time_obj = get_course_time(courses_dict)
        time_difference = course_time_obj - current_time_obj
        MAX_GAP = timedelta(minutes=15)
        MIN_GAP = timedelta(minutes=0)
        today_course = get_today_course(courses_dict)

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


def get_subject_percentage(day, month, year, desieredCourse):
    all_subjects_dict = {}
    counter = 0
    def get_all_subjects(counter):
        all_students = database_cursor.execute("SELECT AcademicID FROM allStudents").fetchall()
        for id in all_students:
            StudentCourses_JSON = database_cursor.execute(
                """
                    SELECT registeredCourses
                    FROM allStudents
                    WHERE AcademicID = ?
    """ , (id[0],)
            ).fetchone()[0]
            StudentCourses_dict = json.loads(StudentCourses_JSON)
            all_subject_lst = list(all_subjects_dict.values())
            for course in StudentCourses_dict.values() :
                if course not in all_subject_lst:
                    counter += 1 
                    all_subjects_dict[f"Course {counter}"] = course
        return all_subjects_dict
    
    def get_student_number_for_each_subject():
        coursesDict = get_all_subjects(counter)
        studentsDict = {}
        percentageDict = {}
        all_students = database_cursor.execute("SELECT AcademicID FROM allStudents").fetchall()
        
        desiredDate_str = datetime(year, month, day).strftime("%Y-%m-%d")

        desiredDate_obj = datetime.strptime(desiredDate_str, "%Y-%m-%d")

        for course in coursesDict.values():
            studentsCount = 0
            presentStudent = 0
            studentsDict[course] = {
                    "All Students" : studentsCount,
                    "Present Students" : presentStudent,
                    "Absent Students" :0
                }
            percentageDict[course] = {
                "Attendance Percentage" : 0,
                "Absence Percentage" : 0
            }
            for id in all_students:
                studentCourses_JSON = database_cursor.execute(
                """
                    SELECT registeredCourses
                    FROM allStudents
                    WHERE AcademicID = ?
                """ , (id[0],)).fetchone()[0]
                studentCourses_dict = json.loads(studentCourses_JSON)
                if course in studentCourses_dict.values():
                    studentsCount += 1
                studentsDict[course]["All Students"] = studentsCount

                studentAttendance_JSON = database_cursor.execute(
                """
                    SELECT attendance
                    FROM allStudents
                    WHERE AcademicID = ?
                """, (id[0],)).fetchone()[0]
                studentAttendance_dict = json.loads(studentAttendance_JSON)

                if (course in studentAttendance_dict 
                    and desiredDate_str in studentAttendance_dict[course] 
                    and studentAttendance_dict[course][desiredDate_str] == True):
                    presentStudent += 1
                studentsDict[course]["Present Students"] = presentStudent
                studentsDict[course]["Absent Students"] = studentsDict[course]["All Students"] - studentsDict[course]["Present Students"]

            attendacncePercent = (studentsDict[course]["Present Students"] / studentsDict[course]["All Students"]) * 100
            absencePrecent = (studentsDict[course]["Absent Students"] / studentsDict[course]["All students"]) * 100
            percentageDict[course]["Attendance Percentage"] = attendacncePercent
            percentageDict[course]["Absence Percentage"] = absencePrecent
    #print(percentageDict[course])
    get_student_number_for_each_subject()