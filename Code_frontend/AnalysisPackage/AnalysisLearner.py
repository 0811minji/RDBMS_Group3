import mysql.connector
from tkinter import *
from AnalysisPackage.DisplayResult import displayResult


def connect_DB():

    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="tjsgud8871!",
        database="math"
    )

    return myDB

class learnerAnalysis:

    def __init__(self, learner_window, learnerID):

        self.learner_window = learner_window
        self.learnerID = learnerID
        self.frame_entry = Frame(self.learner_window, bg="white", borderwidth=5)

    def setting(self):

        self.frame_entry.place(relwidth=0.9, relheight=0.65, relx=0.05, rely=0.3)
        
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
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query1)

        myCursor.fetchall()

        myDB.close()

    def check_testKnowledge(self):

        self.setting()
        self.check_testInfo()

        query1 = f"""CREATE OR REPLACE VIEW testKnowledge AS
                    SELECT DISTINCT(t.testID), `name`, semester, `description`, `chapter.name`
                    FROM knowledge k
                    JOIN testIRT t
                    ON k.id=t.knowledgetag
                    WHERE k.id IN (SELECT DISTINCT(KnowledgeTag) FROM testIRT t 
                                WHERE t.testID IN (SELECT DISTINCT(testID) FROM selectedLearner))
                    ORDER BY t.testID ASC"""

        query2 = """SELECT * FROM testKnowledge"""
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)

        result = myCursor.fetchall()

        label = Label(self.frame_entry, text="test knowledge")
        label.grid(row=1, column=0)

        columns = myCursor.column_names

        display_result = displayResult(self.frame_entry, result, columns)
        display_result.knowledge()
        
        myDB.close()


    def check_theta(self):

        self.setting()
        self.check_testInfo()

        query1 = """CREATE OR REPLACE VIEW AVGtheta AS
                    SELECT tK.`name`, tK.`chapter.name`, AVG(lI.theta) AS averagetheta
                    FROM learnerIRT lI
                    JOIN testKnowledge tK
                    ON lI.testID=tK.testID
                    WHERE tK.testID IN (SELECT testID FROM selectedLearner)
                    GROUP BY tK.`name`, tK.`chapter.name`
                    ORDER BY tK.`name`"""

        query2 = """CREATE OR REPLACE VIEW thetaCDF AS
                    SELECT lI.learnerID, tK.`name`, tK.`chapter.name`, lI.testID, avgt.averagetheta, lI.theta, CUME_DIST() OVER (PARTITION BY tK.`name` ORDER BY theta) AS thetaCDF
                    FROM learnerIRT lI
                    JOIN testKnowledge tK
                    ON lI.testID=tK.testID
                    JOIN AVGtheta avgt
                    ON tk.`name`=avgt.`name`
                    WHERE tK.testID IN (SELECT testID FROM selectedLearner)
                    ORDER BY tK.`name` ASC, tk.testID ASC"""
        
        query3 = f"""SELECT `name`, `chapter.name`, testID, averagetheta, theta, thetaCDF FROM thetaCDF
                    where learnerID='{self.learnerID}'"""
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)
        myCursor.execute(query3)

        result = myCursor.fetchall()

        label = Label(self.frame_entry, text="theta CDF")
        label.grid(row=20, column=0)

        columns = myCursor.column_names

        display_result = displayResult(self.frame_entry, result, columns)
        display_result.others(1)

        myDB.close()

    def calculate_correctRatio(self):

        self.setting()
        self.check_testInfo()

        query1 = """CREATE OR REPLACE VIEW testcorrectRatio AS
                    SELECT tI.testId, aC.learnerID, AVG(tI.difficultyLevel) AS averagedifficulty, 
                        AVG(tI.discriminationLevel) AS averagediscrimination, SUM(aC.answerCode)/COUNT(*) AS correctRatio
                    FROM answerCode aC
                    JOIN testIRT tI
                    ON aC.assessmentItemID=tI.assessmentItemID
                    WHERE aC.testID IN (SELECT testID FROM selectedLearner)
                    GROUP BY tI.testID, aC.learnerID
                    ORDER BY tI.testID ASC, aC.learnerID ASC"""

        query2 = """CREATE OR REPLACE VIEW AVGtestcorrectRatio AS
                    SELECT testID, averagedifficulty, averagediscrimination, AVG(correctRatio) AS averagecorrectRatio
                    FROM testcorrectRatio
                    GROUP BY testID, averagedifficulty, averagediscrimination
                    ORDER BY testID"""
        
        query3 = """CREATE OR REPLACE VIEW testcorrectratioCDF AS
                    SELECT tcR.learnerID, tcR.testID, avgtcR.averagecorrectRatio, tcR.correctRatio, CUME_DIST() OVER (PARTITION BY testID ORDER BY correctRatio) AS correctRatioCDF
                    FROM testcorrectRatio tcR
                    JOIN AVGtestcorrectRatio avgtcR
                    ON tcR.testID=avgtcR.testID
                    ORDER BY testID ASC, learnerID ASC"""
        
        query4 = f"""SELECT testID, averagecorrectRatio, correctRatio, correctRatioCDF FROM testcorrectratioCDF
                    where learnerID='{self.learnerID}'"""
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)
        myCursor.execute(query3)
        myCursor.execute(query4)

        result = myCursor.fetchall()

        label = Label(self.frame_entry, text="theta CDF")
        label.grid(row=1, column=0)

        columns = myCursor.column_names

        display_result = displayResult(self.frame_entry, result, columns)
        display_result.others(1)

        myDB.close()
