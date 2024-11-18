import mysql.connector
from tkinter import *


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
        k = 0
        for cols in columns:
            res_label = Label(self.test_window, text = cols)
            res_label.grid(row=2, column=k)
            k+=1
        
        i = 2
        for res in result:
            for j in range(len(res)):
                print(res[j])
                res_label = Label(self.test_window, text=res[j])
                res_label.grid(row=i+1, column=j)
            i+=1
        
        myDB.close()

    def calculate_correct_ratio(self): # label 이름 구분 짓기

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
        k = 0
        for cols in columns:
            res_label = Label(self.test_window, text = cols)
            res_label.grid(row=22, column=k)
            k+=1
        
        i = 22
        for res in result:
            for j in range(len(res)):
                print(res[j])
                res_label = Label(self.test_window, text=res[j])
                res_label.grid(row=i+1, column=j)
            i+=1
        
        myCursor.execute(query3)

        result = myCursor.fetchone()

        label = Label(self.test_window, text="average correct ratio")
        label.grid(row=41, column=0)
        
        label = Label(self.test_window, text=result)
        label.grid(row=41, column=1)


        myDB.close()