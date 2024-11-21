import tkinter as tk
from tkinter import ttk
import mysql.connector


class chapterAnalysis:
    def __init__(self, root, school):
        self.root = root
        self.root.title("단원 선택")
        self._set_fullscreen()

        # Variables to store selected options
        self.selected_school = tk.StringVar(value=school)
        self.selected_grade = tk.StringVar()
        self.selected_semester = tk.StringVar()
        self.selected_chapter_lv1 = tk.StringVar()
        self.selected_chapter_lv2 = tk.StringVar()
        self.selected_chapter_lv3 = tk.StringVar()

        # Database connection
        self.db_connection = self.connect_to_db()

        # Main container frame
        self.container = ttk.Frame(self.root)
        self.container.pack(fill='both', expand=True)

        # Create and display main page
        self.create_grade_page()

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

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="5749",
                database="math"
            )
            print("Database connected successfully!")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    # def create_main_page(self):
    #     # Main Page Layout
    #     for widget in self.container.winfo_children():
    #         widget.destroy()

    #     # ttk.Label(self.container, text="학교를 선택하세요", font=('Helvetica', 18)).pack(pady=30)
    #     # Display the selected school
    #     ttk.Label(
    #         self.container,
    #         text=f"선택한 학교: {self.selected_school.get()}",
    #         font=('Helvetica', 18)
    #     ).pack(pady=30)

    #     # schools = ["elementary", "middle", "high"]
    #     # for school in schools:
    #     #     ttk.Button(
    #     #         self.container,
    #     #         text=school,
    #     #         command=lambda s=school: self.school_selected(s)
    #     #     ).pack(pady=10, padx=100, fill='x')

    # def school_selected(self, school):
    #     self.selected_school.set(school)
    #     self.create_grade_page()

    def create_grade_page(self):
        # Grade Page Layout
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="학년/학기를 선택하세요", font=('Helvetica', 18)).pack(pady=20)

        grade_frame = ttk.Frame(self.container)
        grade_frame.pack(pady=20)

        grades = range(1, 7) if self.selected_school.get() == "elementary" else range(1, 4)
        for grade in grades:
            for semester in [1, 2]:
                btn_text = f"{grade}학년 {semester}학기"
                ttk.Button(
                    grade_frame,
                    text=btn_text,
                    command=lambda g=grade, s=semester: self.grade_selected(g, s)
                ).grid(row=grade-1, column=semester-1, padx=10, pady=10)

        ttk.Button(
            self.container,
            text="뒤로가기",
            command=self.create_main_page
        ).pack(pady=20)

    def grade_selected(self, grade, semester):
        def convert_grade(self, grade):
            if self.selected_school.get() == "elementary":
                return grade
            elif self.selected_school.get() == "middle":
                return grade + 6
            elif self.selected_school.get() == "high":
                return grade + 9

        grade = convert_grade(self, grade)
        self.selected_grade.set(str(grade))
        self.selected_semester.set(str(semester))
        self.create_chapter_page()

    def create_chapter_page(self):
        # Chapter Page Layout
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="단원을 선택하세요", font=('Helvetica', 18)).pack(pady=20)

        ttk.Label(self.container, text="대단원", font=('Helvetica', 14)).pack(pady=5)
        chapter_lv1_combo = ttk.Combobox(self.container, textvariable=self.selected_chapter_lv1, state="readonly")
        chapter_lv1_combo['values'] = self.get_chapter_lv1_options()
        chapter_lv1_combo.pack(pady=10)
        chapter_lv1_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chapter_lv2_options())

        ttk.Label(self.container, text="중단원", font=('Helvetica', 14)).pack(pady=5)
        self.chapter_lv2_combo = ttk.Combobox(self.container, textvariable=self.selected_chapter_lv2, state="readonly")
        self.chapter_lv2_combo.pack(pady=10)
        self.chapter_lv2_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chapter_lv3_options())

        ttk.Label(self.container, text="소단원", font=('Helvetica', 14)).pack(pady=5)
        self.chapter_lv3_combo = ttk.Combobox(self.container, textvariable=self.selected_chapter_lv3, state="readonly")
        self.chapter_lv3_combo.pack(pady=10)

        ttk.Button(
            self.container,
            text="확인",
            command=self.show_results
        ).pack(pady=20)

        ttk.Button(
            self.container,
            text="뒤로가기",
            command=self.create_grade_page
        ).pack(pady=10)

    def get_chapter_lv1_options(self):
        query = "SELECT DISTINCT chapter_lv1 FROM knowledge WHERE course_grade = %s AND course_semester = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (self.selected_grade.get(), self.selected_semester.get()))
        return [row[0] for row in cursor.fetchall()]

    def update_chapter_lv2_options(self):
        chapter_lv1 = self.selected_chapter_lv1.get()
        query = "SELECT DISTINCT chapter_lv2 FROM knowledge WHERE chapter_lv1 = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (chapter_lv1,))
        self.chapter_lv2_combo['values'] = [row[0] for row in cursor.fetchall()]

    def update_chapter_lv3_options(self):
        chapter_lv2 = self.selected_chapter_lv2.get()
        query = "SELECT DISTINCT chapter_lv3 FROM knowledge WHERE chapter_lv2 = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (chapter_lv2,))
        self.chapter_lv3_combo['values'] = [row[0] for row in cursor.fetchall()]

    def show_results(self):
        selected_lv1 = self.selected_chapter_lv1.get()
        selected_lv2 = self.selected_chapter_lv2.get()
        selected_lv3 = self.selected_chapter_lv3.get()
        results_window = tk.Toplevel(self.root)
        results_window.title("단원 결과")
        ResultsPage(results_window, self.db_connection, selected_lv1, selected_lv2, selected_lv3)

