import sys
import csv
import os
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QStackedWidget,
    QProgressBar, QSizePolicy, QTableWidget, QTableWidgetItem,
    QHeaderView
)
try:
    from PyQt5.QtMultimedia import QSound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# ─────────────────────────────────────────────
#  SHARED STYLE
# ─────────────────────────────────────────────
APP_STYLE = """
    QWidget {
        background-color: #f4f4f4;
        font-family: 'Segoe UI', Arial;
        color: #333;
    }
    QLineEdit {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        background: white;
        font-size: 14px;
        min-width: 250px;
    }
    QLineEdit:focus {
        border: 2px solid #4CAF50;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 15px;
        border: none;
    }
    QPushButton:hover { background-color: #388E3C; }
    QPushButton:disabled {
        background-color: #aaa;
        color: #eee;
    }
    QFrame#WarningBox {
        background-color: #fff0f0;
        border: 1px solid #ffcccc;
        border-radius: 10px;
    }
    QProgressBar {
        border: 1px solid #ccc;
        border-radius: 6px;
        background: #e0e0e0;
        height: 12px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #4CAF50;
        border-radius: 6px;
    }
    QTableWidget {
        background: white;
        border: 1px solid #ddd;
        border-radius: 6px;
        font-size: 12px;
    }
    QHeaderView::section {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 6px;
        border: none;
    }
"""

CSV_FILE = os.path.expanduser("~/ruffier_history.csv")

def make_title(text, size=20):
    lbl = QLabel(text)
    lbl.setFont(QFont("Arial", size, QFont.Bold))
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setWordWrap(True)
    return lbl

def make_label(text, size=13, color="#333"):
    lbl = QLabel(text)
    lbl.setFont(QFont("Arial", size))
    lbl.setStyleSheet(f"color: {color};")
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setWordWrap(True)
    return lbl

def make_warning():
    box = QFrame()
    box.setObjectName("WarningBox")
    box.setMinimumHeight(90)
    layout = QVBoxLayout(box)
    lbl = QLabel(
        "⚠️  Important! If you feel unwell during the test\n"
        "(dizziness, tinnitus, shortness of breath, etc.),\n"
        "stop the test immediately and consult a physician."
    )
    lbl.setStyleSheet("color: #cc0000; font-size: 13px; font-weight: bold;")
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setWordWrap(True)
    layout.addWidget(lbl)
    return box

def make_button(text, width=200):
    btn = QPushButton(text)
    btn.setFixedWidth(width)
    return btn

def make_progress_bar(step):
    bar = QProgressBar()
    bar.setMaximum(3)
    bar.setValue(step)
    bar.setFormat(f"Step {step} of 3")
    bar.setFixedHeight(18)
    return bar

def save_to_csv(name, age, p1, p2, p3, index, performance):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Name", "Age", "P1", "P2", "P3", "Index", "Performance"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            name, age, p1, p2, p3, index, performance
        ])

def load_history():
    if not os.path.isfile(CSV_FILE):
        return []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ─────────────────────────────────────────────
#  WINDOW 1 — Introduction
# ─────────────────────────────────────────────
class IntroWindow(QWidget):
    def __init__(self, on_start):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(12)

        layout.addWidget(make_progress_bar(1))
        layout.addWidget(make_title("Welcome to the Health Status Detection Program!", 20))
        layout.addWidget(make_label(
            "This application allows you to use the Ruffier Test "
            "to make an initial diagnosis of your health.", 14, "#444"
        ))

        layout.addWidget(make_label("── How the Test Works ──", 13, "#888"))

        steps = [
            "1.  Lie in the supine (flat on your back) position for 5 minutes.",
            "2.  Your pulse rate is measured for 15 seconds (P1).",
            "3.  Within 45 seconds, perform 30 squats.",
            "4.  Immediately after exercise, lie back down.",
            "5.  Your pulse is measured again for the first 15 seconds of recovery (P2).",
            "6.  Your pulse is measured once more for the last 15 seconds of the first minute of recovery (P3).",
        ]
        for step in steps:
            layout.addWidget(make_label(step, 13))

        layout.addWidget(make_warning())
        layout.addStretch()

        btn = make_button("Start")
        btn.clicked.connect(on_start)
        layout.addWidget(btn, alignment=Qt.AlignCenter)


