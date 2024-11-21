import mysql.connector
from tkinter import *
from tkinter import ttk
from AnalysisPackage.DisplayResult import displayResult


def connect_DB():

    myDB = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="tjsgud8871!",
        database="math"
    )

    return myDB

class testAnalysis:

    def __init__(self, test_window, testID):
        self.test_window = test_window
        self.testID = testID

    def check_knowledge(self):

        query = f"""SELECT `name`, semester, `description`, `chapter.name`
                    FROM knowledge k
                    WHERE id IN (SELECT DISTINCT(KnowledgeTag) FROM testIRT WHERE testID='{self.testID}')
                    ORDER BY id ASC"""
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query)

        result = myCursor.fetchall()

        label = Label(self.test_window, text="knowledge")
        label.grid(row=1, column=0)

        columns = myCursor.column_names
        
        display_result = displayResult(self.test_window, result, columns)
        display_result.knowledge()
        
        myDB.close()

    def calculate_correct_ratio(self):

        query1 = f"""CREATE OR REPLACE VIEW itemcorrectRatio AS
                    SELECT aC.assessmentItemID, t.difficultyLevel, t.discriminationLevel, SUM(aC.answerCode)/COUNT(*) AS correctRatio
                    FROM answerCode aC
                    JOIN testIRT t
                    ON aC.assessmentItemID=t.assessmentItemID
                    WHERE aC.testID="{self.testID}"
                    GROUP BY aC.assessmentItemID, t.difficultyLevel, t.discriminationLevel
                    ORDER BY aC.assessmentItemID ASC"""
        
        query2 = "SELECT * FROM itemcorrectRatio"

        query3 = """SELECT AVG(correctRatio) AS testcorrectRatio
                    FROM itemcorrectRatio"""
        
        myDB = connect_DB()
        myCursor = myDB.cursor()

        myCursor.execute(query1)
        myCursor.execute(query2)

        result = myCursor.fetchall()

        label = Label(self.test_window, text="correct ratio")
        label.grid(row=21, column=0)

        columns = myCursor.column_names
        
        display_result = displayResult(self.test_window, result, columns)
        display_result.others(2)
        
        myCursor.execute(query3)

        result = myCursor.fetchone()

        label = Label(self.test_window, text="average correct ratio")
        label.grid(row=31, column=0)

        columns = myCursor.column_names

        display_result = displayResult(self.test_window, result, columns)
        display_result.others(3)


        myDB.close()