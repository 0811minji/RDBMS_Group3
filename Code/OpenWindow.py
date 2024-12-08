import platform
from tkinter import *
from AnalysisPackage.AnalysisTest import testAnalysis
from AnalysisPackage.AnalysisLearner import learnerAnalysis

bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

def learner_analysis_selected(value):

    if value == "understanding":
        learner_analysis.check_theta()
    elif value == "correctRatio":
        learner_analysis.view_correctRatio()
    else:
        learner_analysis.check_feedback()

class OpenWindow:

    def __init__(self, selectedEntry, frame_entry):
        self.selected = selectedEntry
        self.frame_entry = frame_entry

    def _set_fullscreen(self):
        """Set the window to fullscreen mode based on the platform."""
        
        os_name = platform.system()
        
        if os_name == "Windows" or os_name == "Linux":
            # Windows/Linux: maximize the window
            try:
                self.root.state("zoomed")
            except Exception as e:
                print(f"Zoomed state failed: {e}")
                self.root.attributes("-fullscreen", True)
        
        elif os_name == "Darwin":  # macOS
            # macOS: use fullscreen attributes
            self.root.attributes("-fullscreen", True)
            # Adjust menubar visibility
            self.root.attributes("-topmost", True)

    def ChapterWindow(self): # 확인 후 제거

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.title("Chapter Analysis")
        top.configure(bg=bg_color)
        label = Label(top, text="Chapter", bg=bg_color, fg=text_color)
        label.pack()


    def TestWindow(self):

        testID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.geometry("1000x500")
        top.title(f"Test Analysis")
        top.configure(bg=bg_color)
        test_analysis = testAnalysis(top, testID)
        test_analysis.check_knowledge()
        #test_analysis.calculate_correct_ratio()

    def LearnerWindow(self):

        learner_grade = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.attributes('-fullscreen', True)
        top.title("Learner Analysis")
        top.configure(bg=bg_color)

        top.grid_rowconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=8)
        top.grid_columnconfigure(0, weight=1)

        width = top.winfo_screenwidth()
        
        global learner_analysis

        learner_analysis = learnerAnalysis(top, learner_grade)

        frame_button = Frame(top, borderwidth=5, bg=bg_color_2)
        frame_button.grid(row=0, column=0, padx=0.05*width, pady=25, sticky="nsew")

        modes = [
            ("Understanding", "understanding"),
            ("Correct Ratio", "correctRatio"),
            ("Feedback", "feedback")
        ]

        analysis = StringVar()
        analysis.set("Test Information")
        
        for idx, (analy, mode) in enumerate(modes):
                Radiobutton(frame_button, text=analy, variable=analysis, value=mode, bg=bg_color_2,
                            command=lambda: learner_analysis_selected(analysis.get())).grid(row=0, column=4*idx, padx=5, pady=8)