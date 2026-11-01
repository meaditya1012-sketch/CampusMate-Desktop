
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


class AddAttendanceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Attendance")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.subject = QLineEdit()
        self.attended = QLineEdit()
        self.total = QLineEdit()

        self.subject.setPlaceholderText("e.g. Mathematics")
        self.attended.setPlaceholderText("e.g. 18")
        self.total.setPlaceholderText("e.g. 20")

        layout.addRow("Subject:", self.subject)
        layout.addRow("Attended Classes:", self.attended)
        layout.addRow("Total Classes:", self.total)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)


class AttendanceScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("attendanceScreen")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(12)

        # -------------------------
        # Title
        # -------------------------

        title = QLabel("Attendance")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Track your attendance for every subject"
        )

        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -------------------------
        # Attendance table
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
            "Subject",
            "Attended",
            "Total",
            "Percentage",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        # -------------------------
        # Add button
        # -------------------------

        add_button = QPushButton("+ Add Subject")

        add_button.setObjectName("primaryButton")

        add_button.clicked.connect(self.open_add_attendance)

        action_row = QHBoxLayout()
        action_row.addStretch()
        action_row.addWidget(add_button)
        layout.addLayout(action_row)

        # Load saved attendance
        self.load_attendance()

    # -------------------------
    # Calculate percentage
    # -------------------------

    def calculate_percentage(self, attended, total):

        if total == 0:
            return 0

        return (attended / total) * 100

    # -------------------------
    # Get status
    # -------------------------

    def get_status(self, percentage):

        if percentage >= 75:
            return "🟢 Good"

        elif percentage >= 65:
            return "🟡 Warning"

        else:
            return "🔴 Low"

    # -------------------------
    # Load attendance
    # -------------------------

    def load_attendance(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT subject, attended, total
            FROM attendance
            ORDER BY id
        """)

        records = cursor.fetchall()

        connection.close()

        self.table.setRowCount(0)

        for record in records:

            subject = record[0]
            attended = record[1]
            total = record[2]

            percentage = self.calculate_percentage(
                attended,
                total
            )

            status = self.get_status(percentage)

            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                subject,
                str(attended),
                str(total),
                f"{percentage:.1f}%",
                status
            ]

            for column, value in enumerate(values):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

    # -------------------------
    # Save attendance
    # -------------------------

    def save_attendance(
        self,
        subject,
        attended,
        total
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO attendance
            (subject, attended, total)
            VALUES (?, ?, ?)
        """, (
            subject,
            attended,
            total
        ))

        connection.commit()

        connection.close()

    # -------------------------
    # Add attendance
    # -------------------------

    def open_add_attendance(self):

        dialog = AddAttendanceDialog(self)

        if dialog.exec():

            subject = dialog.subject.text().strip()
            attended_text = dialog.attended.text().strip()
            total_text = dialog.total.text().strip()

            # -------------------------
            # Empty field validation
            # -------------------------

            if not subject or not attended_text or not total_text:

                QMessageBox.warning(
                    self,
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            # -------------------------
            # Number validation
            # -------------------------

            try:

                attended = int(attended_text)
                total = int(total_text)

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Invalid Numbers",
                    "Attended and Total Classes must be numbers."
                )

                return

            # -------------------------
            # Value validation
            # -------------------------

            if total <= 0:

                QMessageBox.warning(
                    self,
                    "Invalid Total",
                    "Total classes must be greater than 0."
                )

                return

            if attended < 0:

                QMessageBox.warning(
                    self,
                    "Invalid Attendance",
                    "Attended classes cannot be negative."
                )

                return

            if attended > total:

                QMessageBox.warning(
                    self,
                    "Invalid Attendance",
                    "Attended classes cannot be greater than total classes."
                )

                return

            # -------------------------
            # Save
            # -------------------------

            self.save_attendance(
                subject,
                attended,
                total
            )

            # Reload table
            self.load_attendance()