# ─────────────────────────────────────────────
#  WINDOW 2 — Test Screen
# ─────────────────────────────────────────────
class TestWindow(QWidget):
    def __init__(self, on_submit, on_back):
        super().__init__()
        self.on_submit = on_submit
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(14)

        # Progress + back
        top_row = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedWidth(100)
        back_btn.setStyleSheet(
            "background-color: #888; color: white; border-radius: 8px;"
            "padding: 8px; font-size: 13px; font-weight: bold;"
        )
        back_btn.clicked.connect(on_back)
        top_row.addWidget(back_btn)
        top_row.addWidget(make_progress_bar(2))
        layout.addLayout(top_row)

        layout.addWidget(make_title("Health Assessment in Progress", 20))

        # Name & Age
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name (optional)")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter your age *")

        layout.addWidget(make_label("Full Name:", 13))
        layout.addWidget(self.name_input)
        layout.addWidget(make_label("Age: *", 13))
        layout.addWidget(self.age_input)

        # Timer
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setMinimumHeight(80)
        layout.addWidget(self.timer_label)

        # Timer instruction label
        self.instruction_label = make_label("Press a button below to start a timer.", 13, "#555")
        layout.addWidget(self.instruction_label)

        # Timer buttons
        self.btn_p1     = make_button("Start Initial Pulse (P1)", 350)
        self.btn_squats = make_button("Start Squats Counter", 350)
        self.btn_p2p3   = make_button("Start Final Recovery (P2/P3)", 350)
        for btn in [self.btn_p1, self.btn_squats, self.btn_p2p3]:
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        # P1 P2 P3 inputs
        res_row = QHBoxLayout()
        res_row.setAlignment(Qt.AlignCenter)
        self.p1_res = QLineEdit(); self.p1_res.setPlaceholderText("P1 *"); self.p1_res.setFixedWidth(100)
        self.p2_res = QLineEdit(); self.p2_res.setPlaceholderText("P2 *"); self.p2_res.setFixedWidth(100)
        self.p3_res = QLineEdit(); self.p3_res.setPlaceholderText("P3 *"); self.p3_res.setFixedWidth(100)
        for r in [self.p1_res, self.p2_res, self.p3_res]:
            res_row.addWidget(r)
        layout.addLayout(res_row)

        # Auto-focus chain
        self.age_input.returnPressed.connect(self.p1_res.setFocus)
        self.p1_res.returnPressed.connect(self.p2_res.setFocus)
        self.p2_res.returnPressed.connect(self.p3_res.setFocus)

        # Enable submit only when required fields filled
        for field in [self.age_input, self.p1_res, self.p2_res, self.p3_res]:
            field.textChanged.connect(self.check_fields)

        layout.addWidget(make_warning())

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(
            "color: #cc0000; font-size: 12px; font-weight: bold;"
            "background-color: #fff0f0; border: 1px solid #ffcccc;"
            "border-radius: 6px; padding: 12px;"
        )
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setMinimumHeight(100)
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)

        # Submit button
        self.submit_btn = make_button("Send Results", 200)
        self.submit_btn.setEnabled(False)
        self.submit_btn.clicked.connect(self.submit)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

        # Timer logic
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.time_left = 0
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.stop_flash)
        self.flash_count = 0

        self.btn_p1.clicked.connect(lambda: self.start_timer(15, "🫀 Lie still and measure your pulse for 15 seconds (P1)."))
        self.btn_squats.clicked.connect(lambda: self.start_timer(45, "🏋️ Perform 30 squats within 45 seconds!"))
        self.btn_p2p3.clicked.connect(lambda: self.start_timer(60, "🛌 Lie down. P2 = first 15s, P3 = last 15s of this minute."))

    def check_fields(self):
        filled = all([
            self.age_input.text().strip(),
            self.p1_res.text().strip(),
            self.p2_res.text().strip(),
            self.p3_res.text().strip(),
        ])
        self.submit_btn.setEnabled(filled)

    def start_timer(self, seconds, instruction):
        self.time_left = seconds
        self.instruction_label.setText(instruction)
        self.timer_label.setStyleSheet("color: #333;")
        self.timer.start(1000)
        self.refresh_display()

    def tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.refresh_display()
            self.timer_label.setStyleSheet(
                "color: #4CAF50;" if self.time_left <= 15 else "color: #333;"
            )
        else:
            self.timer.stop()
            self.on_timer_done()

    def on_timer_done(self):
        self.instruction_label.setText("✅ Timer done! Record your pulse value above.")
        self.start_flash()
        if SOUND_AVAILABLE:
            QSound.play("beep.wav")
        else:
            QApplication.beep()

    def start_flash(self):
        self.flash_count = 0
        self.flash_timer.start(300)

    def stop_flash(self):
        if self.flash_count < 6:
            color = "#ff0000" if self.flash_count % 2 == 0 else "#333"
            self.timer_label.setStyleSheet(f"color: {color};")
            self.flash_count += 1
        else:
            self.flash_timer.stop()
            self.timer_label.setStyleSheet("color: #4CAF50;")

    def refresh_display(self):
        t = QTime(0, 0).addSecs(self.time_left)
        self.timer_label.setText(t.toString("hh:mm:ss"))

    def submit(self):
        errors = []

        age_text = self.age_input.text().strip()
        if not age_text:
            errors.append("⚠️ Age is required.")
        else:
            try:
                age = int(age_text)
                if age < 1 or age > 120:
                    errors.append("⚠️ Age must be between 1 and 120.")
            except ValueError:
                errors.append("⚠️ Age must be a valid number.")

        pulse_fields = {"P1": self.p1_res, "P2": self.p2_res, "P3": self.p3_res}
        pulse_values = {}
        for name, field in pulse_fields.items():
            text = field.text().strip()
            if not text:
                errors.append(f"⚠️ {name} is required.")
            else:
                try:
                    val = int(text)
                    if val < 10 or val > 60:
                        errors.append(f"⚠️ {name} must be between 10 and 60 (15-second pulse count).")
                    else:
                        pulse_values[name] = val
                except ValueError:
                    errors.append(f"⚠️ {name} must be a valid number.")

        if errors:
            self.error_label.setText("\n".join(errors))
            self.error_label.setVisible(True)
            return

        self.error_label.setVisible(False)
        p1, p2, p3 = pulse_values["P1"], pulse_values["P2"], pulse_values["P3"]
        index = (4 * (p1 + p2 + p3) - 200) / 10
        self.on_submit(
            round(index, 1),
            self.name_input.text().strip(),
            age_text, p1, p2, p3
        )


