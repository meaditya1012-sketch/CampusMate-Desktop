
import sqlite3

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QInputDialog,
    QHeaderView,
    QFrame,
    QSizePolicy,
)

from database.database import get_connection


class StudyScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("studyScreen")
        self.remaining_seconds = 25 * 60

        self.build_ui()
        self.load_subjects()
        self.load_notes()
        self.update_timer_label()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(14)

        # Page heading
        heading = QLabel("Study Center")
        heading.setObjectName("pageTitle")
        layout.addWidget(heading)

        subtitle = QLabel(
            "Organize your subjects, save revision notes, "
            "and focus on your next goal."
        )
        subtitle.setObjectName("pageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Subjects card
        subject_card = QFrame()
        subject_card.setObjectName("contentCard")

        subject_layout = QVBoxLayout(subject_card)
        subject_layout.setContentsMargins(18, 16, 18, 16)
        subject_layout.setSpacing(12)

        subject_heading = QLabel("My Subjects")
        subject_heading.setObjectName("sectionHeading")
        subject_layout.addWidget(subject_heading)

        subject_row = QHBoxLayout()
        subject_row.setSpacing(10)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText(
            "Subject name (e.g. Applied Mathematics)"
        )

        self.goal_input = QLineEdit()
        self.goal_input.setPlaceholderText("Weekly goal (hours)")
        self.goal_input.setText("10")
        self.goal_input.setMaximumWidth(150)

        add_subject_button = QPushButton("+ Add Subject")
        add_subject_button.setObjectName("primaryButton")
        add_subject_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        add_subject_button.clicked.connect(self.add_subject)

        subject_row.addWidget(self.subject_input, 3)
        subject_row.addWidget(self.goal_input, 1)
        subject_row.addWidget(add_subject_button)

        subject_layout.addLayout(subject_row)

        self.subject_table = QTableWidget()
        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(
            ["Subject", "Weekly Goal (hrs)", "Completed (hrs)"]
        )
        self.configure_table(self.subject_table)
        self.subject_table.setMinimumHeight(120)
        self.subject_table.setMaximumHeight(185)

        subject_layout.addWidget(self.subject_table)
        layout.addWidget(subject_card)

        # Study notes card
        notes_card = QFrame()
        notes_card.setObjectName("contentCard")

        notes_layout = QVBoxLayout(notes_card)
        notes_layout.setContentsMargins(18, 16, 18, 16)
        notes_layout.setSpacing(10)

        notes_heading = QLabel("Study Notes")
        notes_heading.setObjectName("sectionHeading")
        notes_layout.addWidget(notes_heading)

        self.note_title_input = QLineEdit()
        self.note_title_input.setPlaceholderText("Note title")

        self.note_subject_input = QComboBox()
        self.note_subject_input.addItem("General")

        self.note_content_input = QTextEdit()
        self.note_content_input.setPlaceholderText(
            "Write your revision notes here..."
        )
        self.note_content_input.setMinimumHeight(65)
        self.note_content_input.setMaximumHeight(95)

        save_note_button = QPushButton("Save Note")
        save_note_button.setObjectName("primaryButton")
        save_note_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        save_note_button.clicked.connect(self.save_note)

        notes_layout.addWidget(self.note_title_input)
        notes_layout.addWidget(self.note_subject_input)
        notes_layout.addWidget(self.note_content_input)
        notes_layout.addWidget(save_note_button)

        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(3)
        self.notes_table.setHorizontalHeaderLabels(
            ["Title", "Subject", "Created"]
        )
        self.configure_table(self.notes_table)
        self.notes_table.setMinimumHeight(115)
        self.notes_table.setMaximumHeight(175)
        self.notes_table.cellDoubleClicked.connect(self.open_note)

        notes_layout.addWidget(self.notes_table)

        tip = QLabel(
            "Tip: Double-click any note to read its full content."
        )
        tip.setObjectName("pageSubtitle")
        notes_layout.addWidget(tip)

        layout.addWidget(notes_card)

        # Pomodoro timer card
        timer_card = QFrame()
        timer_card.setObjectName("contentCard")

        timer_layout = QVBoxLayout(timer_card)
        timer_layout.setContentsMargins(18, 14, 18, 14)
        timer_layout.setSpacing(8)

        timer_heading = QLabel("Pomodoro Focus Timer")
        timer_heading.setObjectName("sectionHeading")
        timer_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(timer_heading)

        self.timer_label = QLabel("25:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)

        timer_buttons = QHBoxLayout()
        timer_buttons.setSpacing(10)

        self.start_button = QPushButton("▶  Start")
        self.pause_button = QPushButton("Ⅱ  Pause")
        self.reset_button = QPushButton("↻  Reset")

        self.start_button.setObjectName("primaryButton")

        for button in [
            self.start_button,
            self.pause_button,
            self.reset_button,
        ]:
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            timer_buttons.addWidget(button)

        timer_layout.addLayout(timer_buttons)
        layout.addWidget(timer_card)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        layout.addStretch()

    def configure_table(self, table):
        table.setAlternatingRowColors(True)
        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(34)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

    # Subjects
    def add_subject(self):
        name = self.subject_input.text().strip()
        goal_text = self.goal_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Missing Subject",
                "Please enter a subject name.",
            )
            return

        try:
            goal_hours = float(goal_text)

            if goal_hours <= 0:
                raise ValueError

        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Goal",
                "Enter a weekly goal greater than zero.",
            )
            return

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO subjects
                    (name, goal_hours, completed_hours)
                VALUES (?, ?, 0)
                """,
                (name, goal_hours),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Subject Exists",
                "This subject already exists.",
            )
            return

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save the subject:\n{error}",
            )
            return

        finally:
            connection.close()

        self.subject_input.clear()
        self.goal_input.setText("10")
        self.load_subjects()

    def load_subjects(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT name, goal_hours, completed_hours
                FROM subjects
                ORDER BY name COLLATE NOCASE
                """
            )
            subjects = cursor.fetchall()

        except sqlite3.Error as error:
            QMessageBox.warning(
                self,
                "Database Error",
                f"Could not load subjects:\n{error}",
            )
            return

        finally:
            connection.close()

        self.subject_table.setRowCount(0)

        for subject, goal, completed in subjects:
            row = self.subject_table.rowCount()
            self.subject_table.insertRow(row)

            values = [
                subject,
                f"{goal:g}" if isinstance(goal, (int, float)) else str(goal),
                f"{completed:g}" if isinstance(completed, (int, float)) else str(completed),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column > 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )
                self.subject_table.setItem(row, column, item)

        current_subject = self.note_subject_input.currentText()

        self.note_subject_input.blockSignals(True)
        self.note_subject_input.clear()
        self.note_subject_input.addItem("General")

        for subject, _, _ in subjects:
            self.note_subject_input.addItem(subject)

        index = self.note_subject_input.findText(current_subject)
        if index >= 0:
            self.note_subject_input.setCurrentIndex(index)

        self.note_subject_input.blockSignals(False)

    # Study notes
    def save_note(self):
        title = self.note_title_input.text().strip()
        subject = self.note_subject_input.currentText()
        content = self.note_content_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Missing Title",
                "Please enter a title for your note.",
            )
            return

        if not content:
            QMessageBox.warning(
                self,
                "Empty Note",
                "Please write some note content first.",
            )
            return

        if subject == "General":
            subject = None

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO study_notes (title, subject, content)
                VALUES (?, ?, ?)
                """,
                (title, subject, content),
            )
            connection.commit()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save the note:\n{error}",
            )
            return

        finally:
            connection.close()

        self.note_title_input.clear()
        self.note_content_input.clear()
        self.load_notes()

    def load_notes(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT title, subject, created_at
                FROM study_notes
                ORDER BY id DESC
                """
            )
            notes = cursor.fetchall()

        except sqlite3.Error as error:
            QMessageBox.warning(
                self,
                "Database Error",
                f"Could not load notes:\n{error}",
            )
            return

        finally:
            connection.close()

        self.notes_table.setRowCount(0)

        for title, subject, created_at in notes:
            row = self.notes_table.rowCount()
            self.notes_table.insertRow(row)

            values = [
                title,
                subject or "General",
                str(created_at or ""),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                self.notes_table.setItem(row, column, item)

    def open_note(self, row, column):
        title_item = self.notes_table.item(row, 0)

        if title_item is None:
            return

        title = title_item.text()

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT content
                FROM study_notes
                WHERE title = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (title,),
            )
            result = cursor.fetchone()

        except sqlite3.Error as error:
            QMessageBox.warning(
                self,
                "Database Error",
                f"Could not open the note:\n{error}",
            )
            return

        finally:
            connection.close()

        if result:
            content = result[0] or ""
            QMessageBox.information(
                self,
                title,
                content,
            )
        else:
            QMessageBox.warning(
                self,
                "Note Not Found",
                "The selected note could not be found.",
            )

    # Pomodoro timer
    def update_timer_label(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        if self.remaining_seconds <= 0:
            self.remaining_seconds = 25 * 60
            self.update_timer_label()

        self.timer.start()
        self.start_button.setEnabled(False)

    def pause_timer(self):
        self.timer.stop()
        self.start_button.setEnabled(True)

    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = 25 * 60
        self.update_timer_label()
        self.start_button.setEnabled(True)

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_label()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.start_button.setEnabled(True)
            QMessageBox.information(
                self,
                "Focus Session Complete",
                "Great work! Your 25-minute focus session is complete.",
            )
