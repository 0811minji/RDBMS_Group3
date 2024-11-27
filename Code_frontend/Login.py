from tkinter import *
from Teacher import open_teacher_window

def create_pwEntry():
    pwEntry = Entry(window)
    pwEntry.pack()

    pwEntry.bind("<Return>", lambda event: open_teacher_window())

    if idEntry == "ddd" and pwEntry == "ddd":
        open_teacher_window()
    '''
    elif idEntry+'*'==pwEntry: #regex로 id 조건 추가
        open_learner_window()
    '''

window = Tk()

window.geometry("600x500")
window.title("Math")

idEntry = Entry(window)
idEntry.pack()

idEntry.bind("<Return>", lambda event: create_pwEntry())

window.mainloop()