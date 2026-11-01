
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
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
from screens.components import create_empty_state, fit_table_height


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
        layout.setSpacing(16)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(4)
        title = QLabel("Attendance")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Track your attendance for every subject"
        )

        subtitle.setObjectName("pageSubtitle")

        heading_layout.addWidget(title)
        heading_layout.addWidget(subtitle)
        header_row.addLayout(heading_layout, 1)

        add_button = QPushButton("+  Add subject")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(self.open_add_attendance)
        header_row.addWidget(
            add_button,
            0,
            Qt.AlignmentFlag.AlignBottom,
        )
        layout.addLayout(header_row)

        self.empty_state = create_empty_state(
            "Attendance starts here",
            "Add a subject and your attended classes to track your progress.",
        )
        layout.addWidget(self.empty_state)

        # -------------------------
        # Attendance table
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)
        self.table.setObjectName("dataTable")
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(46)
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

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        layout.addStretch()

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
            return "On track"

        elif percentage >= 65:
            return "Watch"

        else:
            return "At risk"

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
                item = QTableWidgetItem(value)
                if column == 4:
                    status_colors = {
                        "On track": "#4D987B",
                        "Watch": "#B88739",
                        "At risk": "#C45D64",
                    }
                    item.setForeground(QColor(status_colors[value]))
                self.table.setItem(row, column, item)

        has_records = bool(records)
        self.empty_state.setVisible(not has_records)
        self.table.setVisible(has_records)
        if has_records:
            fit_table_height(self.table, len(records))

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
