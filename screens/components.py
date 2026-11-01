from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)


def create_empty_state(title, description):
    frame = QFrame()
    frame.setObjectName("emptyState")
    frame.setMinimumHeight(118)

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(22, 20, 22, 20)
    layout.setSpacing(14)

    mark = QLabel("✦")
    mark.setObjectName("emptyStateMark")
    mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
    mark.setFixedSize(38, 38)
    layout.addWidget(mark, 0)

    copy = QVBoxLayout()
    copy.setSpacing(4)

    title_label = QLabel(title)
    title_label.setObjectName("emptyStateTitle")

    description_label = QLabel(description)
    description_label.setObjectName("emptyStateDescription")
    description_label.setWordWrap(True)

    copy.addWidget(title_label)
    copy.addWidget(description_label)
    layout.addLayout(copy, 1)

    frame.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed,
    )
    return frame


def fit_table_height(table, row_count, maximum=540, row_height=46):
    header_height = max(table.horizontalHeader().sizeHint().height(), 40)
    visible_rows = max(row_count, 1)
    desired_height = header_height + visible_rows * row_height + 10

    table.setMinimumHeight(0)
    table.setMaximumHeight(min(desired_height, maximum))
    table.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Preferred,
    )
