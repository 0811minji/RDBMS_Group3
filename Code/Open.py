from tkinter import *
from tkinter import messagebox
from OpenWindow import OpenWindow
from AnalysisPackage.AnalysisChapter import chapterAnalysis
from AnalysisPackage.AnalysisLearner import learnerAnalysis
from ConnectDatabase import *

bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

def analysis_selected(value):
    
    global frame_entry
    frame_entry = Frame(window_teacher, bg=bg_color_2, borderwidth=5)
    frame_entry.place(relwidth=0.9, relheight=0.4, relx=0.05, rely=0.3)

    for widget in frame_entry.winfo_children():
                widget.destroy()

    if value == "Chapter":
        # School Level 선택
        Label(frame_entry, text="Select School Level:", bg=bg_color_2, fg=text_color).pack(anchor=W, pady=5)

        # 선택할 수 있는 라디오 버튼
        school_level = StringVar()
        school_level.set("Elementary")

        levels = [("Elementary", "elementary"), ("Middle", "middle"), ("High", "high")]

        for text, val in levels:
            Radiobutton(frame_entry, text=text, variable=school_level, value=val, bg=bg_color_2, activebackground=bg_color_2, fg=text_color).pack(anchor=W, pady=5)

        # Confirm 버튼
        def confirm_selection():

            selected_level = school_level.get()
            print(f"Selected Level: {selected_level}")  # 디버깅용 출력
            # OpenWindow 호출
            # open_window = OpenWindow(selected_level, frame_entry)
            # open_window.ChapterWindow()

            new_root = Toplevel(window_teacher)  # 부모 창은 기존 window
            app = chapterAnalysis(new_root, school=selected_level)  # 선택된 level 전달
            new_root.mainloop()  # 이벤트 루프 실행

        Button(frame_entry, text="Confirm", bg=bg_color_2, fg=text_color, activebackground=button_color, command=confirm_selection).pack(pady=10)
    
    elif  value == "Test":

        indicateLabel = Label(frame_entry, text=f"Enter {value} ID", bg=bg_color_2, fg=text_color)
        indicateLabel.pack(anchor=W)

        global selectedEntry        
        selectedEntry = Entry(frame_entry, bg=entry_color, highlightbackground=text_color, highlightthickness=1)
        selectedEntry.pack(anchor=W)
        selectedEntry.focus_set()

        open_window = OpenWindow(selectedEntry, frame_entry)
        
        selectedEntry.bind("<Return>", lambda event: open_window.TestWindow())
    
    else:
        Label(frame_entry, text="Select School Grade:", bg=bg_color_2, fg=text_color).grid(row=0, column=0, padx=5, pady=10)

        school_grade = StringVar()
        school_grade.set("Elementary-1")

        grades = [("Elementary-1", "Elementary-1"), ("Elementary-2", "Elementary-2"), ("Elementary-3", "Elementary-3"), 
                  ("Elementary-4", "Elementary-4"), ("Elementary-5", "Elementary-5"), ("Elementary-6", "Elementary-6"), 
                  ("Middle-1", "Middle-1"), ("Middle-2", "Middle-2"), ("Middle-3", "Middle-3")]

        for idx, (text, val) in enumerate(grades):
            Radiobutton(frame_entry, text=text, variable=school_grade, value=val, bg=bg_color_2, fg=text_color).grid(row=idx%3+1, column=idx//3, padx=5, pady=5, sticky="w")

        def confirm_grade_selection():
            
            selected_grade = school_grade

            open_window = OpenWindow(selected_grade,frame_entry)
            open_window.LearnerWindow()

        Button(frame_entry, text="Confirm", bg=bg_color_2, fg=text_color, activebackground=button_color, command=confirm_grade_selection).grid(row=4, column=1, padx=5, pady=10)


def open_teacher_window():
    
    global window_teacher
    window_teacher = Toplevel()
    window_teacher.geometry("600x500")
    window_teacher.title("Teacher")
    window_teacher.configure(bg=bg_color)
    window_teacher.resizable(0, 0)

    frame_button = Frame(window_teacher, bg=bg_color_2, borderwidth=5)
    frame_button.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.1)


    modes = [
        ("Test Analysis", "Test"),
        ("Learner Analysis", "Learner"),
        ("Chapter Analysis", "Chapter")
    ]

    analysis = StringVar()
    analysis.set("Chapter Analysis")

    for idx, (analy, mode) in enumerate(modes):
        Radiobutton(frame_button, text=analy, variable=analysis, value=mode, bg=bg_color_2, activebackground=bg_color_2, fg=text_color,
                    command=lambda: analysis_selected(analysis.get())).grid(row=0, column=5*idx, padx=5, pady=8)
    
def open_student_window(student_id):

    def submit_feedback():
        feedback = feedbackEntry.get("1.0", END).strip()  # 피드백 내용 가져오기
        if not feedback:
            messagebox.showerror("Error", "Feedback cannot be empty.")
            return

        conn = connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            query = "UPDATE learner SET feedback = %s WHERE `learnerID` = %s"
            cursor.execute(query, (feedback, student_id))
            conn.commit()
            messagebox.showinfo("Success", "Feedback submitted successfully!")
            feedbackWindow.destroy()  # 창 닫기
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to submit feedback: {e}")
        finally:
            conn.close()

    def check_my_status():
        window_status = Toplevel()
        window_status.title("My Status")
        window_status.config(bg=bg_color)
        window_status.attributes("-fullscreen", True)

        learner_analysis = learnerAnalysis(window_status, int(student_id[2]), student_id)
        learner_analysis.view_correctRatio()

    # 피드백 입력 창
    feedbackWindow = Toplevel()
    feedbackWindow.geometry("800x600")
    feedbackWindow.title("Student Feedback")
    feedbackWindow.configure(bg=bg_color)

    feedbackWindow.grid_columnconfigure(0, weight=1)
    feedbackWindow.grid_columnconfigure(1, weight=1)
    feedbackWindow.grid_columnconfigure(2, weight=1)

    # 스타일 및 레이아웃
    titleLabel = Label(feedbackWindow, text="Feedback Form", bg=bg_color, font=('Helevetica', 20))
    titleLabel.grid(row=0, column=1, pady=20, padx=20)

    feedbackLabel = Label(feedbackWindow, text="Enter your feedback below:", bg=bg_color, font=('Helevetica', 14))
    feedbackLabel.grid(row=1, column=1, pady=10, padx=20)

    feedbackEntry = Text(feedbackWindow, font=('Helevetica', 16),bg=entry_color, width=50, height=10)
    feedbackEntry.grid(row=2, column=1, pady=10, padx=20)

    submitButton = Button(feedbackWindow, text="Submit Feedback", font=('Helevetica', 14), bg=button_color, command=submit_feedback)
    submitButton.grid(row=3, column=1, pady=20, padx=20)

    Button(feedbackWindow, text="Check My Status", font=('Helevetica', 14), command=lambda: check_my_status()).grid(row=4, column=1, pady=10, padx=20)

    feedbackWindow.mainloop()