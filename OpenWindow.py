from tkinter import *
from AnalysisPackage.AnalysisTest import testAnalysis


class OpenWindow:

    def __init__(self, selectedEntry, frame_entry):
        self.selected = selectedEntry
        self.frame_entry = frame_entry

    def ChapterWindow(self):

        top = Toplevel()
        top.geometry("600x500")
        top.title("Chapter Analysis")
        label = Label(top, text="Chapter")
        label.pack()


    def TestWindow(self):

        testID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.geometry("600x500")
        top.title(f"Test Analysis")
        label = Label(top, text=testID)
        label.grid(row=0, column=0)
        test_analysis = testAnalysis(top, testID)
        test_analysis.check_knowledge()
        test_analysis.calculate_correct_ratio()

    def LearnerWindow(self, event):

        learnerID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.geometry("600x500")
        top.title("Learner Analysis")
        label = Label(top, text=learnerID)
        label.grid(row=0, column=0)