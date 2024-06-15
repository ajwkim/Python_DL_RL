# # creating_a_window_3.py

# from PyQt6.QtWidgets import QApplication, QMainWindow
# import sys


# app = QApplication(sys.argv)        # 앱 당 하나의 QApplication 인스턴스

# window = QMainWindow()                  # 윈도우
# window.show()

# app.exec()                          # 이벤트 루프
#                                     # 이벤트 루프 종료해야 여기 도달


# # creating_a_window_end.py

# import sys

# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PyQt6.QtCore import QSize, Qt

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         self.setWindowTitle('My App')
#         self.setFixedSize(QSize(400, 300))      # QSize(가로, 세로)
#                                                 # set Fixed/Minimum/Maximum Size()
#         button = QPushButton('Press Me')
#         self.setCentralWidget(button)


# app = QApplication([])      # sys.argv
# window = MainWindow()
# window.show()
# app.exec()


# # signals_and_slots1.py

# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')

#         self.button_checked = False
#         self.button = QPushButton('Press Me')
#         self.button.setCheckable(True)
#         # self.button.clicked.connect(self.button_toggled)
#         self.button.released.connect(self.button_released)
#         self.button.setChecked(self.button_checked)

#         self.setCentralWidget(self.button)

#     # def button_toggled(self, checked):
#     #     self.button_checked = checked
#     #     print('Checked :', checked)

#     def button_released(self):
#         self.button_checked = self.button.isChecked()
#         print(self.button_checked)


# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()


# # signals_and_slots2.py

# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')

#         self.button = QPushButton('Press Me')                   # QPushButton('button_text')
#         self.button.clicked.connect(self.button_clicked)

#         self.setCentralWidget(self.button)

#     def button_clicked(self):
#         self.button.setText('You clicked me.')
#         self.button.setEnabled(False)

#         self.setWindowTitle('My Clicked App')


# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()


# # signals_and_slot3.py

# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
# import random, sys

# titles = ['My App', 'My App', 'Still My App', 'Still My App', 'What on Earth', 'What on Earth',
#           'This is surprising', 'This is surprising', 'Something went wrong']

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')
        
#         self.times_clicked = 0
#         self.button = QPushButton('Press Me')
#         self.button.clicked.connect(self.button_clicked)
#         self.windowTitleChanged.connect(self.window_title_changed)

#         self.setCentralWidget(self.button)

#     def button_clicked(self):
#         print('Clicked')
#         title = random.choice(titles)
#         print('Setting title:', title)
#         self.setWindowTitle(title)

#     def window_title_changed(self, title):
#         print('Window title changed:', title)
#         if title == 'Something went wrong':
#             # self.button.setDisabled(True)
#             self.button.setEnabled(False)


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()


# # signals_and_slots4.py

# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')

#         self.input = QLineEdit()                                    # .textChanged.connect()
#         self.label = QLabel('initial')                                       # .setText('~')
#         self.input.textChanged.connect(self.label.setText)

#         layout = QVBoxLayout()
#         layout.addWidget(self.input)
#         layout.addWidget(self.label)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()


# import sys
# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')

#         lbl = QLabel('Hello')
#         font = lbl.font()
#         font.setPointSize(30)
#         lbl.setFont(font)
#         lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

#         self.setCentralWidget(lbl)


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()


# import sys
# from PyQt6.QtGui import QPixmap
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('My App')

#         lbl = QLabel('Hello')                   # .setText('~')
#         lbl.setPixmap(QPixmap('otje.jpg'))
#         lbl.setScaledContents(True)                 # .setScaledContents(False)

#         self.setCentralWidget(lbl)


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QVBoxLayout, QDialogButtonBox, QMessageBox

class MyDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle('Hello')
		
		btns = (QDialogButtonBox.StandardButton.Ok |
				QDialogButtonBox.StandardButton.Cancel)
		self.buttonBox = QDialogButtonBox(btns)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		
		self.layout = QVBoxLayout()
		message = QLabel('Something happened, is that OK?')
		self.layout.addWidget(message)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('My App')
		
		btn = QPushButton('Press for a dialog')
		btn.clicked.connect(self.button_clicked)
		self.setCentralWidget(btn)

	def button_clicked(self, s):
		button = QMessageBox.critical(
			self, 'Oh dear!', 'Something went very wrong',
			buttons=QMessageBox.StandardButton.Discard |
				QMessageBox.StandardButton.NoToAll |
				QMessageBox.StandardButton.Ignore,
			defaultButton=QMessageBox.StandardButton.Discard)
		if button == QMessageBox.StandardButton.Discard:
			print('Discard')
		elif button == QMessageBox.StandardButton.NoToAll:
			print('No to all')
		else:
			print('Ignore')


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
