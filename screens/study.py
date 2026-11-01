import sqlite3

from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database.database import get_connection
from screens.components import create_empty_state


class AddSubjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a subject")
        self.setMinimumWidth(370)

        layout = QFormLayout(self)
        layout.setContentsMargins(22, 20, 22, 18)
        layout.setSpacing(12)
        self.name = QLineEdit()
        self.name.setPlaceholderText("e.g. Linear Algebra")
        self.goal = QDoubleSpinBox()
        self.goal.setRange(0.5, 168)
        self.goal.setSingleStep(0.5)
        self.goal.setValue(10)
        self.goal.setSuffix(" hrs / week")
        layout.addRow("Subject", self.name)
        layout.addRow("Weekly goal", self.goal)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


class AddNoteDialog(QDialog):
    def __init__(self, subjects, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Write a study note")
        self.setMinimumSize(430, 390)

        layout = QFormLayout(self)
        layout.setContentsMargins(22, 20, 22, 18)
        layout.setSpacing(12)
        self.title = QLineEdit()
        self.title.setPlaceholderText("e.g. Key ideas from chapter 3")
        self.subject = QComboBox()
        self.subject.addItem("General")
        self.subject.addItems(subjects)
        self.content = QTextEdit()
        self.content.setPlaceholderText("Write a useful summary, formula, or question...")
        self.content.setMinimumHeight(150)

        layout.addRow("Note title", self.title)
        layout.addRow("Subject", self.subject)
        layout.addRow("Your notes", self.content)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


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
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page_layout.addWidget(scroll)

        content = QWidget()
        content.setObjectName("studyContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(34, 28, 34, 28)
        layout.setSpacing(16)

        title = QLabel("Study Center")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Build steady progress, one session at a time.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        columns = QHBoxLayout()
        columns.setSpacing(14)
        layout.addLayout(columns)

        left_column = QVBoxLayout()
        left_column.setSpacing(14)
        columns.addLayout(left_column, 1)

        right_column = QVBoxLayout()
        right_column.setSpacing(14)
        columns.addLayout(right_column, 1)

        # Subjects
        subject_card = QFrame()
        subject_card.setObjectName("contentCard")
        subject_layout = QVBoxLayout(subject_card)
        subject_layout.setContentsMargins(17, 15, 17, 15)
        subject_layout.setSpacing(12)

        subject_header = QHBoxLayout()
        subject_title = QLabel("My subjects")
        subject_title.setObjectName("sectionHeading")
        subject_header.addWidget(subject_title, 1)
        add_subject_button = QPushButton("+  Add")
        add_subject_button.setObjectName("primaryButton")
        add_subject_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_subject_button.clicked.connect(self.add_subject)
        subject_header.addWidget(add_subject_button)
        subject_layout.addLayout(subject_header)

        self.subjects_layout = QVBoxLayout()
        self.subjects_layout.setSpacing(8)
        subject_layout.addLayout(self.subjects_layout)
        left_column.addWidget(subject_card)

        # Focus timer
        timer_card = QFrame()
        timer_card.setObjectName("contentCard")
        timer_layout = QVBoxLayout(timer_card)
        timer_layout.setContentsMargins(17, 15, 17, 16)
        timer_layout.setSpacing(9)

        timer_heading = QLabel("Pomodoro focus")
        timer_heading.setObjectName("sectionHeading")
        timer_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(timer_heading)

        self.timer_label = QLabel("25:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)

        timer_caption = QLabel("A focused 25-minute session, then a short break.")
        timer_caption.setObjectName("muted")
        timer_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(timer_caption)

        timer_buttons = QHBoxLayout()
        timer_buttons.setSpacing(8)
        self.start_button = QPushButton("Start focus")
        self.start_button.setObjectName("primaryButton")
        self.reset_button = QPushButton("Reset")
        for button in (self.start_button, self.reset_button):
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            timer_buttons.addWidget(button)
        timer_layout.addLayout(timer_buttons)
        left_column.addWidget(timer_card)
        left_column.addStretch()

        # Revision notes
        notes_card = QFrame()
        notes_card.setObjectName("contentCard")
        notes_layout = QVBoxLayout(notes_card)
        notes_layout.setContentsMargins(17, 15, 17, 15)
        notes_layout.setSpacing(12)

        notes_header = QHBoxLayout()
        notes_title = QLabel("Study notes")
        notes_title.setObjectName("sectionHeading")
        notes_header.addWidget(notes_title, 1)
        add_note_button = QPushButton("+  New note")
        add_note_button.setObjectName("primaryButton")
        add_note_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_note_button.clicked.connect(self.add_note)
        notes_header.addWidget(add_note_button)
        notes_layout.addLayout(notes_header)

        self.notes_layout = QVBoxLayout()
        self.notes_layout.setSpacing(8)
        notes_layout.addLayout(self.notes_layout)
        right_column.addWidget(notes_card)
        right_column.addStretch()

        layout.addStretch()
        scroll.setWidget(content)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.start_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def make_subject_card(self, record):
        subject_id, name, goal, completed = record
        goal = float(goal or 0)
        completed = float(completed or 0)
        progress_value = min(100, max(0, round(completed / goal * 100))) if goal else 0

        card = QFrame()
        card.setObjectName("subjectItem")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(13, 11, 13, 11)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel(name)
        title.setObjectName("listMain")
        title.setWordWrap(True)
        goal_label = QLabel(f"{goal:g} hrs / week")
        goal_label.setObjectName("subjectGoal")
        header.addWidget(title, 1)
        header.addWidget(goal_label)
        layout.addLayout(header)

        progress = QProgressBar()
        progress.setObjectName("studyProgress")
        progress.setRange(0, 100)
        progress.setValue(max(0, min(100, progress_value)))
        progress.setTextVisible(False)
        progress.setFixedHeight(7)
        layout.addWidget(progress)

        footer = QHBoxLayout()
        detail = QLabel(f"{completed:.1f} hours studied")
        detail.setObjectName("listMeta")
        percent = QLabel(f"{max(0, progress_value)}%")
        percent.setObjectName("studyPercent")
        footer.addWidget(detail, 1)
        footer.addWidget(percent)
        layout.addLayout(footer)

        add_time = QPushButton("+ 30 min")
        add_time.setObjectName("smallButton")
        add_time.setCursor(Qt.CursorShape.PointingHandCursor)
        add_time.clicked.connect(lambda: self.add_study_time(subject_id))
        layout.addWidget(add_time, 0, Qt.AlignmentFlag.AlignLeft)
        return card

    def make_note_card(self, record):
        note_id, title, subject, content, created_at = record
        card = QFrame()
        card.setObjectName("noteItem")

        row = QHBoxLayout(card)
        row.setContentsMargins(11, 10, 9, 10)
        row.setSpacing(9)

        icon = QLabel("▤")
        icon.setObjectName("noteIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(30, 34)
        row.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)

        copy = QVBoxLayout()
        copy.setSpacing(3)
        title_button = QPushButton(title)
        title_button.setObjectName("noteLink")
        title_button.setCursor(Qt.CursorShape.PointingHandCursor)
        title_button.setToolTip("Open note")
        title_button.clicked.connect(lambda: self.open_note(note_id))
        created = QDateTime.fromString(str(created_at or ""), "yyyy-MM-dd HH:mm:ss")
        date_text = created.toString("MMM d") if created.isValid() else str(created_at or "")
        meta = QLabel(f"{subject or 'General'}  ·  {date_text}")
        meta.setObjectName("listMeta")
        meta.setWordWrap(True)
        preview_text = content.replace("\n", " ")
        if len(preview_text) > 110:
            preview_text = preview_text[:107].rstrip() + "…"
        preview = QLabel(preview_text)
        preview.setObjectName("notePreview")
        preview.setWordWrap(True)
        copy.addWidget(title_button)
        copy.addWidget(meta)
        copy.addWidget(preview)
        row.addLayout(copy, 1)

        remove = QPushButton("×")
        remove.setObjectName("iconButton")
        remove.setToolTip("Delete note")
        remove.setAccessibleName(f"Delete note {title}")
        remove.clicked.connect(lambda: self.delete_note(note_id, title))
        row.addWidget(remove, 0, Qt.AlignmentFlag.AlignTop)
        return card

    def load_subjects(self):
        connection = get_connection()
        try:
            records = connection.execute(
                "SELECT id, name, goal_hours, completed_hours FROM subjects ORDER BY name COLLATE NOCASE"
            ).fetchall()
        except sqlite3.Error as error:
            QMessageBox.warning(self, "Database error", f"Could not load subjects:\n{error}")
            return
        finally:
            connection.close()

        self.clear_layout(self.subjects_layout)
        if not records:
            self.subjects_layout.addWidget(
                create_empty_state(
                    "Choose what to focus on",
                    "Add a subject and set a weekly study goal.",
                )
            )
        else:
            for record in records:
                self.subjects_layout.addWidget(self.make_subject_card(record))

    def add_subject(self):
        dialog = AddSubjectDialog(self)
        if not dialog.exec():
            return
        name = dialog.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing subject", "Enter a subject name.")
            return

        connection = get_connection()
        try:
            connection.execute(
                "INSERT INTO subjects (name, goal_hours, completed_hours) VALUES (?, ?, 0)",
                (name, dialog.goal.value()),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Subject already exists", "This subject is already in your study list.")
            return
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Database error", f"Could not save the subject:\n{error}")
            return
        finally:
            connection.close()
        self.load_subjects()

    def add_study_time(self, subject_id):
        connection = get_connection()
        try:
            connection.execute(
                "UPDATE subjects SET completed_hours = COALESCE(completed_hours, 0) + 0.5 WHERE id = ?",
                (subject_id,),
            )
            connection.commit()
        finally:
            connection.close()
        self.load_subjects()

    def load_notes(self):
        connection = get_connection()
        try:
            records = connection.execute(
                """
                SELECT id, title, subject, content, created_at
                FROM study_notes ORDER BY id DESC
                """
            ).fetchall()
        except sqlite3.Error as error:
            QMessageBox.warning(self, "Database error", f"Could not load notes:\n{error}")
            return
        finally:
            connection.close()

        self.clear_layout(self.notes_layout)
        if not records:
            self.notes_layout.addWidget(
                create_empty_state(
                    "Keep your best ideas close",
                    "Save a revision note so you can find it later.",
                )
            )
        else:
            for record in records:
                self.notes_layout.addWidget(self.make_note_card(record))

    def add_note(self):
        connection = get_connection()
        try:
            subjects = [
                row[0]
                for row in connection.execute(
                    "SELECT name FROM subjects ORDER BY name COLLATE NOCASE"
                ).fetchall()
            ]
        finally:
            connection.close()

        dialog = AddNoteDialog(subjects, self)
        if not dialog.exec():
            return
        title = dialog.title.text().strip()
        note_content = dialog.content.toPlainText().strip()
        if not title or not note_content:
            QMessageBox.warning(self, "Note incomplete", "Add a title and some note content.")
            return
        subject = dialog.subject.currentText()
        subject = None if subject == "General" else subject

        connection = get_connection()
        try:
            connection.execute(
                "INSERT INTO study_notes (title, subject, content) VALUES (?, ?, ?)",
                (title, subject, note_content),
            )
            connection.commit()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Database error", f"Could not save the note:\n{error}")
            return
        finally:
            connection.close()
        self.load_notes()

    def open_note(self, note_id):
        connection = get_connection()
        try:
            record = connection.execute(
                "SELECT title, content FROM study_notes WHERE id = ?",
                (note_id,),
            ).fetchone()
        finally:
            connection.close()
        if record:
            QMessageBox.information(self, record[0], record[1] or "")

    def delete_note(self, note_id, title):
        answer = QMessageBox.question(
            self,
            "Delete note",
            f"Delete the note “{title}”?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        connection = get_connection()
        try:
            connection.execute("DELETE FROM study_notes WHERE id = ?", (note_id,))
            connection.commit()
        finally:
            connection.close()
        self.load_notes()

    def update_timer_label(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Resume focus")
            return
        if self.remaining_seconds <= 0:
            self.remaining_seconds = 25 * 60
            self.update_timer_label()
        self.timer.start()
        self.start_button.setText("Pause")

    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = 25 * 60
        self.update_timer_label()
        self.start_button.setText("Start focus")

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_label()
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.start_button.setText("Start focus")
            QMessageBox.information(
                self,
                "Focus session complete",
                "Nice work. Your 25-minute focus session is complete.",
            )
