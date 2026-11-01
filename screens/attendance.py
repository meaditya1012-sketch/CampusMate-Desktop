from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from database.database import get_connection
from screens.components import create_empty_state


class AddAttendanceDialog(QDialog):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.record = record
        self.setWindowTitle("Edit attendance" if record else "Add attendance")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)
        layout.setContentsMargins(22, 20, 22, 18)
        layout.setSpacing(12)

        self.subject = QLineEdit(record[1] if record else "")
        self.subject.setPlaceholderText("e.g. Applied Mathematics")
        self.attended = QSpinBox()
        self.total = QSpinBox()
        self.attended.setRange(0, 9999)
        self.total.setRange(1, 9999)
        self.attended.setValue(int(record[2]) if record else 0)
        self.total.setValue(max(1, int(record[3])) if record else 1)

        layout.addRow("Subject", self.subject)
        layout.addRow("Classes attended", self.attended)
        layout.addRow("Classes held", self.total)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
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

        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(4)
        title = QLabel("Attendance")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Know where you stand in every subject.")
        subtitle.setObjectName("pageSubtitle")
        heading.addWidget(title)
        heading.addWidget(subtitle)
        header.addLayout(heading, 1)

        add_button = QPushButton("+  Add subject")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(self.open_add_attendance)
        header.addWidget(add_button, 0, Qt.AlignmentFlag.AlignBottom)
        layout.addLayout(header)

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

        self.load_attendance()

    def clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @staticmethod
    def calculate_percentage(attended, total):
        return attended / total * 100 if total else 0

    @staticmethod
    def get_status(percentage):
        if percentage >= 75:
            return "On track", "good"
        if percentage >= 65:
            return "Watch", "watch"
        return "At risk", "risk"

    def make_attendance_card(self, record):
        attendance_id, subject, attended, total = record
        percentage = self.calculate_percentage(attended, total)
        status_text, status_key = self.get_status(percentage)

        card = QFrame()
        card.setObjectName("attendanceItem")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 13, 16, 13)
        layout.setSpacing(9)

        heading = QHBoxLayout()
        heading.setSpacing(9)
        name = QLabel(subject)
        name.setObjectName("listMain")
        name.setWordWrap(True)
        heading.addWidget(name, 1)

        percent = QLabel(f"{percentage:.1f}%")
        percent.setObjectName("attendancePercent")
        heading.addWidget(percent)

        status = QLabel(status_text)
        status.setObjectName("attendanceStatus")
        status.setProperty("status", status_key)
        heading.addWidget(status)
        layout.addLayout(heading)

        progress = QProgressBar()
        progress.setObjectName("attendanceProgress")
        progress.setRange(0, 100)
        progress.setValue(round(max(0, min(100, percentage))))
        progress.setTextVisible(False)
        progress.setProperty("status", status_key)
        progress.setFixedHeight(7)
        layout.addWidget(progress)

        detail = QLabel(f"{attended} attended out of {total} classes")
        detail.setObjectName("listMeta")
        layout.addWidget(detail)

        actions = QHBoxLayout()
        actions.addStretch()
        for label, action in (("Present", "present"), ("Missed", "missed"), ("Edit", "edit")):
            button = QPushButton(label)
            button.setObjectName("smallButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _checked=False, value=action: self.handle_attendance_action(value, attendance_id)
            )
            actions.addWidget(button)

        remove = QPushButton("×")
        remove.setObjectName("iconButton")
        remove.setAccessibleName(f"Remove {subject} attendance")
        remove.setToolTip("Remove subject")
        remove.clicked.connect(lambda: self.delete_attendance(attendance_id, subject))
        actions.addWidget(remove)
        layout.addLayout(actions)
        return card

    def load_attendance(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, subject, attended, total FROM attendance ORDER BY subject COLLATE NOCASE, id"
            )
            records = cursor.fetchall()
        finally:
            connection.close()

        self.clear_list()
        if not records:
            self.list_layout.addWidget(
                create_empty_state(
                    "Start tracking attendance",
                    "Add a subject and log each class to see your progress.",
                )
            )
        else:
            for record in records:
                self.list_layout.addWidget(self.make_attendance_card(record))
        self.list_layout.addStretch()

    def handle_attendance_action(self, action, attendance_id):
        if action == "edit":
            connection = get_connection()
            try:
                record = connection.execute(
                    "SELECT id, subject, attended, total FROM attendance WHERE id = ?",
                    (attendance_id,),
                ).fetchone()
            finally:
                connection.close()
            if record:
                self.save_attendance_dialog(record)
            return

        connection = get_connection()
        try:
            if action == "present":
                connection.execute(
                    "UPDATE attendance SET attended = attended + 1, total = total + 1 WHERE id = ?",
                    (attendance_id,),
                )
            else:
                connection.execute(
                    "UPDATE attendance SET total = total + 1 WHERE id = ?",
                    (attendance_id,),
                )
            connection.commit()
        finally:
            connection.close()
        self.load_attendance()

    def delete_attendance(self, attendance_id, subject):
        answer = QMessageBox.question(
            self,
            "Remove attendance",
            f"Remove attendance for {subject}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        connection = get_connection()
        try:
            connection.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
            connection.commit()
        finally:
            connection.close()
        self.load_attendance()

    def open_add_attendance(self):
        self.save_attendance_dialog()

    def save_attendance_dialog(self, record=None):
        dialog = AddAttendanceDialog(self, record)
        if not dialog.exec():
            return

        subject = dialog.subject.text().strip()
        attended = dialog.attended.value()
        total = dialog.total.value()
        if not subject:
            QMessageBox.warning(self, "Missing subject", "Enter a subject to track.")
            return
        if attended > total:
            QMessageBox.warning(
                self,
                "Invalid attendance",
                "Attended classes cannot be greater than classes held.",
            )
            return

        connection = get_connection()
        try:
            if record:
                duplicate = connection.execute(
                    "SELECT id FROM attendance WHERE subject = ? COLLATE NOCASE AND id != ?",
                    (subject, record[0]),
                ).fetchone()
                if duplicate:
                    QMessageBox.warning(self, "Subject already tracked", "Edit the existing record for this subject.")
                    return
                connection.execute(
                    "UPDATE attendance SET subject = ?, attended = ?, total = ? WHERE id = ?",
                    (subject, attended, total, record[0]),
                )
            else:
                duplicate = connection.execute(
                    "SELECT id FROM attendance WHERE subject = ? COLLATE NOCASE",
                    (subject,),
                ).fetchone()
                if duplicate:
                    QMessageBox.warning(self, "Subject already tracked", "Edit the existing record for this subject.")
                    return
                connection.execute(
                    "INSERT INTO attendance (subject, attended, total) VALUES (?, ?, ?)",
                    (subject, attended, total),
                )
            connection.commit()
        finally:
            connection.close()
        self.load_attendance()
