from tkinter import *
from AnalysisPackage.AnalysisChapter import ResultsPage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ConnectDatabase import connect_db
from tkinter import messagebox

class testAnalysis:

    def __init__(self, test_window, testID):
        self.root = test_window
        test_window.attributes('-fullscreen', True)
        self.testID = testID

        # 레이아웃 비율 설정
        test_window.grid_rowconfigure(0, weight=1)  # 한 행
        test_window.grid_columnconfigure(0, weight=7)  # 좌측 70%
        test_window.grid_columnconfigure(1, weight=3)  # 우측 30%

        self.db_connection = connect_db()  # 기존 함수 대신 Login의 함수 사용
        if not self.db_connection:
            raise Exception("Database connection failed!")


        # 좌측 시각화 프레임 (70%)
        self.visual_frame = Frame(test_window, bg='lightblue')
        self.visual_frame.grid(row=0, column=0, sticky="nsew")

        # 우측 챕터 프레임 (30%)
        self.chapter_frame = Frame(test_window, bg='azure')
        self.chapter_frame.grid(row=0, column=1, sticky="nsew")

        # 챕터 프레임에 스크롤 추가
        self.chapter_canvas = Canvas(self.chapter_frame, bg='azure')
        self.chapter_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.chapter_scrollbar = Scrollbar(self.chapter_frame, orient="vertical", command=self.chapter_canvas.yview)
        self.chapter_scrollbar.pack(side=RIGHT, fill=Y)

        self.chapter_canvas.configure(yscrollcommand=self.chapter_scrollbar.set)
        self.chapter_inner_frame = Frame(self.chapter_canvas, bg='azure')
        self.details_window = Toplevel(self.root)
        self.chapter_canvas.create_window((0, 0), window=self.chapter_inner_frame, anchor="nw")

        self.chapter_inner_frame.bind("<Configure>", lambda e: self.chapter_canvas.configure(scrollregion=self.chapter_canvas.bbox("all")))

        self.check_knowledge()
        self.calculate_correct_ratio()

    def check_knowledge(self):

        query = """
            SELECT DISTINCT k.id, k.name
            FROM testIRT t
            JOIN knowledge k ON t.knowledgeTag = k.id
            WHERE t.testID = %s
        """

        cursor = self.db_connection.cursor()
        cursor.execute(query, (self.testID,))
        results = cursor.fetchall()

        if not results:
            Label(self.chapter_inner_frame, text="No knowledge information found.", font=("Arial", 14)).grid(row=0, column=0, pady=20)
            return

        # Display knowledge information in the main window
        Label(self.chapter_inner_frame, text="Knowledge Details", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20)
        Label(self.chapter_inner_frame, text="Relevant Chapters", font=("Arial", 16), wraplength=600, justify="left").grid(row=1, column=0, pady=10, sticky="w")
        
        row_cnt=2
        for row in results:
            knowledge_id, name = row
        
            # Show knowledge summary
            Label(self.chapter_inner_frame, text=name, font=("Arial", 12), wraplength=600, justify="left").grid(row=row_cnt, column=0, pady=10, sticky="w")
            # Add button to navigate to the details page

            Button(
                self.chapter_inner_frame,
                text="see more",
                command=lambda k_id=knowledge_id: self.show_details(k_id)
            ).grid(row=row_cnt, column=1, pady=5)
            row_cnt += 1

    def show_details(self,knowledge_id):

        # Fetch knowledge details
        query = """
            SELECT name, chapter_lv1, chapter_lv2, chapter_lv3
            FROM knowledge
            WHERE id = %s
        """

        cursor = self.db_connection.cursor()
        cursor.execute(query, (knowledge_id,))
        result = cursor.fetchone()

        if result:
            name, chapter_lv1, chapter_lv2, chapter_lv3 = result
            print(chapter_lv1)
            print(chapter_lv2)
            print(chapter_lv3)

            details_window = Toplevel(self.root)
            details_window.geometry("800x600")


        # 바로 show_details_page 호출
            results_instance = ResultsPage(
                root=details_window,
                db_connection=self.db_connection,
                chapter_lv1=chapter_lv1,
                chapter_lv2=chapter_lv2,
                chapter_lv3=chapter_lv3,
                create_page=False
            )
            results_instance.show_details_page(details_window, name)
            
        else:
                messagebox.showwarning(title="Warning",message="No details found for this knowledge.")
        cursor.close()

    def calculate_correct_ratio(self):
        query1 = f"""CREATE OR REPLACE VIEW itemcorrectRatio AS
                     SELECT RIGHT(aC.assessmentItemID, 2) AS problemNumber, k.name,
                            t.difficultyLevel, 
                            t.discriminationLevel, 
                            SUM(aC.answerCode)/COUNT(*) AS correctRatio
                     FROM answerCode aC
                     JOIN testIRT t ON aC.assessmentItemID = t.assessmentItemID
                     JOIN knowledge k ON t.knowledgeTag = k.id
                     WHERE aC.testID="{self.testID}"
                     GROUP BY aC.assessmentItemID, t.difficultyLevel, t.discriminationLevel, k.name
                     ORDER BY aC.assessmentItemID ASC"""
        
        query2 = "SELECT * FROM itemcorrectRatio"

        cursor = self.db_connection.cursor()
        cursor.execute(query1)
        cursor.execute(query2)

        result = cursor.fetchall()  # Fetch query2 results
        
        # Extract data for visualization and chapters
        problem_numbers = [row[0] for row in result]  # Question number
        chapter_names = [row[1] for row in result]
        discrimination_levels = [row[2] for row in result]
        difficulty_levels = [row[3] for row in result]
        correct_ratios = [row[4] for row in result]  # Correct Ratio

        # 시각화 표시
        self.show_test_chart(problem_numbers, discrimination_levels, difficulty_levels, correct_ratios)

    def show_test_chart(self, problem_numbers, discrimination_levels, difficulty_levels, correct_ratios):
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 첫 번째 Y축: Correct Ratio (막대그래프)
        ax1.set_title('Correct Ratio, Discrimination, and Difficulty Levels by Problem', fontsize=14)
        ax1.set_xlabel('Problem Number', fontsize=12)
        ax1.set_ylabel('Correct Ratio', fontsize=12, color='dodgerblue')
        bars = ax1.bar(problem_numbers, correct_ratios, color='dodgerblue', alpha=0.7, label='Correct Ratio')
        ax1.tick_params(axis='y', labelcolor='dodgerblue')
        ax1.set_ylim(0, 1)  # Correct Ratio는 0 ~ 1 범위

        # 두 번째 Y축: Discrimination Level과 Difficulty Level (꺾은선그래프)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Discrimination / Difficulty Levels', fontsize=12, color='black')
        ax2.plot(problem_numbers, discrimination_levels, marker='o', color='red', label='Discrimination Level', linewidth=2)
        ax2.plot(problem_numbers, difficulty_levels, marker='s', color='green', label='Difficulty Level', linewidth=2)
        ax2.tick_params(axis='y', labelcolor='black')

        # 그래프 범례 추가
        fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

        # Tkinter에 그래프 삽입
        canvas = FigureCanvasTkAgg(fig, master=self.visual_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)




"""
첫 화면에서 학년을 입력 
-> 1) 학년 전체 학생들 정보
-> 2) 드롭다운 박스로 개인 학생 정보

1) 
8학년 학생에 대해서
- theta(이해도 평균)
- 부족한 단원 (더 가르쳐야 될 단원 추천)
- 잘 하는 단원 (더 가르칠 필요가 없는 단원 추천)??
- 성별에 따른 이해도 평균
"""