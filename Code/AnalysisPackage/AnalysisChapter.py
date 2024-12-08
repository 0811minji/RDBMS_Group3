from tkinter import *
from tkinter.ttk import Combobox
from ConnectDatabase import connect_db


bg_color = "#FEFAE0"
bg_color_2 = "#F2EED7"
title_color = "#CCD5AE"
text_color = "#6C584C"
button_color = "#E0E5B6"
entry_color = "#FAEDCE"

class chapterAnalysis:
    def __init__(self, root, school):
        self.root = root
        self.root.title("Select Chapter")
        self._set_fullscreen()
        self.root.configure(bg=bg_color)

        # Variables to store selected options
        self.selected_school = StringVar(value=school)
        self.selected_grade = StringVar()
        self.selected_semester = StringVar()
        self.selected_chapter_lv1 = StringVar()
        self.selected_chapter_lv2 = StringVar()
        self.selected_chapter_lv3 = StringVar()

        # Database connection
        self.db_connection = connect_db()  # 기존 함수 대신 Login의 함수 사용
        if not self.db_connection:
            raise Exception("Database connection failed!")

        # Main container frame
        self.container = Frame(self.root, bg=bg_color_2)
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
        
    def create_grade_page(self):
        # Grade Page Layout
        for widget in self.container.winfo_children():
            widget.destroy()

        # Configure rows and columns for the container
        self.container.grid_rowconfigure(0, weight=0)  # 레이블이 위치할 행은 고정 크기
        self.container.grid_rowconfigure(1, weight=1)  # 버튼들이 위치할 행은 나머지 공간 차지
        self.container.grid_columnconfigure(0, weight=1)

        Label(self.container, text="Select Grade/Semester", font=('Helevetica', 20), bg=bg_color_2, fg=text_color).grid(
        row=0, column=0, padx=10, pady=10, sticky="n")

        grade_frame = Frame(self.container, bg=bg_color_2)
        grade_frame.grid(row=1, column=0, padx=10, pady=10)

        grades = range(1, 7) if self.selected_school.get() == "elementary" else range(1, 4)
        for grade in grades:
            for semester in [1, 2]:
                btn_text = f"Grade{grade}, Semester{semester}"
                Button(
                    grade_frame,
                    text=btn_text,
                    bg=bg_color_2, fg=text_color,
                    font=('Helevetica', 16),
                    command=lambda g=grade, s=semester: self.grade_selected(g, s)
                ).grid(row=grade-1, column=semester-1, padx=10, pady=10)

    def grade_selected(self, grade, semester):
        self.copy_selected_school = self.selected_school.get()
        self.copy_selected_grade = f"Grade{grade}, Semester{semester}"

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
        self.selected_chapter_lv1.set("")
        self.selected_chapter_lv2.set("")
        self.selected_chapter_lv3.set("")
        # Chapter Page Layout
        for widget in self.container.winfo_children():
            widget.destroy()

        # Configure rows and columns for the container
        total_rows = 5  # 제목 + 대단원 + 중단원 + 소단원 + 버튼
        total_columns = 2  # 레이블과 콤보박스
        for row in range(total_rows):
            self.container.grid_rowconfigure(row, weight=1)  # 모든 행에 가중치 부여
        for col in range(total_columns):
            self.container.grid_columnconfigure(col, weight=1)  # 모든 열에 가중치 부여

        # 제목
        Label(self.container,
              text = f"Chapter for {self.copy_selected_school} {self.copy_selected_grade}", 
              font=('Helevetica', 20, 'bold'), 
              bg=bg_color_2, fg=text_color
              ).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        Label(
            self.container,
            text="Choose Cahpter",
            font=('Helevetica', 18),
            bg=bg_color_2, fg=text_color
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 대단원
        Label(
            self.container,
            text="Chapter Level 1",
            font=('Helevetica', 16),
            bg=bg_color_2, fg=text_color
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        chapter_lv1_combo = Combobox(self.container, textvariable=self.selected_chapter_lv1, state="readonly")
        chapter_lv1_combo['values'] = self.get_chapter_lv1_options()
        chapter_lv1_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        chapter_lv1_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chapter_lv2_options())

        # 중단원
        Label(
            self.container,
            text="Chapter Level 2",
            font=('Helevetica', 16),
            bg=bg_color_2, fg=text_color
        ).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.chapter_lv2_combo = Combobox(self.container, textvariable=self.selected_chapter_lv2, state="readonly")
        self.chapter_lv2_combo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.chapter_lv2_combo.bind("<<ComboboxSelected>>", lambda e: self.update_chapter_lv3_options())

        # 소단원
        Label(
            self.container,
            text="Chapter Level 3",
            font=('Helevetica', 16),
            bg=bg_color_2, fg=text_color
        ).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.chapter_lv3_combo = Combobox(self.container, textvariable=self.selected_chapter_lv3, state="readonly")
        self.chapter_lv3_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # 버튼 (확인 & 뒤로가기)
        Button(
            self.container,
            text="Confirm",
            bg=bg_color_2, fg=text_color,
            font=('Helevetica', 14),
            activebackground=bg_color,
            command=self.show_results
        ).grid(row=5, column=1, padx=10, pady=10, sticky="e")

        Button(
            self.container,
            text="Go back to grade selection",
            bg=bg_color_2, fg=text_color,
            font=('Helevetica', 14),
            activebackground=bg_color,
            command=self.create_grade_page
        ).grid(row=5, column=0, padx=10, pady=10, sticky="w")


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
        results_window = Toplevel(self.root)
        results_window.title("Chapter Result")
        results_window.configure(bg=bg_color)
        print(f"root type: {type(self.root)}")
        ResultsPage(results_window, self.db_connection, selected_lv1, selected_lv2, selected_lv3)

class ResultsPage:
    def __init__(self, root, db_connection, chapter_lv1, chapter_lv2, chapter_lv3, create_page=True):
        self.root = root
        self.db_connection = db_connection
        self.chapter_lv1 = chapter_lv1
        self.chapter_lv2 = chapter_lv2
        self.chapter_lv3 = chapter_lv3
        if create_page:  # 매개변수에 따라 create_results_page 호출
            self.create_results_page()

    def create_results_page(self):
        # # Clear any existing widgets in the window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_rowconfigure(0, weight=1)  # 제목과 학습목표 영역
        self.root.grid_rowconfigure(1, weight=3)  # 버튼 영역
        self.root.grid_columnconfigure(0, weight=1)

        # Title Section
        Label(
            self.root,
            text="Chapter Results Overview",
            font=('Helevetica', 24, 'bold'),
            fg="darkgreen",
            bg=bg_color
        ).grid(row=0, column=0, pady=(20, 5), sticky="n")

        # Fetch achievement for the selected chapter_lv3
        query = """
            SELECT DISTINCT `achievement.name`
            FROM knowledge
            WHERE chapter_lv3 = %s
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (self.chapter_lv3,))

        achievement = cursor.fetchone()
        cursor.fetchall()

        # Display selected chapters and achievement
        Label(
            self.root,
            text=f"Chapter: {self.chapter_lv1} -> {self.chapter_lv2} -> {self.chapter_lv3}\nLearning Objective: {achievement}",
            font=('Helvetica', 16),
            bg=bg_color, fg=text_color,
            wraplength=600,
            justify="center"
        ).grid(row=0, column=0)
        
        # Fetch and display names (sub-units within chapter_lv3)
        query = """
            SELECT name
            FROM knowledge
            WHERE chapter_lv3 = %s
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query, (self.chapter_lv3,))
        names = cursor.fetchall()

        # Create a frame to hold the buttons
        button_frame = Frame(self.root, bg=bg_color_2)
        button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Ensure the parent grid row/column is configured to allow expansion
        self.root.grid_rowconfigure(1, weight=3)  # Row 1
        # self.root.grid_columnconfigure(0, weight=1)  # Column 0
        
        if not names:
            Label(button_frame, text="No Concepts Available", font=('Helevetica', 16), bg=bg_color_2, fg=text_color).grid(row=0, column=0)
        else:
            Label(button_frame, text="Choose Concept: ", font=('Helevetica', 16), bg=bg_color_2, fg=text_color).grid(row=0, column=0)
            for idx,name in enumerate(names):
                Button(
                    button_frame,
                    text=name[0],
                    bg=bg_color_2, fg=text_color,
                    font=('Helevetica', 16),
                    command=lambda n=name: self.show_details_page(self.root, n)).grid(row=(idx // 3)+1, column=idx % 3, padx=10, pady=10)
        
        Button(self.root, text="Go Back", bg=bg_color_2, fg=text_color, font=('Helevetica', 16), activebackground=button_color, command=self.root.destroy).grid(
                    row=1, column=1, sticky="se", padx=10, pady=10)


    def create_concept_buttons(self, parent, concept_ids, label):
        # "선행학습 개념"은 column=0, "이후에 학습할 개념"은 column=1에 배치
        col = 0 if label == "Prerequisite Concepts" else 1

        # Frame 생성 및 배치
        frame = Frame(parent, bg=bg_color_2)
        frame.grid(row=1, column=col, sticky="nsew", padx=10, pady=10)

        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        Label(frame, text=label, font=('Helevetica', 20, 'bold'), bg=bg_color_2).grid(row=0, column=0, padx=10, pady=10)

        for idx, concept_id in enumerate(concept_ids):
            concept_name = self.get_concept_name(concept_id)
            print(f"get concept name {idx} is successful", concept_name)
            if concept_name:
                Button(
                    frame,
                    text=concept_name,
                    bg=bg_color_2, fg=text_color,
                    font=('Helevetica', 16),
                    activebackground=button_color,
                    command=lambda cid=concept_id: self.show_details_page_by_id(parent, cid)
                ).grid(row=1 + idx, column=0, padx=10, pady=5, sticky="ew") # 버튼은 같은 열(column=0)에 순차적으로 배치


    def get_concept_name(self, concept_id):
        # Fetch the name of a concept based on its ID
        query = "SELECT name FROM knowledge WHERE id = %s"
        cursor = self.db_connection.cursor()

        cursor.execute(query, (concept_id,))
        result = cursor.fetchone()

        print("get concpet name result: ", result)
        return result[0] 
    
    
    def show_details_page(self, parent, name):

        try:
            # Ensure name is not a tuple
            if isinstance(name, tuple):
                name = name[0]

            parent.grid_rowconfigure(0, weight=1)  # 단원 이름
            parent.grid_rowconfigure(1, weight=1)  # 설명
            parent.grid_rowconfigure(2, weight=3)  # 선행/후행 학습 개념
            parent.grid_rowconfigure(3, weight=0)  # 버튼
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_columnconfigure(1, weight=1)


            # Title Section
            Label(
                parent,
                text="Detailed Chapter Information",
                font=('Helevetica', 24, 'bold'),
                bg=bg_color_2, fg=text_color,
            ).grid(row=0, column=0, columnspan=2, pady=(20, 5), sticky="n")

            Label(
                parent,
                text=f"Details for selected chapter: {name}. View learning goals and related concepts.",
                font=('Helevetica', 18),
                bg=bg_color_2, fg=text_color,
            ).grid(row=0, column=0, columnspan=2, pady=(50, 10), sticky="s")

            # Fetch description
            query_description = """
                SELECT description
                FROM knowledge
                WHERE name = %s
            """

            cursor = self.db_connection.cursor()
            cursor.execute(query_description, (name,))
            description_result = cursor.fetchone()

            description = description_result[0].replace("\\n", "\n") if description_result else "No Description Available"

            
            # Clear and configure the layout
            for widget in parent.winfo_children():
                widget.destroy()

            
            Label(
                parent,
                text=f"Chapter Name: {name}",
                font=('Helevetica', 20, 'bold'),
                bg=bg_color_2, fg=text_color,
                justify="center", 
                relief="solid"
            ).grid(row=0, column=0, columnspan=2, pady=10, sticky="n")  # 상단 중앙에 표시
            
            # Display description
            description_frame = Frame(parent, bg=bg_color_2, relief="solid", bd=2)
            description_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

            Label(
                description_frame,
                text="DESCRIPTION",
                font=('Helevetica', 18, 'bold'),
                bg=bg_color_2, fg=text_color,
                justify="center", 
                relief="solid"
            ).grid(row=1, column=0, columnspan=2, pady=10, sticky="n")  # 상단 중앙에 표시

            Label(
                description_frame,
                text=description,
                font=('Helevetica', 16),
                bg=bg_color_2, fg=text_color,
                wraplength=600,
                justify="center"
            ).grid(row=2, column=0, padx=10, pady=10, sticky="n")

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
                prereq_ids = eval(prereq_ids) if len(prereq_ids)>=1 else []
                subsequent_ids = eval(subsequent_ids) if subsequent_ids is not None else []
                self.create_concept_buttons(parent, prereq_ids, "Prerequisite Concepts")
                self.create_concept_buttons(parent, subsequent_ids, "Subsequent Concepts")
            else:
                Label(parent, text="No prerequisite or subsequent concepts.", font=('Helvetica', 12)).grid(row=1, column=1)

            # Fetch avgGuessLevel
            query_avgguesslevel = """
                WITH AvgDiffLevel AS (
                    SELECT 
                        knowledgeTag, 
                        AVG(difficultyLevel) AS avgLevel,
                        NTILE(3) OVER (ORDER BY AVG(guessLevel)) AS DiffLevelGroup
                    FROM testIRT
                    GROUP BY knowledgeTag
                )
                SELECT 
                    CASE 
                        WHEN a.DiffLevelGroup = 1 THEN 'Difficult'
                        WHEN a.DiffLevelGroup = 2 THEN 'Moderate'
                        ELSE 'Easy'
                    END AS GuessLevel
                FROM knowledge k
                LEFT JOIN AvgDiffLevel a ON k.id = a.knowledgeTag
                WHERE k.name = %s
            """
            cursor.execute(query_avgguesslevel, (name,))
            guess_level_result = cursor.fetchone()
            print(f"Guess level result: {guess_level_result}")  # 디버깅 결과 확인

            # Guess Level Label
            Label(
                description_frame,
                text=f"Difficulty level: {guess_level_result}",
                font=('Helevetica', 16, 'bold'),
                bg=bg_color_2, fg=text_color,
                wraplength=600,
                justify="center"
            ).grid(row=3, column=0, padx=10, pady=10, sticky="n")

        except Exception as e: print(f"Error executing query: {e}")

                # Add a close button
        Button(parent, text="Go back", bg=bg_color_2, fg=text_color, font=('Helevetica', 14), command=self.root.destroy).grid(
            row=2, column=0, sticky="se", padx=10, pady=10,
        )


    def show_details_page_by_id(self, parent, concept_id):
        # Fetch the name associated with the ID and open the details page
        name = self.get_concept_name(concept_id)
        if name:
            self.show_details_page(parent, name)