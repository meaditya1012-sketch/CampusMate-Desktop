
import sys
import sqlite3
from screens.theme import CAMPUSMATE_THEME
from datetime import datetime
from database.database import create_tables, get_connection


from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QSizePolicy,
)

from screens.schedule import ScheduleScreen
from screens.tasks import TasksScreen
from screens.study import StudyScreen
from screens.attendance import AttendanceScreen
from screens.ai_tutor import AITutorScreen


class CampusMate(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CampusMate")
        self.setMinimumSize(1050, 680)
        self.resize(1200, 760)

        self.nav_buttons = []

        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        central.setObjectName("appBackground")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 28, 18, 22)
        sidebar_layout.setSpacing(8)

        logo = QLabel("CampusMate")
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)

        tagline = QLabel("YOUR STUDENT SPACE")
        tagline.setObjectName("sidebarSubtitle")
        sidebar_layout.addWidget(tagline)

        sidebar_layout.addSpacing(30)

        section_label = QLabel("WORKSPACE")
        section_label.setObjectName("sectionLabel")
        sidebar_layout.addWidget(section_label)
        sidebar_layout.addSpacing(8)

        self.home_button = self.create_nav_button(
            "⌂", "Home"
        )
        self.schedule_button = self.create_nav_button(
            "▦", "Schedule"
        )
        self.tasks_button = self.create_nav_button(
            "✓", "Tasks"
        )
        self.study_button = self.create_nav_button(
            "▤", "Study Center"
        )
        self.attendance_button = self.create_nav_button(
            "◷", "Attendance"
        )
        self.ai_button = self.create_nav_button(
            "✧", "AI Tutor"
        )

        for button in [
            self.home_button,
            self.schedule_button,
            self.tasks_button,
            self.study_button,
            self.attendance_button,
            self.ai_button,
        ]:
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        sidebar_divider = QFrame()
        sidebar_divider.setObjectName("sidebarDivider")
        sidebar_divider.setFixedHeight(1)
        sidebar_layout.addWidget(sidebar_divider)

        footer = QLabel("Made for your next big thing.")
        footer.setObjectName("sidebarFooter")
        footer.setWordWrap(True)
        sidebar_layout.addWidget(footer)

        # Page stack: keep all existing screens
        self.pages = QStackedWidget()

        self.home_page = self.create_home_page()
        self.schedule_page = ScheduleScreen()
        self.tasks_page = TasksScreen()
        self.study_page = StudyScreen()
        self.attendance_page = AttendanceScreen()
        self.ai_tutor_page = AITutorScreen()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.schedule_page)
        self.pages.addWidget(self.tasks_page)
        self.pages.addWidget(self.study_page)
        self.pages.addWidget(self.attendance_page)
        self.pages.addWidget(self.ai_tutor_page)

        # Navigation
        self.home_button.clicked.connect(self.show_home)

        self.schedule_button.clicked.connect(
            lambda: self.navigate_to(
                self.schedule_page, self.schedule_button
            )
        )
        self.tasks_button.clicked.connect(
            lambda: self.navigate_to(
                self.tasks_page, self.tasks_button
            )
        )
        self.study_button.clicked.connect(
            lambda: self.navigate_to(
                self.study_page, self.study_button
            )
        )
        self.attendance_button.clicked.connect(
            lambda: self.navigate_to(
                self.attendance_page, self.attendance_button
            )
        )
        self.ai_button.clicked.connect(self.show_ai_tutor)
        self.ask_tutor_button.clicked.connect(self.show_ai_tutor)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        self.apply_styles()

        self.set_active_button(self.home_button)

    def create_nav_button(self, symbol, label):
        button = QPushButton(f"{symbol}     {label}")
        button.setObjectName("navButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(False)
        button.setMinimumHeight(44)
        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.nav_buttons.append(button)
        return button

    def set_active_button(self, active_button):
        for button in self.nav_buttons:
            button.setProperty(
                "active", button is active_button
            )
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def navigate_to(self, page, button):
        self.pages.setCurrentWidget(page)
        self.set_active_button(button)

    def apply_styles(self):
        self.setStyleSheet(CAMPUSMATE_THEME)

    # Dashboard data
    def get_dashboard_data(self):
        today = datetime.now().strftime("%A")

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM classes
                WHERE LOWER(day) = LOWER(?)
                """,
                (today,),
            )
            classes_today = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE completed = 0
                """
            )
            pending_tasks = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT AVG(attended * 100.0 / total)
                FROM attendance
                WHERE total > 0
                """
            )
            attendance_average = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT title, subject, due_date
                FROM tasks
                WHERE completed = 0
                ORDER BY due_date
                LIMIT 5
                """
            )
            upcoming_tasks = cursor.fetchall()

            cursor.execute(
                """
                SELECT subject, start_time, end_time, room
                FROM classes
                WHERE LOWER(day) = LOWER(?)
                ORDER BY start_time
                """,
                (today,),
            )
            todays_classes = cursor.fetchall()

        finally:
            connection.close()

        attendance_text = (
            f"{attendance_average:.1f}%"
            if attendance_average is not None
            else "No data"
        )

        return (
            classes_today,
            pending_tasks,
            attendance_text,
            upcoming_tasks,
            todays_classes,
        )

    # Home dashboard
    def create_home_page(self):
        page = QFrame()
        page.setObjectName("homePage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(34, 26, 34, 24)
        layout.setSpacing(11)

        hero = QFrame()
        hero.setObjectName("heroCard")

        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(18)

        hero_copy = QVBoxLayout()
        hero_copy.setSpacing(7)

        eyebrow = QLabel("YOUR DAY, IN SYNC")
        eyebrow.setObjectName("heroEyebrow")

        welcome = QLabel("Make today count.")
        welcome.setObjectName("welcome")

        subtitle = QLabel(
            "Classes, coursework and focus time — all in one place."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        hero_copy.addWidget(eyebrow)
        hero_copy.addWidget(welcome)
        hero_copy.addWidget(subtitle)
        hero_layout.addLayout(hero_copy, 1)

        hero_actions = QVBoxLayout()
        hero_actions.setSpacing(10)

        today = QLabel(datetime.now().strftime("%A, %B %d"))
        today.setObjectName("heroDate")
        today.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ask_tutor_button = QPushButton("Ask your AI tutor  →")
        self.ask_tutor_button.setObjectName("heroButton")
        self.ask_tutor_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        hero_actions.addWidget(today)
        hero_actions.addStretch()
        hero_actions.addWidget(self.ask_tutor_button)
        hero_layout.addLayout(hero_actions)

        layout.addWidget(hero)
        layout.addSpacing(4)

        self.cards_layout = QHBoxLayout()
        

        layout.addLayout(self.cards_layout)

        self.next_class_box = QFrame()
        self.next_class_box.setObjectName("card")
        self.next_class_layout = QVBoxLayout(
            self.next_class_box
        )
        self.next_class_layout.setContentsMargins(
            20, 18, 20, 18
        )
        self.next_class_layout.setSpacing(10)
        layout.addWidget(self.next_class_box)

        self.tasks_box = QFrame()
        self.tasks_box.setObjectName("card")
        self.tasks_layout = QVBoxLayout(self.tasks_box)
        self.tasks_layout.setContentsMargins(
            20, 18, 20, 18
        )
        self.tasks_layout.setSpacing(10)
        layout.addWidget(self.tasks_box)

        layout.addStretch()

        self.refresh_dashboard()
        return page
    
    def create_card(self, title, value, accent):
        card = QFrame()
        card.setObjectName("statCard")
        card.setProperty("variant", accent)
        card.setMinimumHeight(112)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 14)
        card_layout.setSpacing(8)

        title_label = QLabel(title.upper())
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")

        accent = QFrame()
        accent.setObjectName("statAccent")
        accent.setProperty("variant", card.property("variant"))
        accent.setFixedSize(34, 3)

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        card_layout.addWidget(accent)

        return card


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def refresh_dashboard(self):
        try:
            (
                classes_count,
                pending_count,
                attendance_text,
                upcoming_tasks,
                todays_classes,
            ) = self.get_dashboard_data()

        except sqlite3.Error as error:
            print("Dashboard database error:", error)
            return

        self.clear_layout(self.cards_layout)

        for title, value, accent in [
            ("Today's Classes", str(classes_count), "violet"),
            ("Pending Tasks", str(pending_count), "mint"),
            ("Attendance", attendance_text, "amber"),
        ]:
            self.cards_layout.addWidget(
                self.create_card(title, value, accent)
            )

        # Today's classes
        self.clear_layout(self.next_class_layout)

        heading = QLabel("TODAY'S CLASSES")
        heading.setObjectName("cardTitle")
        self.next_class_layout.addWidget(heading)

        if todays_classes:
            for subject, start, end, room in todays_classes:
                details = f"{start} – {end}"

                if room:
                    details += f"    ·    Room {room}"

                label = QLabel(f"{subject}    {details}")
                label.setObjectName("muted")
                label.setWordWrap(True)
                self.next_class_layout.addWidget(label)
        else:
            label = QLabel("No classes scheduled for today.")
            label.setObjectName("muted")
            self.next_class_layout.addWidget(label)

        # Pending tasks
        self.clear_layout(self.tasks_layout)

        heading = QLabel("PENDING TASKS")
        heading.setObjectName("cardTitle")
        self.tasks_layout.addWidget(heading)

        if upcoming_tasks:
            for title, subject, due_date in upcoming_tasks:
                details = title

                if subject:
                    details += f"    ·    {subject}"

                if due_date:
                    details += f"    ·    Due {due_date}"

                label = QLabel(details)
                label.setObjectName("muted")
                label.setWordWrap(True)
                self.tasks_layout.addWidget(label)
        else:
            label = QLabel("You're all caught up!")
            label.setObjectName("muted")
            self.tasks_layout.addWidget(label)

    def show_home(self):
        self.refresh_dashboard()
        self.navigate_to(self.home_page, self.home_button)

    def show_ai_tutor(self):
        print("Opening CampusMate AI Tutor...")
        self.navigate_to(
            self.ai_tutor_page, self.ai_button
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("CampusMate")
    app.setApplicationName("CampusMate")
    app.setApplicationDisplayName("CampusMate")
    app.setFont(QFont("SF Pro Text", 10))

    create_tables()

    window = CampusMate()
    window.show()

    sys.exit(app.exec())
