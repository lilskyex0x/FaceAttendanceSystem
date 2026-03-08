# Global theme using the requested palette:
# #254F22, #A03A13, #F5824A, #EDE4C2

NEON_STYLE = """
QWidget {
    background-color: #254F22;
    color: #EDE4C2;
    font-size: 14px;
}

QLabel {
    color: #EDE4C2;
}

QPushButton {
    background-color: #F5824A;
    color: #254F22;
    border-radius: 8px;
    padding: 8px 12px;
    font-weight: 600;
    border: 1px solid #A03A13;
}

QPushButton:hover {
    background-color: #A03A13;
    color: #EDE4C2;
}

QPushButton:pressed {
    background-color: #254F22;
    border: 1px solid #F5824A;
    color: #EDE4C2;
}

QPushButton:disabled {
    background-color: #EDE4C2;
    color: #A03A13;
    border-color: #F5824A;
}

QTableWidget {
    background-color: #EDE4C2;
    color: #254F22;
    gridline-color: #A03A13;
    selection-background-color: #F5824A;
    selection-color: #254F22;
}

QHeaderView::section {
    background-color: #A03A13;
    color: #EDE4C2;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #F5824A;
}

QScrollBar:vertical {
    background: #254F22;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #A03A13;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #F5824A;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
