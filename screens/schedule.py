from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from database.database import get_connection
from screens.components import create_empty_state


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a class")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)
        layout.setContentsMargins(22, 20, 22, 18)
        layout.setSpacing(12)

        from PySide6.QtWidgets import QLineEdit

        self.subject = QLineEdit()
        self.teacher = QLineEdit()
        self.room = QLineEdit()
        self.day = QComboBox()
        self.day.addItems(DAYS)
        self.start_time = QTimeEdit(QTime(9, 0))
        self.end_time = QTimeEdit(QTime(10, 0))
        self.start_time.setDisplayFormat("h:mm AP")
        self.end_time.setDisplayFormat("h:mm AP")

        self.subject.setPlaceholderText("e.g. Data Structures")
        self.teacher.setPlaceholderText("e.g. Prof. Shah")
        self.room.setPlaceholderText("e.g. B-204")
        self.day.setCurrentText("Monday")

        layout.addRow("Subject", self.subject)
        layout.addRow("Teacher", self.teacher)
        layout.addRow("Day", self.day)
        layout.addRow("Starts", self.start_time)
        layout.addRow("Ends", self.end_time)
        layout.addRow("Room", self.room)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
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
        layout.setSpacing(16)

        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(4)

        title = QLabel("Schedule")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Keep your week in view.")
        subtitle.setObjectName("pageSubtitle")
        heading.addWidget(title)
        heading.addWidget(subtitle)
        header.addLayout(heading, 1)

        add_button = QPushButton("+  Add class")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(self.open_add_class)
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

        self.load_classes()

    @staticmethod
    def format_time(value):
        value = str(value or "")
        for pattern in ("HH:mm", "h:mm AP", "h:mm A"):
            parsed = QTime.fromString(value, pattern)
            if parsed.isValid():
                return parsed.toString("h:mm AP")
        return value

    @staticmethod
    def time_sort_key(value):
        for pattern in ("HH:mm", "h:mm AP", "h:mm A"):
            parsed = QTime.fromString(str(value or ""), pattern)
            if parsed.isValid():
                return parsed.hour() * 60 + parsed.minute()
        return 24 * 60

    def clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def make_class_card(self, record):
        class_id, day, subject, teacher, start, end, room = record
        card = QFrame()
        card.setObjectName("scheduleItem")

        row = QHBoxLayout(card)
        row.setContentsMargins(15, 12, 13, 12)
        row.setSpacing(15)

        time = QLabel(
            f"{self.format_time(start)} – {self.format_time(end)}\n{day}"
        )
        time.setObjectName("scheduleTime")
        time.setMinimumWidth(112)
        row.addWidget(time)

        details = QVBoxLayout()
        details.setSpacing(3)
        name = QLabel(subject)
        name.setObjectName("listMain")
        name.setWordWrap(True)
        metadata = " · ".join(
            value for value in (teacher, f"Room {room}" if room else "") if value
        ) or "Class"
        meta = QLabel(metadata)
        meta.setObjectName("listMeta")
        meta.setWordWrap(True)
        details.addWidget(name)
        details.addWidget(meta)
        row.addLayout(details, 1)

        remove = QPushButton("×")
        remove.setObjectName("iconButton")
        remove.setToolTip("Remove class")
        remove.setAccessibleName(f"Remove {subject}")
        remove.clicked.connect(lambda: self.delete_class(class_id, subject))
        row.addWidget(remove, 0, Qt.AlignmentFlag.AlignVCenter)
        return card

    def load_classes(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, day, subject, teacher, start_time, end_time, room
                FROM classes
                """
            )
            records = cursor.fetchall()
        finally:
            connection.close()

        day_order = {day.lower(): index for index, day in enumerate(DAYS)}
        records.sort(
            key=lambda row: (
                day_order.get(str(row[1]).lower(), len(DAYS)),
                self.time_sort_key(row[4]),
            )
        )

        self.clear_list()
        if not records:
            self.list_layout.addWidget(
                create_empty_state(
                    "Your week is open",
                    "Add your first class to start building a timetable.",
                )
            )
        else:
            for record in records:
                self.list_layout.addWidget(self.make_class_card(record))
        self.list_layout.addStretch()

    def delete_class(self, class_id, subject):
        answer = QMessageBox.question(
            self,
            "Remove class",
            f"Remove {subject} from your schedule?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        connection = get_connection()
        try:
            connection.execute("DELETE FROM classes WHERE id = ?", (class_id,))
            connection.commit()
        finally:
            connection.close()
        self.load_classes()

    def open_add_class(self):
        dialog = AddClassDialog(self)
        if not dialog.exec():
            return

        subject = dialog.subject.text().strip()
        if not subject:
            QMessageBox.warning(self, "Missing subject", "Enter a subject for this class.")
            return

        start = dialog.start_time.time()
        end = dialog.end_time.time()
        if end <= start:
            QMessageBox.warning(self, "Invalid time", "End time must be later than start time.")
            return

        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO classes (subject, teacher, day, start_time, end_time, room)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    subject,
                    dialog.teacher.text().strip(),
                    dialog.day.currentText(),
                    start.toString("HH:mm"),
                    end.toString("HH:mm"),
                    dialog.room.text().strip(),
                ),
            )
            connection.commit()
        finally:
            connection.close()
        self.load_classes()
