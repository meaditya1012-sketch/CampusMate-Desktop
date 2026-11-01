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
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

QLabel#logoMark {
    color: #FFFFFF;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #5368BD, stop:1 #334A78);
    border: 1px solid rgba(255, 255, 255, 28);
    border-radius: 11px;
    font-size: 17px;
    font-weight: 800;
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

QFrame#scheduleItem,
QFrame#taskItem,
QFrame#attendanceItem,
QFrame#subjectItem,
QFrame#noteItem {
    background-color: #FFFFFF;
    border: 1px solid #E5E9F0;
    border-radius: 13px;
}

QLabel#scheduleTime {
    color: #5262C4;
    font-size: 10px;
    font-weight: 750;
    line-height: 1.5;
}

QPushButton#iconButton {
    min-width: 31px;
    max-width: 31px;
    min-height: 31px;
    max-height: 31px;
    padding: 0;
    color: #8591A5;
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    font-size: 18px;
    font-weight: 400;
}

QPushButton#iconButton:hover {
    color: #C45D64;
    background-color: #FFF0F1;
    border-color: #F4DADD;
}

QPushButton#taskToggle {
    min-width: 23px;
    max-width: 23px;
    min-height: 23px;
    max-height: 23px;
    padding: 0;
    color: #FFFFFF;
    background-color: #FFFFFF;
    border: 1.5px solid #C7CFDD;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 800;
}

QPushButton#taskToggle:hover {
    border-color: #5968D9;
}

QPushButton#taskToggle[complete="true"] {
    background-color: #51B795;
    border-color: #51B795;
}

QLabel#listMain[completed="true"] {
    color: #8A95A7;
}

QLabel#priorityBadge {
    padding: 5px 8px;
    color: #627087;
    background-color: #F1F3F7;
    border: none;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 750;
}

QLabel#priorityBadge[priority="high"] {
    color: #BD5D67;
    background-color: #FFF0F1;
}

QLabel#priorityBadge[priority="medium"] {
    color: #A57529;
    background-color: #FFF5E6;
}

QLabel#priorityBadge[priority="low"] {
    color: #42896F;
    background-color: #EAF7F1;
}

QPushButton#filterButton {
    min-height: 31px;
    padding: 0 11px;
    color: #727F95;
    background-color: #FFFFFF;
    border: 1px solid #E1E6EF;
    border-radius: 15px;
    font-size: 10px;
    font-weight: 680;
}

QPushButton#filterButton[selected="true"] {
    color: #4F5FC1;
    background-color: #EEF0FF;
    border-color: #D8DDFA;
}

QPushButton#filterButton:hover {
    border-color: #BEC7D8;
}

QPushButton#smallButton {
    min-height: 31px;
    padding: 0 10px;
    color: #58667D;
    background-color: #FFFFFF;
    border: 1px solid #E1E6EF;
    border-radius: 9px;
    font-size: 10px;
    font-weight: 700;
}

QPushButton#smallButton:hover {
    color: #4F5FC1;
    background-color: #F0F2FF;
    border-color: #D1D8F6;
}

QLabel#attendancePercent {
    color: #29354C;
    font-size: 17px;
    font-weight: 800;
}

QLabel#attendanceStatus {
    padding: 5px 8px;
    color: #438B70;
    background-color: #EAF7F1;
    border: none;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 700;
}

QLabel#attendanceStatus[status="watch"] {
    color: #A57529;
    background-color: #FFF5E6;
}

QLabel#attendanceStatus[status="risk"] {
    color: #BD5D67;
    background-color: #FFF0F1;
}

QProgressBar#attendanceProgress,
QProgressBar#studyProgress {
    background-color: #EDF0F5;
    border: none;
    border-radius: 4px;
}

QProgressBar#attendanceProgress::chunk,
QProgressBar#studyProgress::chunk {
    background-color: #55B996;
    border-radius: 4px;
}

QProgressBar#attendanceProgress[status="watch"]::chunk {
    background-color: #D99B43;
}

QProgressBar#attendanceProgress[status="risk"]::chunk {
    background-color: #CB6570;
}

QLabel#subjectGoal {
    color: #7C889E;
    font-size: 9px;
    font-weight: 650;
}

QLabel#studyPercent {
    color: #4C5BB9;
    font-size: 9px;
    font-weight: 750;
}

QLabel#noteIcon {
    color: #5968C9;
    background-color: #EEF0FF;
    border: 1px solid #E3E6FF;
    border-radius: 8px;
    font-size: 14px;
}

QPushButton#noteLink {
    padding: 0;
    color: #29354C;
    background-color: transparent;
    border: none;
    text-align: left;
    font-size: 11px;
    font-weight: 750;
}

QPushButton#noteLink:hover {
    color: #4F5FC1;
}

QLabel#notePreview {
    color: #7E8BA0;
    font-size: 10px;
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
