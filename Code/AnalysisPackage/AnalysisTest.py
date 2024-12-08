from tkinter import *
from AnalysisPackage.AnalysisChapter import ResultsPage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ConnectDatabase import connect_db
from tkinter import messagebox

# colour palette 
bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

class testAnalysis:

    def __init__(self, test_window, testID):
        self.root = test_window
        test_window.attributes('-fullscreen', True)
        self.testID = testID

        # 레이아웃 비율 설정
        test_window.grid_rowconfigure(0, weight=1)  # 한 행
        test_window.grid_columnconfigure(0, weight=7)  # 좌측 70%
        test_window.grid_columnconfigure(1, weight=3)  # 우측 30%

        self.db_connection = connect_db()
        if not self.db_connection:
            raise Exception("Database connection failed!")

        # 좌측 시각화 프레임 (70%)
        self.visual_frame = Frame(test_window, bg=bg_color)
        self.visual_frame.grid(row=0, column=0, sticky="nsew")

        # 우측 챕터 프레임 (30%)
        self.chapter_frame = Frame(test_window, bg=bg_color_2)
        self.chapter_frame.grid(row=0, column=1, sticky="nsew")

        # 챕터 프레임에 스크롤 추가
        self.chapter_canvas = Canvas(self.chapter_frame, bg=bg_color)
        self.chapter_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.chapter_scrollbar = Scrollbar(self.chapter_frame, orient="vertical", command=self.chapter_canvas.yview)
        self.chapter_scrollbar.pack(side=RIGHT, fill=Y)

        self.chapter_canvas.configure(yscrollcommand=self.chapter_scrollbar.set)
        self.chapter_inner_frame = Frame(self.chapter_canvas, bg=bg_color)
        #self.details_window = Toplevel(self.root)
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
            Label(self.chapter_inner_frame, text="No knowledge information found.",
                  font=('Helevetica', 14), fg=text_color, bg=bg_color).grid(row=0, column=0, pady=20)
            return

        # Display knowledge information in the main window
        Label(self.chapter_inner_frame, text="Knowledge Details", font=('Helevetica', 18, "bold"), fg=text_color, bg=bg_color).grid(row=0, column=0, pady=20)
        Label(self.chapter_inner_frame, text="Relevant Chapters", font=('Helevetica', 18), fg=text_color,bg=bg_color, wraplength=600, justify="left").grid(row=1, column=0, pady=10, sticky="w")
        
        row_cnt=2
        for row in results:
            knowledge_id, name = row
        
            # Show knowledge summary
            Label(self.chapter_inner_frame, text=name, font=('Helevetica', 16), 
                  fg=text_color,bg=bg_color, wraplength=600, justify="left").grid(row=row_cnt, column=0, pady=10, sticky="w")
            # Add button to navigate to the details page

            Button(
                self.chapter_inner_frame,
                text="see more",
                font=('Helevetica', 14),
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
            details_window.configure(bg=bg_color)


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
                     LEFT JOIN testIRT t ON aC.assessmentItemID = t.assessmentItemID
                     LEFT JOIN knowledge k ON t.knowledgeTag = k.id
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
        self.show_test_chart(problem_numbers, discrimination_levels, difficulty_levels, correct_ratios, chapter_names)

    def show_test_chart(self, problem_numbers, discrimination_levels, difficulty_levels, correct_ratios, chapter_names):
        # 그래프와 텍스트를 담을 서브 프레임 추가
        graph_frame = Frame(self.visual_frame, bg=bg_color)
        graph_frame.pack(fill=BOTH, expand=True, side=TOP)
        graph_frame.configure(height=int(self.visual_frame.winfo_height() * 0.6))

        text_frame = Frame(self.visual_frame, bg=bg_color_2)
        text_frame.pack(fill=BOTH, expand=True, side=BOTTOM)
        text_frame.configure(height=int(self.visual_frame.winfo_height() * 0.4))

        # 그래프 생성
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # 첫 번째 Y축: Correct Ratio (막대그래프)
        ax1.set_title('Correct Ratio, Discrimination, and Difficulty Levels by Problem', fontsize=14)
        ax1.set_xlabel('Problem Number', fontsize=12)
        ax1.set_ylabel('Correct Ratio', fontsize=12, color='black')
        bars = ax1.bar(problem_numbers, correct_ratios, color=button_color, alpha=0.7, label='Correct Ratio')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(0, 1)  # Correct Ratio는 0 ~ 1 범위

        # 두 번째 Y축: Discrimination Level과 Difficulty Level (꺾은선그래프)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Discrimination / Difficulty Levels', fontsize=12, color='black')
        ax2.plot(problem_numbers, discrimination_levels, marker='o', color=text_color, label='Discrimination Level', linewidth=2)
        ax2.plot(problem_numbers, difficulty_levels, marker='s', color='darkgreen', label='Difficulty Level', linewidth=2)
        ax2.invert_yaxis()
        ax2.tick_params(axis='y', labelcolor='black')

        # 그래프 범례 추가
        fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

        # Tkinter에 그래프 삽입
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # 분석 텍스트 추가
        # 오답률이 가장 높은 문제 번호와 단원명 추출
        low_correct_idx = correct_ratios.index(min(correct_ratios))  # Correct Ratio가 가장 낮은 문제의 인덱스
        low_correct_num = problem_numbers[low_correct_idx]
        low_correct_name = chapter_names[low_correct_idx]

        # 변별력이 가장 높은 문제 번호와 단원명 추출
        high_discrim_idx = discrimination_levels.index(max(discrimination_levels))  # Discrimination Level이 가장 높은 문제의 인덱스
        high_discrim_num = problem_numbers[high_discrim_idx]
        high_discrim_name = chapter_names[high_discrim_idx]

        # 단원별로 Difficulty Level의 평균 구하기
        chapter_difficulty_map = {}  # 단원별로 difficulty level을 저장할 딕셔너리
        for i, chapter in enumerate(chapter_names):
            if chapter not in chapter_difficulty_map:
                chapter_difficulty_map[chapter] = []
            chapter_difficulty_map[chapter].append(difficulty_levels[i])

        # 각 단원별 평균 Difficulty Level 계산
        chapter_avg_difficulty = {chapter: sum(values) / len(values) for chapter, values in chapter_difficulty_map.items()}

        # 가장 어려운 단원 (평균 Difficulty Level이 가장 높은 단원) 추출
        difficult_chapter_name = min(chapter_avg_difficulty, key=chapter_avg_difficulty.get)

        # 분석 텍스트 생성
        correctratio_text = f"The problem with the lowest correct ratio is < #{low_correct_num}>, and the related chapter is <{low_correct_name}>."
        discrimination_text = f"The problem with the highest discrimination level is < #{high_discrim_num}>, and the related chapter is <{high_discrim_name}>."
        hardest_chap_text = f"Students found the problems in the {difficult_chapter_name} chapter the most challenging in this test."

        # 텍스트를 분석 섹션에 추가
        analysis_section_label = Label(
            text_frame, text="TEST ANALYSIS",
            font=('Helevetica', 18, "bold"), fg=text_color, bg=bg_color_2,
            justify='left', wraplength=800
        )

        analysis_label1 = Label(
            text_frame, text=correctratio_text,
            font=('Helevetica', 16), fg=text_color, bg=bg_color_2,
            justify='left', wraplength=800
        )

        analysis_label2 = Label(
            text_frame, text=discrimination_text,
            font=('Helevetica', 16), fg=text_color, bg=bg_color_2,
            justify='left', wraplength=800
        )

        analysis_label3 = Label(
            text_frame, text=hardest_chap_text,
            font=('Helevetica', 16), fg=text_color, bg=bg_color_2,
            justify='left', wraplength=800
        )        

        analysis_section_label.grid(row=0, column=0, pady=10, padx=10)
        analysis_label1.grid(row=1, column=0, pady=10, padx=10)
        analysis_label2.grid(row=2, column=0, pady=10, padx=10)
        analysis_label3.grid(row=3, column=0, pady=10, padx=10)