class ResultsPage:
    def __init__(self, root, db_connection, chapter_lv1, chapter_lv2, chapter_lv3):
        self.root = root
        self.db_connection = db_connection
        self.chapter_lv1 = chapter_lv1
        self.chapter_lv2 = chapter_lv2
        self.chapter_lv3 = chapter_lv3
        self.create_results_page()

    def create_results_page(self):
        # Clear any existing widgets in the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Fetch achievement for the selected chapter_lv3
        query = """
            SELECT DISTINCT `achievement.name`
            FROM knowledge
            WHERE chapter_lv3 = %s
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (self.chapter_lv3,))
        # achievement_result = cursor.fetchone()
        # achievement = achievement_result[0] if achievement_result else "No Achievement Information"
        achievement = cursor.fetchone() 
        
        # Display selected chapters and achievement
        ttk.Label(
            self.root,
            text=f"단원: {self.chapter_lv1} -> {self.chapter_lv2} -> {self.chapter_lv3}\n학습목표: {achievement}",
            font=('Helvetica', 16),
            wraplength=600,
            justify="center"
        ).pack(pady=20)

        # Fetch and display names (sub-units within chapter_lv3)
        query = """
            SELECT name
            FROM knowledge
            WHERE chapter_lv3 = %s
        """
        cursor.execute(query, (self.chapter_lv3,))
        names = cursor.fetchall()

        if not names:
            ttk.Label(self.root, text="세부 단원 정보가 없습니다.", font=('Helvetica', 14)).pack(pady=10)
        else:
            ttk.Label(self.root, text="세부 단원을 선택하세요:", font=('Helvetica', 14)).pack(pady=10)
            for name in names:
                ttk.Button(
                    self.root,
                    text=name,
                    command=lambda n=name: self.show_details_page(n)
                ).pack(pady=5)

        ttk.Button(self.root, text="뒤로가기", command=self.root.destroy).pack(pady=20)

    
    def create_concept_buttons(self, parent, concept_ids, label):
        if concept_ids:
            ttk.Label(parent, text=label, font=('Helvetica', 14, 'bold')).pack(pady=10)

            if concept_ids is None or concept_ids==[] :  # Check if concept_ids is empty or None
                if label == "선행학습 개념":
                    ttk.Label(parent, text="No prerequisite concepts available.", font=('Helvetica', 12)).pack(pady=5)
                elif label == "이후에 학습할 개념":
                    ttk.Label(parent, text="No subsequent concepts available.", font=('Helvetica', 12)).pack(pady=5)
                return

            #concept_ids= [concept_id.strip() for concept_id in concept_ids.split(",")]
            for concept_id in concept_ids:
                concept_name = self.get_concept_name(concept_id)
                if concept_name:
                    ttk.Button(
                        parent,
                        text=concept_name,
                        command=lambda cid=concept_id: self.show_details_page_by_id(cid)
                    ).pack(pady=5)

    def get_concept_name(self, concept_id):
        # Fetch the name of a concept based on its ID
        query = "SELECT name FROM knowledge WHERE id = %s"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (concept_id,))
        result = cursor.fetchone()
        return result[0] 
    
    
    def show_details_page(self, name):
        # Create a new window for the details page
        details_window = tk.Toplevel(self.root)
        details_window.title("단원 상세 분석")

        try:

            # Ensure name is not a tuple
            if isinstance(name, tuple):
                name = name[0]

            # Fetch description
            query_description = """
                SELECT description
                FROM knowledge
                WHERE name = %s
            """
            
            cursor = self.db_connection.cursor()
            print(f"Executing query: {query_description} with parameter: {name}")  # 디버깅 메시지
            cursor.execute(query_description, (name,))
            description_result = cursor.fetchone()
            print(f"Description result: {description_result}")  # 디버깅 결과 확인

            description = description_result[0] if description_result else "상세 정보가 없습니다."

            # Display description
            ttk.Label(
                details_window,
                text=f"Description:\n{description}",
                font=('Helvetica', 14),
                wraplength=600,
                justify="center"
            ).pack(pady=20)

            query_concepts = """
                SELECT `prereqConcept.id`, `subsequentConcept.id`
                FROM knowledge
                WHERE name = %s
            """
            cursor.execute(query_concepts, (name,))
            concepts_result = cursor.fetchone()
            print(f"Concepts result: {concepts_result}")  # 디버깅 결과 확인

            if concepts_result:
                prereq_ids, subsequent_ids = concepts_result
                prereq_ids = eval(prereq_ids) if prereq_ids else []
                subsequent_ids = eval(subsequent_ids) if subsequent_ids else []
                self.create_concept_buttons(details_window, prereq_ids, "선행학습 개념")
                self.create_concept_buttons(details_window, subsequent_ids, "이후에 학습할 개념")
            else:
                ttk.Label(details_window, text="No prerequisite or subsequent concepts.", font=('Helvetica', 12)).pack(pady=5)

            # Fetch avgGuessLevel
            query_avgguesslevel = """
                WITH AvgGuessLevel AS (
                    SELECT 
                        knowledgeTag, 
                        AVG(guessLevel) AS avgGuess,
                        NTILE(3) OVER (ORDER BY AVG(guessLevel)) AS GuessLevelGroup
                    FROM testIRT
                    GROUP BY knowledgeTag
                )
                SELECT 
                    CASE 
                        WHEN ag.GuessLevelGroup = 1 THEN '하'
                        WHEN ag.GuessLevelGroup = 2 THEN '중'
                        ELSE '상'
                    END AS GuessLevel
                FROM knowledge k
                LEFT JOIN AvgGuessLevel ag ON k.id = ag.knowledgeTag
                WHERE k.name = %s
            """
            cursor.execute(query_avgguesslevel, (name,))
            guess_level_result = cursor.fetchone()
            print(f"Guess level result: {guess_level_result}")  # 디버깅 결과 확인

            if guess_level_result:
                guess_level = guess_level_result[0]
                ttk.Label(
                    details_window,
                    text=f"난이도 수준: {guess_level}",
                    font=('Helvetica', 14, 'bold'),
                    wraplength=600,
                    justify="center"
                ).pack(pady=20)

                
        except Exception as e: print(f"Error executing query: {e}")

        ttk.Button(details_window, text="닫기", command=details_window.destroy).pack(pady=20)


    def show_details_page_by_id(self, concept_id):
        # Fetch the name associated with the ID and open the details page
        name = self.get_concept_name(concept_id)
        if name:
            self.show_details_page(name)