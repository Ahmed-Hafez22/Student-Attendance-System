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
            attendance_dict = {}
            for course in courses_dict.values():
                attendance_dict[course] = {}
                update_query = "UPDATE allStudents SET attendance = ?"
                database_cursor.execute(update_query, (json.dumps(attendance_dict),))
    database_connection.commit()


def take_attendance():  
    def get_today_course(courses):
        for course_code in courses:
            if today_info[0] == courses[course_code]["Day"]:
                return course_code
            else:
                pass

    def check_if_student_registered_course(courses):
            for course in courses:
                for g1_course in courses_dict:
                    if course == g1_course : 
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
            course_time_obj.append(datetime.strptime(time, "%H:%M").replace(year=date_obj.year, month=date_obj.month, day=date_obj.day))
        
        for time_obj in course_time_obj:
            gap = timedelta(minutes=15)
            time_difference = current_time_obj - time_obj
            if time_difference <= gap:
                return time_obj
            else:
                continue
    
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
            courses_JSON =database_cursor.execute("SELECT courses FROM Group1Table").fetchone()[0]
            courses_dict = json.loads(courses_JSON)

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

        today_course = get_today_course(courses_dict)

        if greenLight == True:
            attendance_JSON_query = (
                "SELECT attendance FROM allStudents WHERE AcademicID = ?"
            )
            attendance_JSON = database_cursor.execute(
                attendance_JSON_query, (student_ID,)
            ).fetchone()[0]
            attendance_dict = json.loads(attendance_JSON)
            course_time_obj = get_course_time(courses_dict)
            print((type(course_time_obj)) , (type(current_time_obj)))
            time_difference = course_time_obj - current_time_obj
            MAX_GAP = timedelta(minutes=15)
            MIN_GAP = timedelta(minutes=0)
            registered_lst = []
            if time_difference <= MAX_GAP and time_difference > MIN_GAP:
                for course in studentCourses_dict.values():
                    if today_course == course:
                        attendance_dict[today_course][today_info[1]] = True
                        registered_lst.append(student_ID)
                        database_cursor.execute(
                "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                (json.dumps(attendance_dict), student_ID),
            )
            else:
                for course in studentCourses_dict.values():
                    if today_course == course:
                        attendance_dict[today_course][today_info[1]] = False
                    database_cursor.execute(
                "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                (json.dumps(attendance_dict), student_ID),
            )

                for studentAcademicID in registered_lst:
                    left_out_students = database_cursor.execute("SELECT attendance FROM allStudents WHERE AcademicID != ?", (studentAcademicID,))
                    for course in studentCourses_dict.values():
                        if today_course == course:
                            attendance_dict[today_course][today_info[1]] = False
                    database_cursor.execute(
                "UPDATE allStudents SET attendance = ? WHERE AcademicID = ?",
                (json.dumps(attendance_dict), student_ID),
            )
    database_connection.commit()