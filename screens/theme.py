CAMPUSMATE_THEME = """
/* CampusMate Obsidian — Global Theme */

QWidget {
    font-family: "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
    color: #F5F5F5;
}

QMainWindow, QWidget#appBackground, QWidget#homePage,
QWidget#studyScreen, QWidget#scheduleScreen,
QWidget#tasksScreen, QWidget#attendanceScreen,
QWidget#aiTutorScreen {
    background-color: #101114;
}

QWidget#appBackground, QWidget#homePage,
QWidget#scheduleScreen, QWidget#tasksScreen,
QWidget#attendanceScreen, QWidget#aiTutorScreen {
    background-color: #101114;
}

QLabel {
    background-color: transparent;
    color: #F5F5F5;
}

QLabel[role="pageTitle"], QLabel#pageTitle {
    font-size: 28px;
    font-weight: 700;
    color: #F5F5F5;
    padding: 0 0 2px;
}

QLabel[role="subtitle"], QLabel#pageSubtitle {
    font-size: 13px;
    color: #A1A1AA;
    padding-bottom: 8px;
}

QLabel#sectionHeading {
    font-size: 16px;
    font-weight: 700;
    color: #F5F5F5;
}

QFrame#card, QFrame#contentCard {
    background-color: #1C1D22;
    border: 1px solid #35353D;
    border-radius: 14px;
}

QLineEdit, QTextEdit, QPlainTextEdit, QComboBox,
QSpinBox, QDateEdit, QTimeEdit {
    background-color: #17181D;
    color: #F5F5F5;
    border: 1px solid #383941;
    border-radius: 8px;
    padding: 9px 11px;
    selection-background-color: #A78BFA;
    selection-color: #101114;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QComboBox:focus, QSpinBox:focus, QDateEdit:focus,
QTimeEdit:focus {
    border: 1px solid #A78BFA;
}

QComboBox QAbstractItemView {
    background-color: #1C1D22;
    color: #F5F5F5;
    selection-background-color: #383047;
    selection-color: #D8CCFF;
    border: 1px solid #35353D;
}

QPushButton {
    background-color: #23242B;
    color: #F5F5F5;
    border: 1px solid #373842;
    border-radius: 9px;
    padding: 10px 15px;
    font-weight: 600;
}

QPushButton#navButton {
    background-color: transparent;
    color: #B7B7C2;
    border: 1px solid transparent;
    border-radius: 9px;
    text-align: left;
    padding: 11px 12px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #302B3B;
    border-color: #A78BFA;
}

QPushButton:pressed {
    background-color: #3B3150;
}

QPushButton:disabled {
    color: #71717A;
    background-color: #202126;
    border-color: #2C2D34;
}

QPushButton#primaryButton {
    background-color: #A78BFA;
    color: #17121F;
    border: 1px solid #A78BFA;
    font-weight: 700;
    padding: 11px 17px;
}

QPushButton#primaryButton:hover {
    background-color: #B9A4FF;
    border-color: #B9A4FF;
}

QPushButton#heroButton {
    background-color: #C4B5FD;
    color: #17121F;
    border: 1px solid #C4B5FD;
    border-radius: 10px;
    padding: 11px 16px;
    font-weight: 700;
}

QPushButton#heroButton:hover {
    background-color: #D6CCFF;
    border-color: #D6CCFF;
}

QPushButton#secondaryButton {
    background-color: #1C1D22;
    color: #C8C5D2;
    border: 1px solid #35353D;
}

QTableWidget, QTableView {
    background-color: #17181D;
    alternate-background-color: #1D1E24;
    color: #F5F5F5;
    border: 1px solid #34353E;
    border-radius: 12px;
    gridline-color: transparent;
    selection-background-color: #383047;
    selection-color: #F5F5F5;
    outline: none;
}

QHeaderView::section {
    background-color: #22232A;
    color: #D1C6FF;
    border: none;
    border-bottom: 1px solid #363740;
    padding: 13px 12px;
    font-weight: 700;
}

QTableWidget::item, QTableView::item {
    padding: 9px 10px;
    border: none;
}

QTableWidget::item:selected, QTableView::item:selected {
    background-color: #383047;
    color: #F5F5F5;
}

QScrollBar:vertical {
    background-color: #101114;
    width: 9px;
    margin: 3px;
}

QScrollBar::handle:vertical {
    background-color: #484751;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #A78BFA;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #101114;
    height: 9px;
    margin: 3px;
}

QScrollBar::handle:horizontal {
    background-color: #484751;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QDialog, QMessageBox {
    background-color: #15161A;
    color: #F5F5F5;
}

QCheckBox {
    color: #F5F5F5;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QToolTip {
    background-color: #29252F;
    color: #F5F5F5;
    border: 1px solid #484052;
    padding: 6px 8px;
    border-radius: 5px;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #151519;
    border-right: 1px solid #303038;
}

QLabel#logo {
    color: #F5F5F5;
    font-size: 23px;
    font-weight: 800;
}

QLabel#sidebarSubtitle {
    color: #9696A3;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#sectionLabel {
    color: #858592;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#sidebarFooter {
    color: #858592;
    font-size: 11px;
}

QFrame#sidebarDivider {
    background-color: #303038;
    border: none;
}

/* Navigation */
QPushButton#navButton {
    background-color: transparent;
    color: #B7B7C2;
    border: 1px solid transparent;
    border-radius: 9px;
    text-align: left;
    padding: 11px 12px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#navButton:hover {
    background-color: #232229;
    color: #F5F5F5;
    border-color: #35313F;
}

QPushButton#navButton[active="true"] {
    background-color: #2C2538;
    color: #D8CCFF;
    border: 1px solid #46385E;
    font-weight: 700;
}

/* Dashboard typography */
QFrame#heroCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #302844, stop:0.58 #252330, stop:1 #20272B);
    border: 1px solid #484058;
    border-radius: 18px;
}

QLabel#heroEyebrow {
    color: #C4B5FD;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
}

QLabel#welcome {
    color: #F5F5F5;
    font-size: 29px;
    font-weight: 800;
}

QLabel#subtitle {
    color: #C1BDCA;
    font-size: 13px;
}

QLabel#heroDate {
    color: #DBD4E8;
    background-color: #302C39;
    border: 1px solid #494152;
    border-radius: 9px;
    padding: 7px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel#statTitle {
    color: #A1A1AA;
    font-size: 10px;
    font-weight: 700;
}

QLabel#statValue {
    color: #C4B5FD;
    font-size: 30px;
    font-weight: 800;
}

QFrame#statAccent {
    background-color: #A78BFA;
    border: none;
    border-radius: 1px;
}

QFrame#statCard {
    background-color: #1C1D22;
    border: 1px solid #35353D;
    border-radius: 15px;
}

QFrame#statCard[variant="violet"] {
    border-color: #463B60;
}

QFrame#statCard[variant="mint"] {
    border-color: #354B45;
}

QFrame#statCard[variant="amber"] {
    border-color: #514532;
}

QFrame#statAccent[variant="mint"] {
    background-color: #74DCC0;
}

QFrame#statAccent[variant="amber"] {
    background-color: #F1C777;
}

QFrame#card {
    background-color: #1C1D22;
    border: 1px solid #35353D;
    border-radius: 15px;
}

QLabel#cardTitle {
    color: #C4B5FD;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

QLabel#muted {
    color: #C0C0CA;
    font-size: 13px;
}

/* Shared page headings and AI Tutor */
QLabel#pageTitle {
    color: #F5F5F5;
    font-size: 29px;
    font-weight: 800;
}

QLabel#pageSubtitle {
    color: #A7A6B2;
    font-size: 13px;
    padding-bottom: 5px;
}

QLabel#sectionHeading {
    color: #F5F5F5;
    font-size: 16px;
    font-weight: 700;
}

QLabel#timerLabel {
    color: #C4B5FD;
    font-size: 38px;
    font-weight: 700;
}

QPlainTextEdit#aiChatDisplay {
    background-color: #17181D;
    border: 1px solid #35353D;
    border-radius: 14px;
    padding: 15px;
    line-height: 1.45;
}

"""