# ─────────────────────────────────────────────
#  WINDOW 3 — Results
# ─────────────────────────────────────────────
class ResultsWindow(QWidget):
    def __init__(self, on_done, on_retake):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(16)

        layout.addWidget(make_progress_bar(3))
        layout.addWidget(make_title("Your Results", 22))

        # Name/age display
        self.meta_label = make_label("", 13, "#888")
        layout.addWidget(self.meta_label)

        # Index
        self.index_label = QLabel("Ruffier Index: —")
        self.index_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.index_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.index_label)

        # Performance
        self.performance_label = QLabel("Cardiac Performance: —")
        self.performance_label.setFont(QFont("Arial", 18))
        self.performance_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.performance_label)

        # Gauge bar
        self.gauge = QProgressBar()
        self.gauge.setMaximum(25)
        self.gauge.setValue(0)
        self.gauge.setFormat("")
        self.gauge.setFixedHeight(22)
        layout.addWidget(self.gauge)

        gauge_labels = QHBoxLayout()
        for lbl in ["0 Excellent", "6 Good", "10 Avg", "15 Below Avg", "16+ Poor"]:
            l = QLabel(lbl)
            l.setStyleSheet("font-size: 10px; color: #888;")
            gauge_labels.addWidget(l)
        layout.addLayout(gauge_labels)

        # Health advice
        self.advice_label = make_label("", 13, "#555")
        self.advice_label.setStyleSheet(
            "background-color: #f0fff0; border: 1px solid #c8e6c9;"
            "border-radius: 8px; padding: 10px; font-size: 13px; color: #2e7d32;"
        )
        self.advice_label.setMinimumHeight(70)
        layout.addWidget(self.advice_label)

        # History table
        layout.addWidget(make_label("── Past Results ──", 12, "#888"))
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(8)
        self.history_table.setHorizontalHeaderLabels(["Date", "Name", "Age", "P1", "P2", "P3", "Index", "Performance"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setFixedHeight(150)
        layout.addWidget(self.history_table)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        retake_btn = make_button("Retake Test", 160)
        retake_btn.setStyleSheet(
            "background-color: #1976D2; color: white; border-radius: 8px;"
            "padding: 12px 30px; font-weight: bold; font-size: 15px;"
        )
        retake_btn.clicked.connect(on_retake)
        done_btn = make_button("Done", 160)
        done_btn.clicked.connect(on_done)
        btn_row.addWidget(retake_btn)
        btn_row.addWidget(done_btn)
        layout.addLayout(btn_row)

    def set_results(self, index, name, age, p1, p2, p3):
        self.index_label.setText(f"Ruffier Index: {index}")

        if index <= 3:
            perf, color, advice = (
                "Excellent cardiac performance 💚", "#2e7d32",
                "Outstanding! Your heart is in excellent shape. Keep up your active lifestyle."
            )
        elif index <= 6:
            perf, color, advice = (
                "Good cardiac performance 🟢", "#4CAF50",
                "Great result! Your heart handles physical stress well. Regular exercise is paying off."
            )
        elif index <= 10:
            perf, color, advice = (
                "Average cardiac performance 🟡", "#f9a825",
                "Your heart is functioning normally. Consider adding more cardio to your routine."
            )
        elif index <= 15:
            perf, color, advice = (
                "Below average cardiac performance 🟠", "#e65100",
                "Your heart may need attention. Consult a doctor and consider a structured exercise plan."
            )
        else:
            perf, color, advice = (
                "Poor cardiac performance 🔴", "#b71c1c",
                "Please consult a physician. Avoid strenuous activity until you've been evaluated."
            )

        self.performance_label.setText(f"Cardiac Performance: {perf}")
        self.performance_label.setStyleSheet(f"color: {color}; font-size: 18px;")
        self.advice_label.setText(f"💡 {advice}")
        self.advice_label.setStyleSheet(
            f"background-color: #f9f9f9; border: 1px solid {color};"
            f"border-radius: 8px; padding: 10px; font-size: 13px; color: {color};"
        )

        # Gauge
        self.gauge.setValue(min(int(index) + 12, 25))
        self.gauge.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; border-radius: 6px; }}")

        # Meta
        display_name = name if name else "Anonymous"
        self.meta_label.setText(f"Name: {display_name}   |   Age: {age}")

        # Save & reload history
        save_to_csv(display_name, age, p1, p2, p3, index, perf)
        self.load_history_table()

    def load_history_table(self):
        history = load_history()
        self.history_table.setRowCount(len(history))
        for row, entry in enumerate(reversed(history)):
            for col, key in enumerate(["Date", "Name", "Age", "P1", "P2", "P3", "Index", "Performance"]):
                self.history_table.setItem(row, col, QTableWidgetItem(entry.get(key, "")))


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
app = QApplication(sys.argv)
app.setStyleSheet(APP_STYLE)

stack = QStackedWidget()
stack.setWindowTitle("Health Status Detection Program")
stack.setMinimumSize(750, 900)

def go_to_results(index, name, age, p1, p2, p3):
    results.set_results(index, name, age, p1, p2, p3)
    stack.setCurrentIndex(2)

intro   = IntroWindow(on_start=lambda: stack.setCurrentIndex(1))
test    = TestWindow(on_submit=go_to_results, on_back=lambda: stack.setCurrentIndex(0))
results = ResultsWindow(on_done=lambda: stack.setCurrentIndex(0), on_retake=lambda: stack.setCurrentIndex(1))

stack.addWidget(intro)
stack.addWidget(test)
stack.addWidget(results)

stack.show()
sys.exit(app.exec_())