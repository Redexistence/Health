from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

ruffier_index = (4*(p1+p2+p3)-200)/10

# Define cardiac performance thresholds by age group
# Format: (min_age, thresholds tuple - Low, Satisfactory, Average, Above Average, High)
age_thresholds = {
    15: (15, 11, 6, 0.5, 0),      # Age 15+
    13: (16.5, 12.5, 7.5, 2, 0),  # Age 13-14
    11: (18, 14, 9, 3.5, 0),      # Age 11-12
    9: (19.5, 15.5, 10.5, 5, 0),  # Age 9-10
    7: (21, 17, 12, 6.5, 0),      # Age 7-8
}
performance_labels = ["Low", "Satisfactory", "Average", "Above Average", "High"]

# Determine cardiac performance based on age
def get_cardiac_performance(age, ruffier_index):
    for min_age in sorted(age_thresholds.keys(), reverse=True):
        if age >= min_age:
            thresholds = age_thresholds[min_age]
            if ruffier_index >= thresholds[0]:
                return performance_labels[0]
            elif ruffier_index >= thresholds[1]:
                return performance_labels[1]
            elif ruffier_index >= thresholds[2]:
                return performance_labels[2]
            elif ruffier_index >= thresholds[3]:
                return performance_labels[3]
            else:
                return performance_labels[4]
    return "Unknown"

cardiac_performance = get_cardiac_performance(age, ruffier_index)


# Create the application and window
app = QApplication([])
window = QWidget()
window.setWindowTitle("Custom Text Window")
window.resize(900, 800)
window.setStyleSheet("background-color: white;")

# Configure fonts
top_font = QFont("Arial", 24, QFont.Bold)
bottom_font = QFont("Arial", 18)

# Create labels for custom text
top_label = QLabel(f"Your Ruffier Index: {ruffier_index}")  # Replace with your top text
top_label.setFont(top_font)
top_label.setStyleSheet("color: black;")
top_label.setAlignment(Qt.AlignCenter)

bottom_label = QLabel(f"Cardiac Performance: {cardiac_performance}")  # Replace with your bottom text
bottom_label.setFont(bottom_font)
bottom_label.setStyleSheet("color: black;")
bottom_label.setAlignment(Qt.AlignCenter)

# Create Done button
done_button = QPushButton("Done")
done_button.setFont(QFont("Arial", 14))
done_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;")
done_button.clicked.connect(window.close)

# Set up the layout
layout = QVBoxLayout()
layout.addWidget(top_label)
layout.addWidget(bottom_label)
layout.addWidget(done_button, alignment=Qt.AlignCenter)
window.setLayout(layout)

# Show the window and run the application
window.show()
app.exec_()