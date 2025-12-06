import DatabaseFunctions
import DatabaseConstantData
from libs import *


#Set intial start
def update_time():
    today = datetime.now()
    return today


intiationTime = update_time()
endTime = datetime.strptime("15:00", "%H:%M").replace(
    year=intiationTime.year, month=intiationTime.month, day=intiationTime.day
)

DatabaseFunctions.insert_date()

latestDay = DatabaseConstantData.database_cursor.execute(
    """
        SELECT Date FROM DateTable WHERE id = (SELECT MAX (id) FROM DateTable)
"""
).fetchone()[0]

latestDay = datetime.strptime(latestDay, "%Y-%m-%d").replace(hour=intiationTime.hour, minute=intiationTime.minute)

DatabaseFunctions.make_attendance_dict()


window = Tk()
window.state("zoomed")
window.title("Student Attendance System")
window.config(background="white")

orginal_logo = Image.open("D:\\Programming\\Pyhton Projects\\Student Barcode Attendance System\\Innovation_University_logo.png")
orginal_text = Image.open("D:\\Programming\\Pyhton Projects\\Student Barcode Attendance System\\Innovation_University.png")

tk_logo = ImageTk.PhotoImage(orginal_logo)
tk_text = ImageTk.PhotoImage(orginal_text)

center_frame = Frame(window, background="white")
center_frame.pack(expand=True)


logo_label = Label(center_frame, image=tk_logo)
text_label = Label(center_frame, image=tk_text)

logo_label.pack()
text_label.pack()

main_frame = Frame(window, background="white")
# fill="both" ensures the frame takes the whole screen, allowing us to center things inside it
main_frame.pack(expand=True, fill="both")

def startApp():
    center_frame.destroy()

    for widget in main_frame.winfo_children():
        widget.destroy()

    # --- CENTER CONTAINER ---
    # This invisible frame sits in the exact center of the screen
    container = Frame(main_frame, background="white")
    container.place(relx=0.5, rely=0.5, anchor="center")

    # 1. The Label
    Label(container,
          text="Choose a computer",
          background="white",
          font=("Arial", 30, "bold")).pack(pady=(0, 40))

    # 2. The Buttons (Grouped in a row)
    button_row = Frame(container, background="white")
    button_row.pack()

    comp_0_btn = Button(button_row,
                        font=("Inter", 24),
                        text="Computer 0",
                        relief="solid",
                        background="white",
                        width=12,
                        command=takeAttendance)
    
    comp_1_btn = Button(button_row,
                        font=("Inter", 24),
                        text="Computer 1",
                        relief="solid",
                        background="white",
                        width=12,
                        command=staffSignIn)

    comp_0_btn.pack(side="left", padx=20)
    comp_1_btn.pack(side="left", padx=20)
    
def takeAttendance():
    # 1. Clear the screen
    for widget in main_frame.winfo_children():
        widget.destroy()

    # 2. Logic Functions
    def force_focus(event = None):
        scanner_entry.focus_set()

    def processScan(event = None):
        global latestDay
        updateTime = update_time()
        latestDay = latestDay.replace(hour=updateTime.hour, minute=updateTime.minute)
        if(latestDay > endTime):
            return
        else:
            content = scanner_entry.get()
            if content:
                try:
                    studentID = int(content)
                    DatabaseFunctions.take_attendance(studentID)
                    # Optional: Add visual feedback here (e.g., "Scanned!")
                except:
                    pass

                scanner_entry.delete(0, END)
                scanner_entry.focus_set()

    # --- 3. CENTER LAYOUT ---
    # We create a container frame and place it in the exact middle
    container = Frame(main_frame, bg="white")
    container.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    Label(container, text="Ready to Scan", font=("Arial", 24, "bold"), bg="white").pack(pady=(0, 20))

    # Scanner Entry (Styled to be visible)
    scanner_entry = Entry(
        container, 
        bg="#EADDE8",   # Light purple background
        fg="black",     # Black text
        width=30, 
        font=("Arial", 16),
        justify="center"
    )
    scanner_entry.pack(pady=(0, 40), ipady=10) # ipady makes the box taller
    
    scanner_entry.focus_set()
    scanner_entry.bind("<Button-1>", force_focus)
    scanner_entry.bind("<Return>", processScan)

    # Change Computer Button
    Button(
        container,
        text="Change Computer",
        font=("Inter", 16),
        bg="white",
        relief="solid",
        bd=1,
        width=20,
        command=startApp
    ).pack()

