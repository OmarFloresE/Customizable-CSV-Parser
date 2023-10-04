import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QComboBox, QFormLayout, QDialog, QHBoxLayout, QLabel, QScrollArea


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load CSV File")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input = QLineEdit(self)
        layout.addWidget(self.input)

        self.load_button = QPushButton("Browse File", self)
        self.load_button.clicked.connect(self.load_button_handler)
        layout.addWidget(self.load_button)

        self.central_widget.setLayout(layout)

        # Initialize data attribute
        self.data = []

    def load_button_handler(self):
        print("Load Initiated")
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.data, headers = self.read_csv_file(file_path)
            if self.data:
                self.open_combo_box_dialog(headers)

    def read_csv_file(self, file_path):
        data = []
        headers = []
        try:
            with open(file_path, 'r') as infile:
                csv_reader = csv.reader(infile, delimiter=",")
                headers = next(csv_reader)  # Get column headers
                data = list(csv_reader)
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
        return data, headers

    def open_combo_box_dialog(self, headers):
        dialog = ComboBoxDialog(headers, self.data)
        dialog.exec_()


class ComboBoxDialog(QDialog):
    def __init__(self, headers, data):
        super().__init__()

        self.setWindowTitle("Combo Boxes for CSV Data")

        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()

        form_layout = QFormLayout()

        # Add labels for column headers
        header_row = QHBoxLayout()
        for header in headers:
            header_label = QLabel(header, self)  # Create a label for each column header
            header_row.addWidget(header_label)
        # print(header_row)
        form_layout.addRow(header_row)  # Add the header row to the form layout

        for row in data:
            row_layout = QHBoxLayout()
            for value in row:
                combo_box = QComboBox(self)  # Create a combo box for each value in the row
                # Populate the combo box with unique values from the entire row
                combo_box.addItems(set(row))                                           # We have to fix this! It is being populated by the wrong variables. Row instead of Col.
                combo_box.setCurrentText(value)  # Set the initial value of the combo box
                row_layout.addWidget(combo_box)  # Add the combo box to the row layout
            form_layout.addRow(row_layout)  # Add the row layout to the form layout

        container_widget = QWidget()
        container_widget.setLayout(form_layout)

        # Set up a scrollable area to accommodate the form layout
                                                                                                # WE HAVE TO FIX THE SCROLL CHANGING THE COMBO BOXES
        self.scroll_area.setWidget(container_widget)
        layout.addWidget(self.scroll_area)

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.adjustSize()
        layout.addWidget(self.save_button)

        self.export_button = QPushButton("Export File", self)
        self.export_button.adjustSize()
        layout.addWidget(self.export_button)

        # self.save_button.clicked.connect(self.save_button_handler)
        # self.export_button.clicked.connect(self.export_button_handler)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.resize(400, 100)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
