import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,\
      QComboBox, QFormLayout, QDialog, QLabel, QScrollArea, QHBoxLayout, QPushButton,QLineEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        print("Load Initiated")
        file_path = "Main_operating_variables.csv"
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
        dialog.setWindowTitle("Combo Boxes for CSV Data")
        dialog.exec_()


class ComboBoxDialog(QDialog):
    def __init__(self, headers, data): # Need to use the headers for the top of the columns
        super().__init__()

        layout = QVBoxLayout()

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.adjustSize()

        self.export_button = QPushButton("Export File",self)
        self.export_button.adjustSize()

        layout.addWidget(self.save_button)
        layout.addWidget(self.export_button)

        self.save_button.clicked.connect(self.save_button_handler)
        self.export_button.clicked.connect(self.export_button_handler)

        self.setLayout(layout)

        self.scroll_area = QScrollArea()
        layout.addWidget(self.scroll_area)

        self.form_layout = QFormLayout()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(QWidget())  # Initialize the scroll area's widget

        header_row = QHBoxLayout()
        for header in headers:
            header_label = QLabel(header,self)
            header_row.addWidget(header_label)
        self.form_layout.addRow(header_row)

        # Create a list of combo boxes for each cell in the CSV file
        self.combo_boxes = []
        self.text_entries = []
        self.currentVal = []

        self.populateComboBoxes(data)

        container_widget = QWidget()
        container_widget.setLayout(self.form_layout)
        self.scroll_area.setWidget(container_widget)


    def populateComboBoxes(self, data):
        for row in data:
            row_layout = QHBoxLayout()
            for col, value in enumerate(row):
                combo_box = QComboBox(self)
                # text_entry = QLineEdit(self)
                self.combo_boxes.append(combo_box)
                combo_box.addItems(set(data[i][col] for i in range(len(data))))
                combo_box.setCurrentText(value)
                # self.currentVal.append(self.combo_box.currentText())
                row_layout.addWidget(combo_box)
            self.form_layout.addRow(row_layout)


    def save_button_handler(self):
        print("SAVING CURRENT EDITS")

        self.currentVal = []

        for combo_box in self.combo_boxes:
            currText = combo_box.currentText()
            self.currentVal.append(currText)
        print("Current Values:", self.currentVal)

    def export_button_handler(self):
        print("EXPORTING FILE")
        file_path = "exported_data.csv"  # Specify the desired file path for the exported CSV file
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Write the headers
            csv_writer.writerow(["Group Name", "Unique Name", "Display Name", "Type", "Value", "Tags"])

            # Write the current values
            for i in range(0, len(self.currentVal), 6):
                row = self.currentVal[i:i + 6]  # 6 columns for each of the rows and their headers
                csv_writer.writerow(row)

        print("Data has been exported to", file_path)





def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
