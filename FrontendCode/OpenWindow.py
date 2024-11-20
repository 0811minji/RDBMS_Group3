from tkinter import *
from AnalysisPackage.AnalysisTest import testAnalysis


class OpenWindow:

    def __init__(self, selectedEntry, frame_entry):
        self.selected = selectedEntry
        self.frame_entry = frame_entry
        self._set_fullscreen()

    def _set_fullscreen(self):
        """Set the window to fullscreen mode based on the platform."""
        import platform
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

    def ChapterWindow(self):

        top = Toplevel()
        #top.geometry("600x500")
        top.title("Chapter Analysis")
        label = Label(top, text="Chapter")
        label.pack()


    def TestWindow(self):

        testID = self.selected.get()

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

        top = Toplevel()
        #top.geometry("600x500")
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
        #top.geometry("600x500")
        top.title("Learner Analysis")
        label = Label(top, text=learnerID)
        label.grid(row=0, column=0)