def staffSignIn():
    screenHeight = window.winfo_screenheight()
    screenWidth = window.winfo_screenwidth()

    PURPLE_LIGHT = "#EADDE8"
    PURPLE_DARK  = "#6A368B"  
    TEXT_BLACK   = "#1E1E1E"
    
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # 2. CREATE A CONTAINER
    login_box = CTkFrame(main_frame, corner_radius=0, fg_color="white")
    login_box.pack(expand=True, fill="both")

    logo_ctk = CTkImage(light_image=orginal_logo, size=(100, 100))
    logo_label = CTkLabel(login_box, image=logo_ctk, text="")
    logo_label.pack(pady=(50, 10))
    CTkLabel(login_box, text="Innovation\nUniversity", 
                font=("Arial", 28, "bold"), text_color=PURPLE_DARK).pack(pady=(50, 20))

    CTkLabel(login_box, text="Sign in", 
                font=("Arial", 20, "bold"), text_color="black").pack(pady=(0, 30))
    
    # --- EMAIL FIELD ---
    CTkLabel(login_box, text="Email*", text_color="black", 
                font=("Arial", 12, "bold"), anchor="w").pack(pady=(0, 5))
    
    email_entry = CTkEntry(
        login_box,
        width=400,            
        height=50,            
        corner_radius=20,     
        fg_color=PURPLE_LIGHT,
        border_width=0,       
        text_color="black",
        font=("Arial", 14)
    )
    email_entry.pack(pady=(0, 20))

    # --- PASSWORD FIELD ---
    CTkLabel(login_box, text="Password*", text_color="black", 
                font=("Arial", 12, "bold"), anchor="w").pack(pady=(0, 5))
    
    pass_frame = CTkFrame(login_box, fg_color="transparent")
    pass_frame.pack()

    password_entry = CTkEntry(
        pass_frame,
        width=400,
        height=50,
        corner_radius=20,
        fg_color=PURPLE_LIGHT,
        border_width=0,
        text_color="black",
        font=("Arial", 14),
        show="*" 
    )
    password_entry.pack()

    # --- SHOW/HIDE TOGGLE ---
    def toggle_password():
        if show_pass_var.get() == 1:
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    show_pass_var = IntVar(value=0)
    show_pass_chk = CTkCheckBox(
        login_box, 
        text="Show Password", 
        command=toggle_password,
        variable=show_pass_var,
        text_color="gray",
        fg_color=PURPLE_DARK,
        hover_color=PURPLE_DARK
    )
    show_pass_chk.pack(pady=(10, 0))

    # --- LOGIN LOGIC ---
    # We add 'event=None' so this function can be called by a button click OR a key press
    def login_action(event=None):
        email = email_entry.get()
        password = password_entry.get()
        
        # Simple validation before DB call
        if not email or not password:
            return 

        query = "SELECT name, courses FROM collegeStaff WHERE email = ? AND password = ?"
        staffInfo = DatabaseFunctions.database_cursor.execute(query, (email, password)).fetchone()

        if staffInfo:
            staffScreen(staffInfo[0], staffInfo[1])
        else:
            # Optional: Visual feedback for failed login
            print("Invalid Login")

    # --- SIGN IN BUTTON ---
    login_btn = CTkButton(
        login_box,
        text="Sign in",
        font=("Arial", 15, "bold"),
        width=400,
        height=50,
        corner_radius=25,     
        fg_color=PURPLE_DARK, 
        hover_color="#502a69",
        command=login_action
    )
    login_btn.pack(pady=40)

    # --- KEY BINDINGS & FOCUS ---
    # 1. Allow pressing 'Enter' key inside the boxes to trigger login
    email_entry.bind("<Return>", login_action)
    password_entry.bind("<Return>", login_action)

    # 2. Force Focus on Email Field so user can type immediately
    # We use 'after' to ensure the widget is fully drawn before grabbing focus
    email_entry.after(100, email_entry.focus_set)
