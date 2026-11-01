from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox,
)
from database.database import get_connection


class AddTaskDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Task")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.title = QLineEdit()
        self.subject = QLineEdit()
        self.due_date = QLineEdit()

        self.priority = QComboBox()
        self.priority.addItems([
            "Low",
            "Medium",
            "High"
        ])

        self.title.setPlaceholderText("e.g. Maths Assignment")
        self.subject.setPlaceholderText("e.g. Mathematics")
        self.due_date.setPlaceholderText("e.g. 15 Oct 2026")

        layout.addRow("Task:", self.title)
        layout.addRow("Subject:", self.subject)
        layout.addRow("Due Date:", self.due_date)
        layout.addRow("Priority:", self.priority)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


class TasksScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("tasksScreen")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(12)

        # -------------------------
        # Title
        # -------------------------

        title = QLabel("Tasks")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage your assignments and deadlines"
        )

        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -------------------------
        # Task table
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)
        self.table.setObjectName("dataTable")
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(42)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setHorizontalHeaderLabels([
            "Task",
            "Subject",
            "Due Date",
            "Priority",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        # -------------------------
        # Add Task button
        # -------------------------

        add_button = QPushButton("+ Add Task")

        add_button.setObjectName("primaryButton")

        add_button.clicked.connect(self.open_add_task)

        action_row = QHBoxLayout()
        action_row.addStretch()
        action_row.addWidget(add_button)
        layout.addLayout(action_row)

        # Load saved tasks
        self.load_tasks()

    # -------------------------
    # Load tasks
    # -------------------------

    def load_tasks(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT title, subject, due_date,
                   priority, completed
            FROM tasks
            ORDER BY id
        """)

        tasks = cursor.fetchall()

        connection.close()

        self.table.setRowCount(0)

        for task in tasks:

            title = task[0]
            subject = task[1]
            due_date = task[2]
            priority = task[3]
            completed = task[4]

            row = self.table.rowCount()

            self.table.insertRow(row)

            status = "Completed" if completed else "Pending"

            values = [
                title,
                subject,
                due_date,
                priority,
                status
            ]

            for column, value in enumerate(values):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )

    # -------------------------
    # Save task
    # -------------------------

    def save_task_to_database(
        self,
        title,
        subject,
        due_date,
        priority
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks
            (title, subject, due_date, priority)
            VALUES (?, ?, ?, ?)
        """, (
            title,
            subject,
            due_date,
            priority
        ))

        connection.commit()

        connection.close()

    # -------------------------
    # Add task
    # -------------------------

    def open_add_task(self):

        dialog = AddTaskDialog(self)

        if dialog.exec():

            title = dialog.title.text().strip()
            subject = dialog.subject.text().strip()
            due_date = dialog.due_date.text().strip()
            priority = dialog.priority.currentText()

            # Validate required fields and guard against accidental empty strings
            required_fields = {
                "Task": title,
                "Subject": subject,
                "Due Date": due_date,
            }

            if any(value.strip() == "" for value in required_fields.values()):
                QMessageBox.warning(
                    self,
                    "Missing Information",
                    "Please fill in all fields."
                )
                return

            # Save
            self.save_task_to_database(
                title,
                subject,
                due_date,
                priority
            )

            # Reload
            self.load_tasks()
