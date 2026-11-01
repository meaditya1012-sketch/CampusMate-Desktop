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
    QDialogButtonBox,
    QMessageBox,
)
from database.database import get_connection


class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Class")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.subject = QLineEdit()
        self.teacher = QLineEdit()
        self.day = QLineEdit()
        self.start_time = QLineEdit()
        self.end_time = QLineEdit()
        self.room = QLineEdit()

        self.subject.setPlaceholderText("e.g. Mathematics")
        self.teacher.setPlaceholderText("e.g. Dr. Sharma")
        self.day.setPlaceholderText("e.g. Monday")
        self.start_time.setPlaceholderText("e.g. 09:00 AM")
        self.end_time.setPlaceholderText("e.g. 10:00 AM")
        self.room.setPlaceholderText("e.g. Room 101")

        layout.addRow("Subject:", self.subject)
        layout.addRow("Teacher:", self.teacher)
        layout.addRow("Day:", self.day)
        layout.addRow("Start Time:", self.start_time)
        layout.addRow("End Time:", self.end_time)
        layout.addRow("Room:", self.room)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


class ScheduleScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("scheduleScreen")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(12)

        # Title
        title = QLabel("Schedule")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Your weekly class timetable")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Schedule table
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
            "Day",
            "Subject",
            "Teacher",
            "Time",
            "Room"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        # Add Class button
        add_button = QPushButton("+ Add Class")

        add_button.setObjectName("primaryButton")

        add_button.clicked.connect(self.open_add_class)

        action_row = QHBoxLayout()
        action_row.addStretch()
        action_row.addWidget(add_button)
        layout.addLayout(action_row)

        # Load saved classes
        self.load_classes()

    # --------------------------------
    # Load classes from database
    # --------------------------------

    def load_classes(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT day, subject, teacher,
                   start_time, end_time, room
            FROM classes
            ORDER BY id
        """)

        classes = cursor.fetchall()

        connection.close()

        self.table.setRowCount(0)

        for class_data in classes:

            day = class_data[0]
            subject = class_data[1]
            teacher = class_data[2]
            start_time = class_data[3]
            end_time = class_data[4]
            room = class_data[5]

            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                day,
                subject,
                teacher,
                f"{start_time} - {end_time}",
                room
            ]

            for column, value in enumerate(values):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

    # --------------------------------
    # Save class to database
    # --------------------------------

    def save_class_to_database(
        self,
        subject,
        teacher,
        day,
        start_time,
        end_time,
        room
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO classes
            (subject, teacher, day, start_time, end_time, room)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            subject,
            teacher,
            day,
            start_time,
            end_time,
            room
        ))

        connection.commit()

        connection.close()

    # --------------------------------
    # Add class
    # --------------------------------

    def open_add_class(self):

        dialog = AddClassDialog(self)

        if dialog.exec():

            subject = dialog.subject.text().strip()
            teacher = dialog.teacher.text().strip()
            day = dialog.day.text().strip()
            start_time = dialog.start_time.text().strip()
            end_time = dialog.end_time.text().strip()
            room = dialog.room.text().strip()

            # Validation
            if not all([
                subject,
                teacher,
                day,
                start_time,
                end_time,
                room
            ]):

                QMessageBox.warning(
                    self,
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            # Save to database
            self.save_class_to_database(
                subject,
                teacher,
                day,
                start_time,
                end_time,
                room
            )

            # Reload table
            self.load_classes()
