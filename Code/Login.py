from tkinter import *
from tkinter import messagebox
from Open import open_teacher_window, open_student_window
from ConnectDatabase import connect_db

# 학생 로그인 검증 함수
def validate_student_login(id, pw):
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM learner WHERE `learnerID` = %s AND `password` = %s"
    cursor.execute(query, (id, pw))
    result = cursor.fetchone()
    conn.close()

    return result[0] > 0  # 일치하는 행이 있으면 True

# 로그인 처리 함수
def verify():
    user_type = userType.get()  # 라디오 버튼 값 확인 (선생/학생 구분)
    id = idEntry.get()
    pw = pwEntry.get()

    if user_type == "teacher":
        # 선생님 로그인
        if id == "ddd" and pw == "ddd":
            messagebox.showinfo("Login Successful", "Welcome, Teacher!")
            open_teacher_window()  # 선생님 창 열기
        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password for Teacher.")
    elif user_type == "student":
        # 학생 로그인
        if validate_student_login(id, pw):
            messagebox.showinfo("Login Successful", "Welcome, Student!")
            open_student_window(id)  # 학생 창 열기
        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password for Student.")
    else:
        messagebox.showerror("Login Failed", "Please select user type.")

# 메인 윈도우 생성
window = Tk()
window.geometry("800x300")  # 창 크기 변경
window.title("Math Is Fun")

# 색상 조합
bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

# 창 배경색 설정
window.configure(bg=bg_color)

# 메인 프레임 생성
main_frame = Frame(window, bg=bg_color)
main_frame.grid(row=0, column=0, sticky="nsew")

# 왼쪽 프레임 (제목/설명)
left_frame = Frame(main_frame, bg=bg_color_2, width=480)
left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

titleLabel = Label(
    left_frame,
    text="Welcome to MATH IS FUN!",
    font=("Arial", 24, "bold"),
    fg=text_color,
    bg=bg_color_2
)
titleLabel.grid(row=0, column=0, pady=20, sticky="w")

descriptionLabel = Label(
    left_frame,
    text="""
        MATH IS FUN aims for effective lessons and teacher-student interactions.  
        This is the login page for teachers and students.  
        Please select your role and enter your credentials to continue.  
    """,
    font=("Arial", 14), fg=text_color, bg=bg_color_2, justify=LEFT
)
descriptionLabel.grid(row=1, column=0, pady=10, sticky="w")

# 오른쪽 프레임 (아이디/비번 입력)
right_frame = Frame(main_frame, bg=bg_color, width=320)
right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# 사용자 타입 선택 (라디오 버튼)
userType = StringVar(value="teacher")  # 기본값을 'teacher'로 설정
teacherRadio = Radiobutton(
    right_frame,
    text="Teacher",
    variable=userType,
    value="teacher",
    font=("Arial", 14),
    bg=bg_color,
    activebackground=bg_color,
    fg=text_color
)
teacherRadio.grid(row=0, column=0, pady=5, sticky="w")

studentRadio = Radiobutton(
    right_frame,
    text="Student",
    variable=userType,
    value="student",
    font=("Arial", 14),
    bg=bg_color,
    activebackground=bg_color,
    fg=text_color
)
studentRadio.grid(row=1, column=0, pady=5, sticky="w")

# 아이디 입력
idLabel = Label(right_frame, text="ID:", font=("Arial", 14), fg=text_color, bg=bg_color)
idLabel.grid(row=2, column=0, pady=5, sticky="w")
idEntry = Entry(right_frame, font=("Arial", 14), bg=entry_color, highlightbackground=text_color, highlightthickness=1)
idEntry.grid(row=3, column=0, pady=5, sticky="ew")

# 비밀번호 입력
pwLabel = Label(right_frame, text="Password:", font=("Arial", 14), fg=text_color, bg=bg_color)
pwLabel.grid(row=4, column=0, pady=5, sticky="w")
pwEntry = Entry(right_frame, font=("Arial", 14), show="*", bg=entry_color, highlightbackground=text_color, highlightthickness=1)
pwEntry.grid(row=5, column=0, pady=5, sticky="ew")

# 로그인 버튼
loginButton = Button(
    right_frame,
    text="Login",
    font=("Arial", 14, "bold"),
    bg=button_color,
    fg=text_color,
    activebackground=text_color,
    activeforeground=button_color,
    command=verify,
    borderwidth=0
)
loginButton.grid(row=6, column=0, pady=20)

# 창 크기 조정 및 비율 유지
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=3)  # 왼쪽 프레임 비율
main_frame.grid_columnconfigure(1, weight=2)  # 오른쪽 프레임 비율

window.mainloop()
