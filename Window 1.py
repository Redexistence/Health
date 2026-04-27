import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

app = QApplication(sys.argv)

main_win = QWidget()
main_win.setWindowTitle("Health Status Detection Program")
main_win.setGeometry(300, 100, 700, 600)

layout = QVBoxLayout()
layout.setSpacing(12)
layout.setContentsMargins(50, 40, 50, 40)

# Title
title = QLabel("Welcome to the Health Status Detection Program!")
title.setAlignment(Qt.AlignCenter)
title.setStyleSheet("font-size: 20px; font-weight: bold;")
title.setWordWrap(True)

# Subtitle
subtitle = QLabel("This application allows you to use the Ruffier Test to make an initial diagnosis of your health.")
subtitle.setAlignment(Qt.AlignCenter)
subtitle.setStyleSheet("font-size: 14px; color: #444;")
subtitle.setWordWrap(True)

# Divider label
procedure_title = QLabel("── How the Test Works ──")
procedure_title.setAlignment(Qt.AlignCenter)
procedure_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #888; margin-top: 10px;")

# Numbered steps
steps = [
    "1.  Lie in the supine (flat on your back) position for 5 minutes.",
    "2.  Your pulse rate is measured for 15 seconds (P1).",
    "3.  Within 45 seconds, perform 30 squats.",
    "4.  Immediately after exercise, lie back down.",
    "5.  Your pulse is measured again for the first 15 seconds of recovery (P2).",
    "6.  Your pulse is measured once more for the last 15 seconds of the first minute of recovery (P3).",
]

step_labels = []
for step in steps:
    lbl = QLabel(step)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setStyleSheet("font-size: 13px;")
    lbl.setWordWrap(True)
    step_labels.append(lbl)

# Safety warning
warning = QLabel(
    "⚠️  Important! If you feel unwell during the test\n"
    "(dizziness, tinnitus, shortness of breath, etc.),\n"
    "stop the test immediately and consult a physician."
)
warning.setAlignment(Qt.AlignCenter)
warning.setStyleSheet(
    "font-size: 13px; color: #b00000; font-weight: bold;"
    "background-color: #fff0f0; border: 1px solid #f5c0c0;"
    "border-radius: 8px; padding: 10px; margin-top: 10px;"
)
warning.setWordWrap(True)

# Start button
start_btn = QPushButton("Start")
start_btn.setFixedSize(160, 45)
start_btn.setStyleSheet(
    "font-size: 15px; background-color: #4CAF50; color: white;"
    "border-radius: 8px; margin-top: 15px;"
)

# Add everything to layout
layout.addWidget(title)
layout.addWidget(subtitle)
layout.addWidget(procedure_title)
for lbl in step_labels:
    layout.addWidget(lbl)
layout.addWidget(warning)
layout.addStretch()
layout.addWidget(start_btn, alignment=Qt.AlignCenter)

main_win.setLayout(layout)
main_win.show()

sys.exit(app.exec_())