CAMPUSMATE_THEME = """
/* CampusMate · calm, clear, considered */

QWidget {
    color: #202A40;
    font-family: "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

QMainWindow,
QWidget#appBackground,
QWidget#homePage,
QWidget#scheduleScreen,
QWidget#tasksScreen,
QWidget#studyScreen,
QWidget#attendanceScreen,
QWidget#aiTutorScreen {
    background-color: #F4F6FA;
}

QLabel {
    color: #202A40;
    background-color: transparent;
}

QFrame#sidebar {
    background-color: #18233A;
    border-right: 1px solid #26324A;
}

QLabel#logo {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

QLabel#sidebarSubtitle {
    color: #98A5BC;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.6px;
}

QLabel#sectionLabel {
    color: #7F8CA6;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.6px;
}

QFrame#sidebarDivider {
    background-color: #2D3950;
    border: none;
}

QLabel#sidebarFooter {
    color: #98A5BC;
    font-size: 11px;
}

QPushButton {
    background-color: #FFFFFF;
    color: #3B4761;
    border: 1px solid #DCE2EC;
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 12px;
    font-weight: 650;
}

QPushButton:hover {
    background-color: #F7F8FC;
    border-color: #BEC7D8;
}

QPushButton:pressed {
    background-color: #E9EDF6;
}

QPushButton:disabled {
    color: #9BA5B6;
    background-color: #E8EBF1;
    border-color: #E1E5EC;
}

QPushButton#navButton {
    background-color: transparent;
    color: #A7B2C6;
    border: 1px solid transparent;
    border-radius: 10px;
    text-align: left;
    padding: 11px 13px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#navButton:hover {
    background-color: #202D46;
    color: #FFFFFF;
    border-color: #2D3B56;
}

QPushButton#navButton[active="true"] {
    background-color: #2B3954;
    color: #FFFFFF;
    border: 1px solid #3A4A67;
    font-weight: 700;
}

QPushButton#primaryButton {
    background-color: #5968D9;
    color: #FFFFFF;
    border: 1px solid #5968D9;
    border-radius: 10px;
    padding: 11px 17px;
    font-weight: 700;
}

QPushButton#primaryButton:hover {
    background-color: #4D5CC8;
    border-color: #4D5CC8;
}

QPushButton#primaryButton:pressed {
    background-color: #414FAF;
}

QPushButton#heroButton {
    background-color: #FFFFFF;
    color: #4353BA;
    border: 1px solid #FFFFFF;
    border-radius: 10px;
    padding: 11px 16px;
    font-weight: 750;
}

QPushButton#heroButton:hover {
    background-color: #F1F3FF;
    border-color: #F1F3FF;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #68758D;
    border: 1px solid transparent;
}

QPushButton#secondaryButton:hover {
    background-color: #EDF0F6;
    border-color: #E1E5EC;
}

QFrame#heroCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #263A63, stop:0.55 #354C83, stop:1 #5364B5);
    border: 1px solid #53649D;
    border-radius: 20px;
}

QLabel#heroEyebrow {
    color: #C3D0FF;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.8px;
}

QLabel#welcome {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

QLabel#subtitle {
    color: #D1D9F0;
    font-size: 13px;
}

QLabel#heroDate {
    color: #EEF1FF;
    background-color: rgba(255, 255, 255, 24);
    border: 1px solid rgba(255, 255, 255, 40);
    border-radius: 9px;
    padding: 7px 10px;
    font-size: 10px;
    font-weight: 700;
}

QFrame#statCard,
QFrame#card,
QFrame#contentCard {
    background-color: #FFFFFF;
    border: 1px solid #E5E9F0;
    border-radius: 15px;
}

QFrame#statCard[variant="violet"] {
    border-color: #D9DDF7;
}

QFrame#statCard[variant="mint"] {
    border-color: #D4EAE2;
}

QFrame#statCard[variant="amber"] {
    border-color: #F0E4CF;
}

QLabel#statTitle {
    color: #78849A;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.6px;
}

QLabel#statValue {
    color: #1E2940;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -0.6px;
}

QFrame#statAccent {
    background-color: #6573E5;
    border: none;
    border-radius: 2px;
}

QFrame#statAccent[variant="mint"] {
    background-color: #53B895;
}

QFrame#statAccent[variant="amber"] {
    background-color: #E0A94F;
}

QLabel#cardTitle {
    color: #26334B;
    font-size: 13px;
    font-weight: 750;
}

QLabel#muted,
QLabel#listMeta {
    color: #7B879B;
    font-size: 11px;
}

QLabel#listMain {
    color: #26334B;
    font-size: 12px;
    font-weight: 650;
}

QLabel#rowTrailing {
    color: #5F6C83;
    font-size: 10px;
    font-weight: 700;
}

QLabel#rowDot {
    color: #6876E5;
    font-size: 12px;
}

QLabel#rowDot[variant="mint"] {
    color: #53B895;
}

QLabel#rowDot[variant="amber"] {
    color: #E0A94F;
}

QFrame#emptyState {
    background-color: #FFFFFF;
    border: 1px solid #E5E9F0;
    border-radius: 15px;
}

QLabel#emptyStateMark {
    color: #5968D9;
    background-color: #EEF0FF;
    border: 1px solid #E0E4FF;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 700;
}

QLabel#emptyStateTitle {
    color: #26334B;
    font-size: 13px;
    font-weight: 750;
}

QLabel#emptyStateDescription {
    color: #7B879B;
    font-size: 11px;
}

QFrame#dashboardRow {
    background-color: transparent;
    border-bottom: 1px solid #EEF1F5;
}

QLabel#pageTitle {
    color: #1F2B43;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.6px;
}

QLabel#pageSubtitle {
    color: #77849A;
    font-size: 12px;
    padding-bottom: 3px;
}

QLabel#sectionHeading {
    color: #26334B;
    font-size: 14px;
    font-weight: 750;
}

QLabel#timerLabel {
    color: #4F5FC8;
    font-size: 40px;
    font-weight: 800;
}

QLabel#modelBadge {
    color: #4D5B78;
    background-color: #E9EDF7;
    border: 1px solid #DCE2EF;
    border-radius: 11px;
    padding: 9px 13px;
    font-size: 10px;
    font-weight: 700;
}

QPushButton#promptButton {
    color: #596783;
    background-color: #FFFFFF;
    border: 1px solid #E0E5EF;
    border-radius: 16px;
    padding: 8px 13px;
    font-size: 10px;
    font-weight: 650;
}

QPushButton#promptButton:hover {
    color: #4655B6;
    background-color: #F0F2FF;
    border-color: #C9D0F5;
}

QPlainTextEdit#aiChatDisplay {
    background-color: #FFFFFF;
    border: 1px solid #E5E9F0;
    border-radius: 15px;
    padding: 17px;
    line-height: 1.5;
    selection-background-color: #DCE1FF;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox,
QSpinBox,
QDateEdit,
QTimeEdit {
    background-color: #FFFFFF;
    color: #26334B;
    border: 1px solid #DCE2EC;
    border-radius: 9px;
    padding: 10px 11px;
    selection-background-color: #DCE1FF;
    selection-color: #26334B;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus,
QSpinBox:focus,
QDateEdit:focus,
QTimeEdit:focus {
    border: 1px solid #7180E5;
}

QLineEdit::placeholder,
QTextEdit::placeholder,
QPlainTextEdit::placeholder {
    color: #A1ABBA;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #26334B;
    selection-background-color: #EDF0FF;
    selection-color: #26334B;
    border: 1px solid #DCE2EC;
}

QTableWidget,
QTableView {
    background-color: #FFFFFF;
    alternate-background-color: #F8F9FC;
    color: #303B51;
    border: 1px solid #E4E8EF;
    border-radius: 13px;
    gridline-color: transparent;
    selection-background-color: #E9ECFF;
    selection-color: #27345B;
    outline: none;
}

QTableWidget::item,
QTableView::item {
    padding: 9px 11px;
    border: none;
}

QTableWidget::item:selected,
QTableView::item:selected {
    background-color: #E9ECFF;
    color: #27345B;
}

QHeaderView::section {
    background-color: #F1F3F8;
    color: #78849A;
    border: none;
    border-bottom: 1px solid #E4E8EF;
    padding: 12px 11px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.3px;
}

QTableCornerButton::section {
    background-color: #F1F3F8;
    border: none;
}

QScrollArea,
QScrollArea > QWidget > QWidget {
    background-color: transparent;
    border: none;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 9px;
    margin: 4px 1px;
}

QScrollBar::handle:vertical {
    background-color: #CBD2DF;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9AA6BB;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 9px;
    margin: 1px 4px;
}

QScrollBar::handle:horizontal {
    background-color: #CBD2DF;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QDialog,
QMessageBox {
    background-color: #F4F6FA;
    color: #26334B;
}

QDialog QLabel,
QMessageBox QLabel {
    color: #26334B;
}

QCheckBox {
    color: #303B51;
    spacing: 8px;
}

QToolTip {
    background-color: #202A40;
    color: #FFFFFF;
    border: 1px solid #202A40;
    padding: 6px 8px;
    border-radius: 6px;
}
"""
