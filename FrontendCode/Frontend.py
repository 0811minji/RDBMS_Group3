from tkinter import *
from OpenWindow import OpenWindow
from ChapterApp import ChapterApp


def analysis_selected(value):
    
    global frame_entry
    frame_entry = Frame(window, bg="white", borderwidth=5)
    frame_entry.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.3)


    if value == "Chapter":
        # School Level 선택
        Label(frame_entry, text="Select School Level:", bg="white").pack(anchor=W, pady=5)

        # 선택할 수 있는 라디오 버튼
        school_level = StringVar()
        school_level.set("Elementary")

        levels = [("Elementary", "elementary"), ("Middle", "middle"), ("High", "high")]
        
        select_frame = Frame(window, bg="white", borderwidth=5)
        select_frame.place(relwidth=0.9, relheight=0.4, relx=0.05, rely=0.4)

        for text, val in levels:
            Radiobutton(select_frame, text=text, variable=school_level, value=val, bg="white").pack(anchor=W, pady=5)

        # Confirm 버튼
        def confirm_selection():
            selected_level = school_level.get()
            print(f"Selected Level: {selected_level}")  # 디버깅용 출력
            # OpenWindow 호출
            # open_window = OpenWindow(selected_level, frame_entry)
            # open_window.ChapterWindow()

            new_root = Toplevel(window)  # 부모 창은 기존 window
            app = ChapterApp(new_root, school=selected_level)  # 선택된 level 전달
            new_root.mainloop()  # 이벤트 루프 실행


        Button(select_frame, text="Confirm", bg='white', command=confirm_selection).pack(pady=10)

    else:
        indicateLabel = Label(frame_entry, text=f"Enter {value} ID")
        indicateLabel.pack(anchor=W)

        global selectedEntry        
        selectedEntry = Entry(frame_entry)
        selectedEntry.pack(anchor=W)

        open_window = OpenWindow(selectedEntry, frame_entry)

        if value == "Test":
            selectedEntry.bind("<Return>", lambda event: open_window.TestWindow())
        else:
            selectedEntry.bind("<Return>", lambda event: open_window.LearnerWindow())
        

window = Tk()


window.geometry("600x500")
window.title("Title")
window.resizable(0, 0)


frame_button = Frame(window, bg="white", borderwidth=5)
frame_button.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.1)


modes = [
    ("Chapter Analysis", "Chapter"),
    ("Test Analysis", "Test"),
    ("Learner Analysis", "Learner")
]

analysis = StringVar()
analysis.set("Chapter Analysis")

for idx, (analy, mode) in enumerate(modes):
    Radiobutton(frame_button, text=analy, variable=analysis, value=mode,
                command=lambda: analysis_selected(analysis.get())).grid(row=0, column=5*idx, padx=5, pady=8)
    


window.mainloop()