import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QScrollArea)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont

class RuffierSecondScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Status Detection - Step 2")
        self.setMinimumSize(900, 750)
        
        # Unified Stylesheet (Matching Page 1)
        self.setStyleSheet("""
            QWidget { background-color: #f4f4f4; font-family: 'Segoe UI', Arial; }
            QLabel { color: #333; line-height: 1.6; }
            QLineEdit { 
                padding: 10px; border: 1px solid #ccc; border-radius: 5px; 
                background: white; font-size: 14px; min-width: 250px;
            }
            QPushButton { 
                background-color: #00b341; color: white; border-radius: 8px; 
                padding: 12px 30px; font-weight: bold; font-size: 16px; border: none;
            }
            QPushButton:hover { background-color: #008f33; }
            QFrame#WarningBox { 
                background-color: #fff0f0; border: 1px solid #ffcccc; border-radius: 10px; 
            }
            QLabel#TimerDisplay { 
                font-size: 72px; font-weight: bold; color: #000; margin: 20px;
            }
        """)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(50, 40, 50, 40)
        self.main_layout.setSpacing(25)

        # 1. Header (Centered)
        header = QLabel("Health Assessment in Progress")
        header.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(header)

        # 2. User Info Inputs (Centered)
        input_container = QVBoxLayout()
        input_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter your age")
        
        input_container.addWidget(QLabel("<b>Full Name:</b>"))
        input_container.addWidget(self.name_input)
        input_container.addWidget(QLabel("<b>Age:</b>"))
        input_container.addWidget(self.age_input)
        self.main_layout.addLayout(input_container)

        # 3. Instruction & Timer Area
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setObjectName("TimerDisplay")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.timer_label)

        # 4. Action Buttons (Matching Page 1 'Start' style)
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_p1 = QPushButton("Start Initial Pulse (P1)")
        self.btn_squats = QPushButton("Start Squats Counter")
        self.btn_p2p3 = QPushButton("Start Final Recovery (P2/P3)")
        
        for btn in [self.btn_p1, self.btn_squats, self.btn_p2p3]:
            btn.setFixedWidth(400)
            btn_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addLayout(btn_layout)

        # 5. The Results Area (Inputs for P1, P2, P3)
        self.results_layout = QHBoxLayout()
        self.p1_res = QLineEdit(); self.p1_res.setPlaceholderText("P1 result")
        self.p2_res = QLineEdit(); self.p2_res.setPlaceholderText("P2 result")
        self.p3_res = QLineEdit(); self.p3_res.setPlaceholderText("P3 result")
        
        for res in [self.p1_res, self.p2_res, self.p3_res]:
            res.setFixedWidth(120)
            self.results_layout.addWidget(res)
        self.main_layout.addLayout(self.results_layout)

        # 6. Important Warning (Matching Page 1 style)
        self.warning_box = QFrame()
        self.warning_box.setObjectName("WarningBox")
        warn_layout = QVBoxLayout(self.warning_box)
        warn_text = QLabel("⚠️ <b>Important!</b> If you feel unwell during the test\n"
                           "(dizziness, tinnitus, shortness of breath, etc.),\n"
                           "stop the test immediately and consult a physician.")
        warn_text.setStyleSheet("color: #cc0000; font-size: 13px;")
        warn_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warn_layout.addWidget(warn_text)
        self.main_layout.addWidget(self.warning_box)

        # 7. Final Submit Button
        self.submit_btn = QPushButton("Send Results")
        self.main_layout.addWidget(self.submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Logic
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.time_left = 0

        self.btn_p1.clicked.connect(lambda: self.run_test(15))
        self.btn_squats.clicked.connect(lambda: self.run_test(45))
        self.btn_p2p3.clicked.connect(lambda: self.run_test(60))

    def run_test(self, seconds):
        self.time_left = seconds
        self.timer.start(1000)
        self.update_display()

    def update_clock(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            # Visual cue for P2/P3 measurement windows
            if self.time_left <= 15 or self.time_left >= 45:
                self.timer_label.setStyleSheet("color: #00b341;") # Green
            else:
                self.timer_label.setStyleSheet("color: #000;") # Black
        else:
            self.timer.stop()

    def update_display(self):
        time_obj = QTime(0, 0).addSecs(self.time_left)
        self.timer_label.setText(time_obj.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RuffierSecondScreen()
    ex.show()
    sys.exit(app.exec())
