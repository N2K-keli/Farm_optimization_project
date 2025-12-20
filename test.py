from PySide6.QtWidgets import QApplication, QLabel
import sys 
app = QApplication(sys.argv)
label = QLabel("Farm optimization application")
label.show()
sys.exit(app.exec())
