import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog,
    QLabel, QTabWidget, QVBoxLayout, QWidget, QTextEdit, QPushButton, QHBoxLayout, QLineEdit, QSpinBox
)
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import Qt


class ImageDisplayTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()


class NotepadTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()

        self.open_button = QPushButton("Otwórz")
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Otwórz plik tekstowy", "", "Pliki tekstowe (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setText(content)

    def save_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Zapisz plik tekstowy", "", "Pliki tekstowe (*.txt)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.text_edit.toPlainText()
                file.write(content)

    def clear_text(self):
        self.text_edit.clear()


class ConcatenationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Wpisz tekst dla pola A")
        self.layout.addWidget(self._create_labeled_widget("Pole A:", self.input_a))

        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Wpisz tekst dla pola B")
        self.layout.addWidget(self._create_labeled_widget("Pole B:", self.input_b))

        self.input_c = QSpinBox()
        self.input_c.setRange(0, 1000)
        self.layout.addWidget(self._create_labeled_widget("Pole C (liczba):", self.input_c))

        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)
        self.layout.addWidget(self._create_labeled_widget("Pole A + B + C:", self.result_field))

        self.input_a.textChanged.connect(self.update_result)
        self.input_b.textChanged.connect(self.update_result)
        self.input_c.valueChanged.connect(self.update_result)

        self.setLayout(self.layout)

    def _create_labeled_widget(self, label_text, widget):
        container = QWidget()
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        container.setLayout(layout)
        return container

    def update_result(self):
        text_a = self.input_a.text()
        text_b = self.input_b.text()
        text_c = str(self.input_c.value())
        concatenated_result = text_a + text_b + text_c
        self.result_field.setText(concatenated_result)

    def clear_fields(self):
        self.input_a.clear()
        self.input_b.clear()
        self.input_c.setValue(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja z Zakładkami")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.image_tab = ImageDisplayTab()
        self.tabs.addTab(self.image_tab, "Wyświetl obraz")

        self.notepad_tab = NotepadTab()
        self.tabs.addTab(self.notepad_tab, "Notatnik")

        self.concatenate_tab = ConcatenationTab()
        self.tabs.addTab(self.concatenate_tab, "Sklejanie pól")

        self.menu = self.menuBar()
        self.create_menus()

    def create_menus(self):
        file_menu = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        task1_menu = self.menu.addMenu("Task 1")
        open_image_action = QAction("Open", self)
        open_image_action.setShortcut("Ctrl+O")
        open_image_action.triggered.connect(self.open_image_file)
        task1_menu.addAction(open_image_action)

        task2_menu = self.menu.addMenu("Task 2")
        open_notepad_action = QAction("Open", self)
        open_notepad_action.setShortcut("Ctrl+Shift+O")
        open_notepad_action.triggered.connect(self.notepad_tab.open_file)
        task2_menu.addAction(open_notepad_action)

        save_notepad_action = QAction("Save", self)
        save_notepad_action.setShortcut("Ctrl+S")
        save_notepad_action.triggered.connect(self.notepad_tab.save_file)
        task2_menu.addAction(save_notepad_action)

        save_as_notepad_action = QAction("Save as", self)
        save_as_notepad_action.setShortcut("Ctrl+Shift+S")
        save_as_notepad_action.triggered.connect(self.notepad_tab.save_file)
        task2_menu.addAction(save_as_notepad_action)

        clear_notepad_action = QAction("Clear", self)
        clear_notepad_action.setShortcut("Ctrl+Shift+C")
        clear_notepad_action.triggered.connect(self.notepad_tab.clear_text)
        task2_menu.addAction(clear_notepad_action)

        task3_menu = self.menu.addMenu("Task 3")
        clear_fields_action = QAction("Clear", self)
        clear_fields_action.setShortcut("Ctrl+Shift+K")
        clear_fields_action.triggered.connect(self.concatenate_tab.clear_fields)
        task3_menu.addAction(clear_fields_action)

    def open_image_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Wybierz plik obrazu", "",
            "Obrazy (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.image_tab.display_image(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
