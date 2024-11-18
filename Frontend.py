from tkinter import *
from OpenWindow import OpenWindow


def analysis_selected(value):
    
    global frame_entry
    frame_entry = Frame(window, bg="white", borderwidth=5)
    frame_entry.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.3)


    if value == "Chapter":
        open_window = OpenWindow(None, frame_entry)
        open_window.ChapterWindow()
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