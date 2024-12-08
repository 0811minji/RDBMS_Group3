import platform
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from AnalysisPackage.AnalysisChapter import ResultsPage

from ConnectDatabase import connect_db

bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

class learnerAnalysis:

    def __init__(self, learner_window, learner_grade, own_ID=None):
        self.learner_window = learner_window
        self.frame_entry = Frame(self.learner_window, bg=bg_color_2, borderwidth=5)
        self.width = self.learner_window.winfo_screenwidth()
        self.learner_window.attributes('-fullscreen', True)
        
        self.learner_grade = None

        if not isinstance(learner_grade, int):
            if learner_grade.startswith("Elementary"):
                self.learner_grade = learner_grade[-1]
            elif learner_grade.startswith("Middle"):
                self.learner_grade = str(6 + int(learner_grade[-1]))
        else:
            self.learner_grade = str(learner_grade)

        self.own_ID = own_ID
        self.selected_learnerID = StringVar()
        self.selected_testID = StringVar()
        self.selected_name = StringVar()
        self.learnerID = None
        self.final_name = None

    def setting(self):

        self.frame_entry.grid(row=1, column=0, padx=0.05*self.width, pady=30, sticky="nsew")

        for widget in self.frame_entry.winfo_children():
            widget.destroy()

    def check_testInfo(self):

        query1 = f"""CREATE OR REPLACE VIEW selectedLearner AS
                    SELECT aC.learnerID, aC.testID, aC.assessmentItemID, aC.answerCode, lI.theta, lI.realScore
                    FROM answerCode aC
                    JOIN learnerIRT lI
                    ON aC.learnerID=lI.learnerID
                    WHERE aC.learnerID='{self.learnerID}'
                    ORDER BY aC.learnerID ASC, aC.testID ASC, aC.assessmentItemID ASC"""
        
        query2 = f"""CREATE OR REPLACE VIEW testKnowledge AS
                    SELECT DISTINCT(t.testID), `name`, semester, `description`, `chapter.name`
                    FROM knowledge k
                    JOIN testIRT t
                    ON k.id=t.knowledgetag
                    WHERE k.id IN (SELECT DISTINCT(KnowledgeTag) FROM testIRT t 
                                WHERE t.testID IN (SELECT DISTINCT(testID) FROM selectedLearner))
                    ORDER BY t.testID ASC"""
        
        db_connection = connect_db()
        myCursor = db_connection.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)

        db_connection.close()


    def check_theta(self):

        query1 = f"""CREATE OR REPLACE VIEW Gradetheta AS
                    SELECT lI.learnerID, AVG(lI.theta) AS avgtheta
                    FROM learnerIRT lI
                    WHERE lI.learnerID LIKE 'A0{self.learner_grade}%'
                    GROUP BY lI.learnerID
                    ORDER BY lI.learnerID ASC"""
        
        query2 = """SELECT l.gender, AVG(Gt.avgtheta) AS genderavgtheta
                    FROM Gradetheta Gt
                    JOIN learner l
                    ON Gt.learnerID=l.learnerID
                    GROUP BY l.gender"""
        
        query3 = f"""CREATE OR REPLACE VIEW GradetestKnowledge AS
                    SELECT k.`name`, k.id, AVG(lI.theta) AS avgtheta
                    FROM learnerIRT lI
                    JOIN testIRT tI
                    ON lI.testID=tI.testID
                    JOIN knowledge k
                    ON k.id=tI.knowledgetag
                    WHERE lI.learnerID LIKE 'A0{self.learner_grade}%'
                    GROUP BY k.`name`, k.id
                    ORDER BY k.`name` ASC"""
        
        query4 = f"""CREATE OR REPLACE VIEW GtKthetaCDF AS
                    SELECT `name`,id, avgtheta, CUME_DIST() OVER (ORDER BY avgtheta) AS thetaCDF
                    FROM GradetestKnowledge
                    ORDER BY thetaCDF ASC, `name` ASC"""
        
        query5 = """SELECT * FROM GtKthetaCDF
                    WHERE thetaCDF>0.95"""
        
        query6 = """SELECT * FROM GtKthetaCDF
                    WHERE thetaCDF<0.05"""
        
        
        db_connection = connect_db()
        myCursor = db_connection.cursor()
        
        myCursor = db_connection.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)
        
        result = myCursor.fetchall()

        columns = myCursor.column_names

        theta_data = {column: [] for column in columns}

        for row in result:
            for idx, column in enumerate(columns):
                theta_data[column].append(row[idx])

        myCursor.execute(query3)
        myCursor.execute(query4)
        myCursor.execute(query5)

        top_result = myCursor.fetchall()

        columns = myCursor.column_names

        top_data = {column: [] for column in columns}

        for row in top_result:
            for idx, column in enumerate(columns):
                top_data[column].append(row[idx])

        myCursor.execute(query6)

        bottom_result = myCursor.fetchall()

        columns = myCursor.column_names

        bottom_data = {column: [] for column in columns}

        for row in bottom_result:
            for idx, column in enumerate(columns):
                bottom_data[column].append(row[idx])

        db_connection.close()

        self.setting()
        
        self.frame_entry.grid_rowconfigure(0, weight=1)
        self.frame_entry.grid_rowconfigure(1, weight=1)
        self.frame_entry.grid_columnconfigure(0, weight=55)
        self.frame_entry.grid_columnconfigure(1, weight=45)

        bar_graph_frame = Frame(self.frame_entry, bg=bg_color)
        bar_graph_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        top_chapter_frame = Frame(self.frame_entry, bg=bg_color)
        top_chapter_frame.grid(row=0, column=1, sticky="nsew")
        bottom_chapter_frame = Frame(self.frame_entry, bg=bg_color_2)
        bottom_chapter_frame.grid(row=1, column=1, sticky="nsew")

        categories =  ['Female', 'Male', 'All']
        all = sum(theta_data['genderavgtheta'])/2
        values = theta_data['genderavgtheta']+[all]
        fig1 = Figure(figsize=(8, 6), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.set_ylim(-0.6, 0.6)
        ax1.bar(categories, values,
               color=['#DA8359', '#A5B68D', text_color], width=0.4)

        # 축 설정
        ax1.set_ylabel('Average Comprehension Level')
        ax1.set_title('Average Comprehension for Selected Grade')

        # Matplotlib Figure를 Tkinter Canvas에 추가
        canvas = FigureCanvasTkAgg(fig1, bar_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        top_label = Label(
            top_chapter_frame,
            text="Top Average Comprehension",
            font=('Helevetica', 18, "bold"),
            fg=text_color,
            bg=bg_color
        )
        top_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        
        for idx in range(len(top_data)):
            
            more_info = Button(
            top_chapter_frame,
            text=top_data['name'][idx], 
            command=lambda: self.show_details((top_data['id'][idx],)),
            bg=button_color,
            fg=text_color,
            font=('Helevetica', 14, "bold"),
            relief=RAISED
            )
            more_info.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")
        
        bottom_label = Label(bottom_chapter_frame, text="Bottom Average Comprehension", font=('Helevetica', 18, "bold"), fg=text_color, bg=bg_color_2)
        bottom_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        for idx in range(len(bottom_data['name'])):
            
            more_info_b = Button(
            bottom_chapter_frame,
            text=bottom_data['name'][idx], 
            command=lambda: self.show_details((bottom_data['id'][idx],)),
            bg=button_color,
            fg=text_color,
            font=('Helevetica', 14, "bold"),
            relief=RAISED
            )
            more_info_b.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")
            # knowledge_label = Label(bottom_chapter_frame, text=bottom_data['name'][idx], fg=text_color, bg=bg_color_2, font=('Helevetica', 16))
            # knowledge_label.grid(row=idx+1, column=0, padx=10, pady=5, sticky="w")

    def learnerID_options(self):

        if self.own_ID is not None:
            return self.own_ID
        
        else:
            db_connection= connect_db()
            myCursor = db_connection.cursor()

            query_learnerID = f"""SELECT DISTINCT(learnerID)
                                FROM learner
                                WHERE learnerID LIKE 'A0{self.learner_grade}%'"""

            myCursor.execute(query_learnerID)

            result = myCursor.fetchall()
            
            db_connection.close()
            
            return [row[0] for row in result]


    def testID_options(self):
        
        self.learnerID = self.selected_learnerID.get()
        self.check_testInfo()

        db_connection = connect_db()
        myCursor = db_connection.cursor()

        query_testID = "SELECT DISTINCT(testID) FROM selectedLearner ORDER BY testID ASC"

        myCursor.execute(query_testID)

        result = myCursor.fetchall()

        self.combo_testID['values'] = [row[0] for row in result]
    
    def name_options(self):

        db_connection = connect_db()
        myCursor = db_connection.cursor()

        testID = self.selected_testID.get()

        query_name = f"""SELECT `name` FROM testKnowledge
                        WHERE testID='{testID}'
                        ORDER BY `name` ASC"""

        myCursor.execute(query_name)

        result = myCursor.fetchall()

        self.combo_name['values'] = [row[0] for row in result]

        db_connection.close()

    def selected_option(self, event):

        self.final_name = self.selected_name.get()
        self.final_name = self.final_name.replace("\\", "\\\\")

    def select_name(self):

        Label(self.select_frame, text="learnerID", fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self.select_frame, text="testID", fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Label(self.select_frame, text="knowledge name", fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        combo_learner = ttk.Combobox(self.select_frame, textvariable=self.selected_learnerID, state="readonly")
        combo_learner['values'] = self.learnerID_options()
        combo_learner.grid(row=0, column=1, padx=10, pady=10)
        combo_learner.bind("<<ComboboxSelected>>", lambda event: self.testID_options())
                
        self.combo_testID = ttk.Combobox(self.select_frame, textvariable=self.selected_testID, state="readonly")
        self.combo_testID.grid(row=1, column=1, padx=10, pady=10)
        self.combo_testID.bind("<<ComboboxSelected>>", lambda event: self.name_options())

        self.combo_name = ttk.Combobox(self.select_frame, textvariable=self.selected_name, state="readonly")
        self.combo_name.grid(row=2, column=1, padx=10, pady=10)
        self.combo_name.bind("<<ComboboxSelected>>", lambda event: self.selected_option(event))

        Button(
            self.select_frame,
            text="Confirm",
            command=self.calculate_correctRatio,
            bg=bg_color,
            fg=text_color,
            activebackground=text_color,
            font=('Helevetica', 14)
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_correctRatio(self):

        query1 = """CREATE OR REPLACE VIEW testcorrectRatio AS
                    SELECT tI.testId, aC.learnerID, SUM(aC.answerCode)/COUNT(*) AS correctRatio
                    FROM answerCode aC
                    JOIN testIRT tI
                    ON aC.assessmentItemID=tI.assessmentItemID
                    WHERE aC.testID IN (SELECT testID FROM selectedLearner)
                    GROUP BY tI.testID, aC.learnerID
                    ORDER BY tI.testID, aC.learnerID ASC"""

        query2 = """CREATE OR REPLACE VIEW AVGtestcorrectRatio AS
                    SELECT testID, AVG(correctRatio) AS avgtestcorrectRatio
                    FROM testcorrectRatio
                    GROUP BY testID
                    ORDER BY testID"""
        
        query3 = """CREATE OR REPLACE VIEW testcorrectratioCDF AS
                    SELECT tcR.learnerID, tcR.testID, avgtcR.avgtestcorrectRatio, tcR.correctRatio,
                        CUME_DIST() OVER (PARTITION BY testID ORDER BY correctRatio) AS correctRatioCDF
                    FROM testcorrectRatio tcR
                    JOIN AVGtestcorrectRatio avgtcR
                    ON tcR.testID=avgtcR.testID
                    ORDER BY testID ASC, learnerID ASC"""
        
        query4 = f"""CREATE OR REPLACE VIEW testknowledgecorrectratioCDF AS
                    SELECT DISTINCT(tcrCDF.testID), tK.`name`, tcrCDF.avgtestcorrectRatio, tcrCDF.correctRatio, tcrCDF.correctRatioCDF
                    FROM testcorrectratioCDF tcrCDF
                    JOIN testKnowledge tK
                    ON tcrCDF.testID=tK.testID
                    WHERE learnerID='{self.learnerID}'"""
        
        query5 = f"""SELECT * FROM testknowledgecorrectratioCDF
                    WHERE `name`='{self.final_name}'"""

        db_connection = connect_db()
        myCursor = db_connection.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)
        myCursor.execute(query3)
        myCursor.execute(query4)
        myCursor.execute(query5)

        result = myCursor.fetchall()

        columns = myCursor.column_names

        db_connection.close()

        data = {column: [] for column in columns}

        for row in result:
            for idx, column in enumerate(columns):
                data[column].append(row[idx])


        self.draw_graph(data)
    
    def show_details(self,knowledge_id):

        # Fetch knowledge details
        query = """
            SELECT name, chapter_lv1, chapter_lv2, chapter_lv3
            FROM knowledge
            WHERE id = %s
        """
        db_connection = connect_db()
        cursor = db_connection.cursor()
        cursor.execute(query, knowledge_id)
        result = cursor.fetchone()

        if result:
            name, chapter_lv1, chapter_lv2, chapter_lv3 = result
            print(chapter_lv1)
            print(chapter_lv2)
            print(chapter_lv3)

            details_window = Toplevel(self.learner_window)
            details_window.geometry("800x600")
            details_window.configure(bg=bg_color)


        # 바로 show_details_page 호출
            results_instance = ResultsPage(
                root=details_window,
                db_connection=db_connection,
                chapter_lv1=chapter_lv1,
                chapter_lv2=chapter_lv2,
                chapter_lv3=chapter_lv3,
                create_page=False
            )
            results_instance.show_details_page(details_window, name)
            
        else:
                messagebox.showwarning(title="Warning",message="No details found for this knowledge.")
        cursor.close()

    def draw_graph(self, data):

        #self.final_name에 해당하는 단원 정보를 chapteranalysis에서 받아옴.

        global more_info
        
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        try:
            more_info.destroy()
        except:
            pass
        
        query6 = f"SELECT id FROM knowledge WHERE name LIKE '{self.final_name}'"
        db_connection = connect_db()
        myCursor = db_connection.cursor()
        myCursor.execute(query6)
        k_id = myCursor.fetchone()
        print(k_id)
        db_connection.close()

        more_info = Button(
            self.select_frame,
            text=f"See more about <{self.final_name}>",
            command=lambda: self.show_details(k_id),
            bg=button_color,
            fg=text_color,
            font=('Helevetica', 14, "bold"),
            relief=RAISED
        )
        more_info.grid(row=5, column=1, padx=10, pady=10)
        

        x = data['testID']
        line_y = np.array(data['avgtestcorrectRatio']) * 100
        bar1_y = np.array(data['correctRatio']) * 100
        bar2_y = np.array(data['correctRatioCDF']) * 100
        

        fig2, ax21 = plt.subplots(figsize=(8, 8))
        ax22 = ax21.twinx()

        binwidth=0.1
        ax22.bar(np.arange(len(x))-binwidth/2, bar1_y, label=f'{self.learnerID} correct ratio', color=button_color, alpha=0.7)

        ax21.bar(np.arange(len(x))+binwidth/2, bar2_y, label=f'{self.learnerID} correct ratio CDF', color='darkgreen', alpha=0.7)

        ax22.plot(x, line_y, marker='o', color=text_color, label='average correct ratio')

        ax22.set_xticks(np.arange(len(x)))
        ax22.set_xticklabels(x, rotation=10)

        ax22.set_xlabel('testID')
        ax22.set_ylabel('correct ratio')
        ax22.set_ylim(0, 100)
        ax21.set_ylabel('CDF')
        ax22.yaxis.set_label_position("right")

        fig2.legend(loc="upper right", bbox_to_anchor=(1,1))

        plt.title('Correct Ratio Analysis')

        canvas = FigureCanvasTkAgg(fig2, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def view_correctRatio(self):

        self.setting()

        self.frame_entry.grid_rowconfigure(0, weight=1)
        self.frame_entry.grid_columnconfigure(0, weight=3)
        self.frame_entry.grid_columnconfigure(1, weight=7)

        self.select_frame = Frame(self.frame_entry, bg=bg_color_2)
        self.select_frame.grid(row=0, column=0, sticky="nsew")

        self.graph_frame = Frame(self.frame_entry, bg=bg_color_2)
        self.graph_frame.grid(row=0, column=1, sticky="nsew")
        
        self.select_name()

    def return_feedback(self):
        self.learnerID = self.combo_feedback.get()
        
        query1 = f"""SELECT feedback
                    FROM learner
                    WHERE learnerID='{self.learnerID}'"""
        
        
        db_connection = connect_db()
        myCursor = db_connection.cursor()
        
        myCursor = db_connection.cursor()

        myCursor.execute(query1)
        result = myCursor.fetchall()
        feedback = result[0][0]

        Label(self.frame_entry, text="Feedback", fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        Label(self.frame_entry, text=feedback, fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=1, column=1, padx=10, pady=10, sticky="nw")

    def check_feedback(self):

        self.setting()

        self.frame_entry.grid_rowconfigure(0, weight=2)
        self.frame_entry.grid_rowconfigure(1, weight=8)
        self.frame_entry.grid_columnconfigure(0, weight=2)
        self.frame_entry.grid_columnconfigure(1, weight=8)
        
        Label(self.frame_entry, text="learnerID", fg=text_color, bg=bg_color_2, font=('Helevetica', 16)).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.combo_feedback = ttk.Combobox(self.frame_entry, textvariable=self.selected_learnerID, state="readonly")
        self.combo_feedback['values'] = self.learnerID_options()
        self.combo_feedback.grid(row=0, column=1, padx=5, pady=10, sticky="nw")
        self.combo_feedback.bind("<<ComboboxSelected>>", lambda event: self.return_feedback())