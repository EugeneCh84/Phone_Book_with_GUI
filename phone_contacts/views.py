
"""This module provides views to manage the contacts table."""

from .model import ContactsModel
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QFileDialog,
    QTableWidget
    
)

        


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Phone_contacts")
        self.resize(800, 600)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()
        

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        
        self.table.setModel(self.contactsModel.model)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.resizeColumnsToContents()
        self.filtermodel = QSortFilterProxyModel()
        self.filtermodel.setSourceModel(self.contactsModel.model)
        self.filtermodel.setFilterKeyColumn(0)
        
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts)
        self.search_field= QLineEdit()
        self.search_field.textChanged.connect(self.contactsModel.proxy.setFilterRegularExpression)
        self.filter_label = QLabel('Search/Filter Mask')
        self.filter_option = QComboBox()
        self.filter_option.addItems(['ID', 'Name', 'Phone', 'Email'])
        self.filter_option.currentIndexChanged.connect(self.contactsModel.proxy.setFilterKeyColumn)
        self.buttonOpen = QPushButton('Open')
        self.buttonSave = QPushButton('Save')
        self.buttonOpen.clicked.connect(self.contactsModel.handleOpen)
        self.buttonSave.clicked.connect(self.contactsModel.handleSave)
        
        


        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.buttonSave)
        layout.addWidget(self.buttonOpen)
        layout.addStretch()
        layout.addWidget(self.filter_label)
        layout.addWidget(self.filter_option)
        layout.addWidget(self.search_field)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        #search_layout = QHBoxLayout()
        #search_layout.addWidget(self.sear_field)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)
        #layout.addLayout(search_layout)


                 


    def openAddDialog(self):
        """Open the Add Contact dialog."""
        dialog = AddDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            print('True')
            self.table.resizeColumnsToContents()
        

    def deleteContact(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            
            self.contactsModel.deleteContact(row)
        


    def clearContacts(self):
        """Remove all contacts from the database."""
        messageBox = QMessageBox.warning(
        self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if messageBox == QMessageBox.StandardButton.Ok:
            self.contactsModel.clearContacts()



    



class AddDialog(QDialog):
    """Add Contact dialog."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Add Contact dialog's GUI."""
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Phone:", self.phoneField)
        layout.addRow("Email:", self.emailField)
        #layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)
    
    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.nameField, self.phoneField, self.emailField):
           if not field.text():
               QMessageBox.critical(
                   self,
                   "Error!",
                   f"You must provide a contact's {field.objectName()}",
               )
               self.data = None  # Reset .data
               return

        self.data.append(field.text())
            
        if not self.data:
           return
        print(self.data)
        super().accept()