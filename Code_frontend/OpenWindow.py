import platform
from tkinter import *
from AnalysisPackage.AnalysisTest import testAnalysis
from AnalysisPackage.AnalysisLearner import learnerAnalysis

def learner_analysis_selected(value):

    if value == "knowledge":
        learner_analysis.check_testKnowledge()
    elif value == "theta":
        learner_analysis.check_theta()
    else:
        learner_analysis.calculate_correctRatio()

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
        label = Label(top, text="Chapter")
        label.pack()


    def TestWindow(self):

        testID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.geometry("1000x500")
        top.title(f"Test Analysis")
        label = Label(top, text=testID)
        label.grid(row=0, column=0)
        test_analysis = testAnalysis(top, testID)
        test_analysis.check_knowledge()
        test_analysis.calculate_correct_ratio()

    def LearnerWindow(self):

        learnerID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        top.geometry("1000x500")
        top.title("Learner Analysis")
        label = Label(top, text=learnerID)
        label.grid(row=0, column=0)
        
        global learner_analysis

        learner_analysis = learnerAnalysis(top, learnerID)

        frame_button = Frame(top, bg="white", borderwidth=5)
        frame_button.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.1)

        modes = [
            ("Test Knowledge", "knowledge"),
            ("Theta", "theta"),
            ("Correct Ratio", "correctRatio")
        ]

        analysis = StringVar()
        analysis.set("Test Information")
        
        for idx, (analy, mode) in enumerate(modes):
                Radiobutton(frame_button, text=analy, variable=analysis, value=mode, 
                            command=lambda: learner_analysis_selected(analysis.get())).grid(row=0, column=4*idx, padx=5, pady=8)