from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
top_label = QLabel("Your Rufier Index: ")  # Replace with your top text
top_label.setFont(top_font)
top_label.setStyleSheet("color: black;")
top_label.setAlignment(Qt.AlignCenter)

bottom_label = QLabel("Cardiac Performance:")  # Replace with your bottom text
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