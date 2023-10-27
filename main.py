import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
    QComboBox, QFormLayout, QDialog, QLabel, QScrollArea, QHBoxLayout, QPushButton, QLineEdit, \
    QAbstractItemView, QHeaderView, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Create a QMainWindow subclass to represent the main application window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Load CSV File")

        # Create a central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a QLineEdit widget for entering the file path
        self.input = QLineEdit(self)
        layout.addWidget(self.input)

        # Create a "Browse File" button and connect it to the load_button_handler method
        self.load_button = QPushButton("Browse File", self)
        self.load_button.clicked.connect(self.load_button_handler)
        layout.addWidget(self.load_button)

        # Set the layout for the central widget
        self.central_widget.setLayout(layout)

        # Initialize an empty data attribute
        self.data = []

    def load_button_handler(self):
        print("Load Initiated")
        
        # Open a file dialog to select a CSV file
        file_path, _ = QFileDialog.getOpenFileName()
        
        if file_path:
            # Read the CSV file and its headers
            self.data, headers = self.read_csv_file(file_path)
            
            if self.data:
                # Open a custom dialog to customize the CSV data
                self.open_combo_box_dialog(headers)

    def read_csv_file(self, file_path):
        data = []
        headers = []
        try:
            with open(file_path, 'r') as infile:
                # Use the csv module to read the CSV file
                csv_reader = csv.reader(infile, delimiter=",")
                headers = next(csv_reader)  # Get column headers
                data = list(csv_reader)
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
        return data, headers

    def open_combo_box_dialog(self, headers):
        dialog = ComboBoxDialog(headers, self.data)
        dialog.setWindowTitle("Customize CSV Data")
        dialog.exec_()

# Create a custom QDialog subclass for customizing the CSV data
class ComboBoxDialog(QDialog):
    def __init__(self, headers, data):
        super().__init__()

        layout = QVBoxLayout()

        # Create "Save Changes" and "Export File" buttons
        self.save_button = QPushButton("Save Changes", self)
        self.save_button.adjustSize()
        self.export_button = QPushButton("Export File", self)
        self.export_button.adjustSize()
        
        # Connect button clicks to corresponding methods
        self.save_button.clicked.connect(self.save_button_handler)
        self.export_button.clicked.connect(self.export_button_handler)

        # Add buttons to the layout
        layout.addWidget(self.save_button)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

        # Create a scroll area to display the CSV data
        self.scroll_area = QScrollArea()
        layout.addWidget(self.scroll_area)

        # Create a form layout for arranging widgets
        self.form_layout = QFormLayout()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(QWidget())  # Initialize the scroll area's widget
        
        self.combo_boxes = []
        self.text_entries = []
        self.currentVal = []
        self.headers = headers

        # Add labels for column headers
        header_row = QHBoxLayout()
        for header in headers:
            header_label = QLabel(header, self)  # Create a label for each column header
            header_row.addWidget(header_label)

        # Add the header row to the form layout
        self.form_layout.addRow(header_row)

        # Populate the dialog with combo boxes and text entry fields
        self.populateComboBoxes(data)

        container_widget = QWidget()
        container_widget.setLayout(self.form_layout)
        self.scroll_area.setWidget(container_widget)

    # Populate the dialog with combo boxes and text entry fields
    def populateComboBoxes(self, data):
        for row in data:
            row_layout = QHBoxLayout()
            for col, value in enumerate(row):
                if col in [1, 2, 4, 5]:  # Check if the column index should be a text entry
                    text_entry = QLineEdit(self)
                    text_entry.setText(value)
                    text_entry.adjustSize()
                    text_entry.setStyleSheet('background-color:yellow;')
                    self.combo_boxes.append(text_entry)
                    row_layout.addWidget(text_entry)
                else:
                    combo_box = QComboBox(self)
                    combo_box.setStyleSheet('background-color:aqua;')
                    combo_box.addItems(set(data[i][col] for i in range(len(data))))
                    combo_box.setCurrentText(value)
                    self.combo_boxes.append(combo_box)
                    row_layout.addWidget(combo_box)
            self.form_layout.addRow(row_layout)

    # Handle the "Save Changes" button click
    def save_button_handler(self):
        print("SAVING CURRENT EDITS")
        self.currentVal = []
        for combo_box in self.combo_boxes:
            try:
                currText = combo_box.currentText()
            except AttributeError:
                currText = combo_box.text()
            self.currentVal.append(currText)
        print("Current Values:", self.currentVal)

    def export_button_handler(self):
        print("EXPORTING FILE")
        
        # Specify the desired file path for the exported CSV file
        file_path = "exported_data.csv"
        
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Write the headers
            csv_writer.writerow(self.headers)

            # Write the current values
            for i in range(0, len(self.currentVal), 6):
                row = self.currentVal[i:i + 6]  # 6 columns for each of the rows and their headers
                csv_writer.writerow(row)

        print("Data has been exported to", file_path)

# Define the main function to run the application
def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.resize(400, 100)
    window.show()
    sys.exit(app.exec_())

# Entry point of the script
if __name__ == "__main__":
    main()
