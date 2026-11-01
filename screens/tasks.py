from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from database.database import get_connection
from screens.components import create_empty_state


class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a task")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)
        layout.setContentsMargins(22, 20, 22, 18)
        layout.setSpacing(12)

        self.title = QLineEdit()
        self.subject = QLineEdit()
        self.due_date = QDateEdit(QDate.currentDate())
        self.due_date.setCalendarPopup(True)
        self.due_date.setDisplayFormat("d MMM yyyy")
        self.no_due_date = QCheckBox("No due date")
        self.no_due_date.setChecked(True)
        self.due_date.setEnabled(False)
        self.no_due_date.toggled.connect(lambda checked: self.due_date.setEnabled(not checked))

        self.priority = QComboBox()
        self.priority.addItems(["Low", "Medium", "High"])
        self.title.setPlaceholderText("e.g. Finish the lab report")
        self.subject.setPlaceholderText("e.g. Physics (optional)")

        layout.addRow("Task", self.title)
        layout.addRow("Subject", self.subject)
        due_row = QHBoxLayout()
        due_row.addWidget(self.due_date, 1)
        due_row.addWidget(self.no_due_date)
        layout.addRow("Due date", due_row)
        layout.addRow("Priority", self.priority)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


class TasksScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("tasksScreen")
        self.filter = "open"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(15)

        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(4)
        title = QLabel("Tasks")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Make room for the work that matters.")
        subtitle.setObjectName("pageSubtitle")
        heading.addWidget(title)
        heading.addWidget(subtitle)
        header.addLayout(heading, 1)

        add_button = QPushButton("+  Add task")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(self.open_add_task)
        header.addWidget(add_button, 0, Qt.AlignmentFlag.AlignBottom)
        layout.addLayout(header)

        filters = QHBoxLayout()
        filters.setSpacing(7)
        self.filter_buttons = {}
        for key, label in (("open", "Open"), ("all", "All"), ("done", "Completed")):
            button = QPushButton(label)
            button.setObjectName("filterButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _checked=False, value=key: self.set_filter(value))
            filters.addWidget(button)
            self.filter_buttons[key] = button
        filters.addStretch()
        layout.addLayout(filters)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_content = QWidget()
        self.list_layout = QVBoxLayout(self.list_content)
        self.list_layout.setContentsMargins(0, 0, 4, 0)
        self.list_layout.setSpacing(9)
        self.scroll.setWidget(self.list_content)
        layout.addWidget(self.scroll, 1)

        self.load_tasks()

    def set_filter(self, value):
        self.filter = value
        self.load_tasks()

    def clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def make_task_card(self, task):
        task_id, title, subject, due_date, priority, completed = task
        card = QFrame()
        card.setObjectName("taskItem")

        row = QHBoxLayout(card)
        row.setContentsMargins(14, 11, 12, 11)
        row.setSpacing(11)

        toggle = QPushButton("✓" if completed else "")
        toggle.setObjectName("taskToggle")
        toggle.setProperty("complete", bool(completed))
        toggle.setCheckable(False)
        toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle.setAccessibleName(
            f"Mark {title} {'open' if completed else 'complete'}"
        )
        toggle.clicked.connect(lambda: self.toggle_task(task_id, completed))
        row.addWidget(toggle, 0, Qt.AlignmentFlag.AlignVCenter)

        copy = QVBoxLayout()
        copy.setSpacing(3)
        title_label = QLabel(title)
        title_label.setObjectName("listMain")
        title_label.setWordWrap(True)
        if completed:
            font = QFont(title_label.font())
            font.setStrikeOut(True)
            title_label.setFont(font)
            title_label.setProperty("completed", True)
        subject_text = subject or "Assignment"
        if due_date:
            date = QDate.fromString(due_date, Qt.DateFormat.ISODate)
            due_text = date.toString("MMM d") if date.isValid() else due_date
        else:
            due_text = "No due date"
        details = QLabel(f"{subject_text}  ·  {due_text}")
        details.setObjectName("listMeta")
        details.setWordWrap(True)
        copy.addWidget(title_label)
        copy.addWidget(details)
        row.addLayout(copy, 1)

        priority_label = QLabel(priority or "Medium")
        priority_label.setObjectName("priorityBadge")
        priority_label.setProperty("priority", (priority or "Medium").lower())
        row.addWidget(priority_label, 0, Qt.AlignmentFlag.AlignVCenter)

        remove = QPushButton("×")
        remove.setObjectName("iconButton")
        remove.setAccessibleName(f"Delete {title}")
        remove.setToolTip("Delete task")
        remove.clicked.connect(lambda: self.delete_task(task_id, title))
        row.addWidget(remove, 0, Qt.AlignmentFlag.AlignVCenter)
        return card

    def load_tasks(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, title, subject, due_date, priority, completed
                FROM tasks
                ORDER BY CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END,
                         due_date, id DESC
                """
            )
            tasks = cursor.fetchall()
        finally:
            connection.close()

        for key, button in self.filter_buttons.items():
            button.setProperty("selected", key == self.filter)
            button.style().unpolish(button)
            button.style().polish(button)

        visible = [
            task for task in tasks
            if self.filter == "all"
            or (self.filter == "open" and not task[5])
            or (self.filter == "done" and bool(task[5]))
        ]

        self.clear_list()
        if not visible:
            if not tasks:
                title = "Your task list is clear"
                description = "Add an assignment or deadline and it will show up here."
            elif self.filter == "done":
                title = "No completed tasks yet"
                description = "Finished tasks will show up here."
            else:
                title = "You're all caught up"
                description = "Open tasks will appear here when you add them."
            self.list_layout.addWidget(create_empty_state(title, description))
        else:
            for task in visible:
                self.list_layout.addWidget(self.make_task_card(task))
        self.list_layout.addStretch()

    def toggle_task(self, task_id, completed):
        connection = get_connection()
        try:
            connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?",
                (0 if completed else 1, task_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.load_tasks()

    def delete_task(self, task_id, title):
        answer = QMessageBox.question(
            self,
            "Delete task",
            f"Delete “{title}”?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        connection = get_connection()
        try:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            connection.commit()
        finally:
            connection.close()
        self.load_tasks()

    def open_add_task(self):
        dialog = AddTaskDialog(self)
        if not dialog.exec():
            return

        title = dialog.title.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing task", "Enter a name for this task.")
            return
        subject = dialog.subject.text().strip()
        due_date = "" if dialog.no_due_date.isChecked() else dialog.due_date.date().toString(Qt.DateFormat.ISODate)

        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO tasks (title, subject, due_date, priority)
                VALUES (?, ?, ?, ?)
                """,
                (title, subject, due_date, dialog.priority.currentText()),
            )
            connection.commit()
        finally:
            connection.close()
        self.load_tasks()