# --- ADD THESE 2 LINES AT THE VERY TOP OF YOUR FILE (Global Scope) ---
current_staff_name = ""
current_staff_courses = ""

# --- REPLACE YOUR staffScreen FUNCTION WITH THIS ---
def staffScreen(staffName, staffCourses_raw):
    # 1. SAVE STATE (Solves Problem 1)
    # We save these into the global variables so the 'Back' button can use them later
    global current_staff_name, current_staff_courses
    current_staff_name = staffName
    current_staff_courses = staffCourses_raw

    # 2. CLEAR FRAME
    for widget in main_frame.winfo_children():
        widget.destroy()

    # 3. PARSE COURSES
    try:
        courses_data = json.loads(staffCourses_raw)
        # Assuming format: {"Course 1": "BS213", ...}
        course_codes = list(courses_data.values()) 
    except:
        course_codes = []

    # --- UI SETUP ---
    
    # Header
    header_frame = CTkFrame(main_frame, fg_color="white", height=80)
    header_frame.pack(fill="x", side="top")
    
    # Logo & Name
    # (Make sure 'orginal_logo' is defined at the top of your file)
    logo_img = CTkImage(light_image=orginal_logo, size=(40, 40))
    CTkLabel(header_frame, image=logo_img, text="").pack(side="left", padx=20, pady=10)
    
    CTkLabel(header_frame, text=f"Welcome, {staffName}", 
                 font=("Arial", 16, "bold"), text_color="#6A368B").pack(side="left")

    # Logout
    CTkButton(header_frame, text="Logout", width=80, height=30, 
                  fg_color="#EADDE8", text_color="black",
                  command=staffSignIn).pack(side="right", padx=20)

    # Subject Selection
    subject_frame = CTkFrame(main_frame, fg_color="white")
    subject_frame.pack(fill="x", pady=20, padx=40)

    CTkLabel(subject_frame, text="Select Subject:", 
                 font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", pady=(0, 10))

    # Student List Container
    list_frame = CTkScrollableFrame(main_frame, fg_color="white", width=600, height=400)
    list_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    # --- LOAD STUDENTS LOGIC ---
    def load_students(selected_course):
        # Clear current list
        for widget in list_frame.winfo_children():
            widget.destroy()

        CTkLabel(list_frame, text=f"Students registered for {selected_course}:", 
                     font=("Arial", 14, "bold"), text_color="black", anchor="w").pack(fill="x", pady=10)

        # SQL Query
        query = f"SELECT name, AcademicID FROM allStudents WHERE registeredCourses LIKE ?"
        results = DatabaseFunctions.database_cursor.execute(query, (f'%{selected_course}%',)).fetchall()

        if not results:
            CTkLabel(list_frame, text="No students found.", text_color="gray").pack(pady=20)
            return

        # --- THIS IS "PART 3" (THE CLICK LOGIC) ---
        for student in results:
            name = student[0]
            academic_id = student[1]

            # We use a Frame instead of a Button to control the look better
            row_frame = CTkFrame(list_frame, fg_color="#EADDE8", corner_radius=10, height=45)
            row_frame.pack(fill="x", pady=5)

            # THE CLICK FUNCTION
            # This captures the specific ID/Name for THIS row
            def on_click(event, sid=academic_id, sname=name, c=selected_course):
                # Calls the profile screen function
                show_student_profile(sid, sname, c)

            # BIND THE CLICK
            # We must bind the click to the Frame AND the Labels inside it
            # otherwise clicking the text won't work.
            row_frame.bind("<Button-1>", on_click)

            # Grey Dot
            dot = CTkLabel(row_frame, text="●", text_color="gray", font=("Arial", 16))
            dot.pack(side="left", padx=15)
            dot.bind("<Button-1>", on_click)

            # Name
            lbl_name = CTkLabel(row_frame, text=name, text_color="black", font=("Arial", 14))
            lbl_name.pack(side="left")
            lbl_name.bind("<Button-1>", on_click)
            
            # ID
            lbl_id = CTkLabel(row_frame, text=str(academic_id), text_color="gray", font=("Arial", 12))
            lbl_id.pack(side="right", padx=15)
            lbl_id.bind("<Button-1>", on_click)

    # --- GENERATE SUBJECT BUTTONS ---
    for course in course_codes:
        btn = CTkButton(
            subject_frame, 
            text=course, 
            font=("Arial", 14, "bold"),
            fg_color="#6A368B", 
            text_color="white",
            width=150,
            command=lambda c=course: load_students(c)
        )
        btn.pack(side="left", padx=(0, 10))

    # Auto-load first course
    if course_codes:
        load_students(course_codes[0])

def calculate_attendance_percentage(attendance_json_str, course_code):
    """
    Parses the JSON string from the DB and calculates % for the specific course.
    """
    try:
        data = json.loads(attendance_json_str)
        
        # Get the dictionary for the specific course (e.g., "BS213")
        course_data = data.get(course_code, {})
        
        if not course_data:
            return "N/A (No classes recorded)"

        total_classes = len(course_data)
        if total_classes == 0:
            return "0%"
            
        # Count how many times value is True
        present_count = sum(1 for status in course_data.values() if status is True)
        
        percentage = (present_count / total_classes) * 100
        return f"{int(percentage)}% ({present_count}/{total_classes})"
        
    except Exception as e:
        print(f"Error calc attendance: {e}")
        return "Error"

def show_student_profile(student_id, student_name, course_code):
    # Ensure layout fills screen
    main_frame.pack(fill="both", expand=True)

    # 1. CLEAR FRAME
    for widget in main_frame.winfo_children():
        widget.destroy()

    # 2. FETCH DATA
    query = "SELECT attendance FROM allStudents WHERE AcademicID = ?"
    result = DatabaseFunctions.database_cursor.execute(query, (student_id,)).fetchone()
    attendance_json = result[0] if result else "{}"
    attendance_stat = calculate_attendance_percentage(attendance_json, course_code)

    # --- 3. POPUP LOGIC (Standard Tkinter to Fix Crash) ---
    def open_excuse_popup():
        try:
            data = json.loads(attendance_json)
            course_data = data.get(course_code, {})
            absent_dates = [date for date, status in course_data.items() if status is False]
        except:
            absent_dates = []

        # USE STANDARD TKINTER WINDOW (No Crash)
        popup = Toplevel(window) 
        popup.title("Grant Excuse")
        popup.geometry("400x500")
        popup.config(bg="white")
        
        # Keep popup on top
        popup.transient(window)
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        # Header
        Label(popup, text=f"Excuse Absences\n{course_code}", 
              font=("Arial", 18, "bold"), bg="white", fg="black").grid(row=0, column=0, pady=20)

        if not absent_dates:
            Label(popup, text="✅ No absences found!", font=("Arial", 14), bg="white", fg="green").grid(row=1, column=0)
            Button(popup, text="Close", command=popup.destroy).grid(row=2, column=0, pady=20)
            return

        # List of Checkboxes (Using Standard Frame + Canvas for scrolling if needed, 
        # but for simplicity we'll just pack them in a frame since lists are usually short)
        
        list_frame = Frame(popup, bg="white")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=30)
        
        checkbox_vars = []
        for date in absent_dates:
            var = BooleanVar(value=False)
            # Standard Checkbutton
            chk = Checkbutton(list_frame, text=date, variable=var, 
                              font=("Arial", 12), bg="white", activebackground="white", anchor="w")
            chk.pack(fill="x", pady=5)
            checkbox_vars.append((date, var))

        def submit_excuses():
            updates_made = False
            for date_str, var in checkbox_vars:
                if var.get():
                    DatabaseFunctions.make_excuse(student_id, course_code, date_str)
                    updates_made = True
            
            popup.destroy()
            if updates_made:
                window.after(100, lambda: show_student_profile(student_id, student_name, course_code))

        # Buttons
        btn_frame = Frame(popup, bg="white")
        btn_frame.grid(row=2, column=0, pady=20)
        
        Button(btn_frame, text="Cancel", command=popup.destroy, width=10).pack(side="left", padx=10)
        Button(btn_frame, text="Confirm", command=submit_excuses, width=10, bg="#6A368B", fg="white").pack(side="left", padx=10)


    # --- 4. MASTER LAYOUT ---
    profile_view = CTkFrame(main_frame, fg_color="white", corner_radius=0)
    profile_view.pack(fill="both", expand=True)

    profile_view.grid_rowconfigure(0, weight=0) 
    profile_view.grid_rowconfigure(1, weight=1) 
    profile_view.grid_columnconfigure(0, weight=1) 
    profile_view.grid_columnconfigure(1, weight=1) 

    # Header
    header = CTkFrame(profile_view, fg_color="white", height=80, corner_radius=0)
    header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
    
    logo_img = CTkImage(light_image=orginal_logo, size=(40, 40))
    CTkLabel(header, image=logo_img, text="").pack(side="left", padx=(10, 10))
    
    title_frame = CTkFrame(header, fg_color="transparent")
    title_frame.pack(side="left")
    CTkLabel(title_frame, text="Innovation", font=("Arial", 20, "bold"), text_color="#6A368B", anchor="w").pack(anchor="w")
    CTkLabel(title_frame, text="University", font=("Arial", 20, "bold"), text_color="#6A368B", anchor="w").pack(anchor="w")

    btn_back = CTkButton(
        header, text="← Back", width=80, height=30,
        fg_color="#EADDE8", text_color="black", hover_color="#D1C4D0",
        font=("Arial", 12, "bold"),
        command=lambda: staffScreen(current_staff_name, current_staff_courses)
    )
    btn_back.pack(side="right", padx=10)

    # Left Side (Avatar)
    left_frame = CTkFrame(profile_view, fg_color="white", corner_radius=0)
    left_frame.grid(row=1, column=0, sticky="nsew")
    
    avatar_container = CTkFrame(left_frame, fg_color="transparent")
    avatar_container.pack(expand=True)

    avatar = CTkLabel(avatar_container, text="", fg_color="#8F92A1", width=250, height=250, corner_radius=125)
    avatar.pack()
    CTkLabel(avatar, text="👤", font=("Arial", 100), text_color="#5A5E6B").place(relx=0.5, rely=0.5, anchor="center")

    # Right Side (Cards)
    right_frame = CTkFrame(profile_view, fg_color="white", corner_radius=0)
    right_frame.grid(row=1, column=1, sticky="nsew")

    info_container = CTkFrame(right_frame, fg_color="#F6F6F6", corner_radius=40, width=500, height=420)
    info_container.pack(expand=True)
    info_container.pack_propagate(False) 

    cards_vertical_group = CTkFrame(info_container, fg_color="transparent")
    cards_vertical_group.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

    def create_purple_card(label_text, value_text):
        card = CTkFrame(cards_vertical_group, fg_color="#CBAACD", height=60, corner_radius=15)
        card.pack(fill="x", pady=10)
        card.pack_propagate(False)
        CTkLabel(card, text=label_text, font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=20)
        CTkLabel(card, text=value_text, font=("Arial", 16, "bold"), text_color="white").pack(side="right", padx=20)

    create_purple_card("Student Name:", student_name)
    create_purple_card("Student ID:", str(student_id))
    create_purple_card("Student Course Attendance:", attendance_stat)

    # Button to Open Popup
    CTkButton(
        cards_vertical_group,
        text="Make Excuse",
        font=("Arial", 14, "bold"),
        fg_color="#6A368B",       
        hover_color="#502a69",
        height=40,
        corner_radius=20,
        command=open_excuse_popup
    ).pack(pady=(20, 0), fill="x")

window.after(1000, startApp)
window.mainloop()