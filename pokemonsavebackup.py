from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
                             QVBoxLayout, QFileDialog, QListWidget, 
                             QListWidgetItem, QLineEdit, QCheckBox, QMessageBox)
import sys
import os
import json
import re
import bcrypt
import zipfile
from datetime import datetime

SETTINGS_FILE = 'settings.json'
CREDENTIALS_FILE = 'credentials.json'

class PokemonSaveBackup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()
    
    def initUI(self):
        self.setWindowTitle('Pokémon Center Save Backup')
        self.setGeometry(100, 100, 500, 400)
        
        self.layout = QVBoxLayout()
        
        self.folder_label = QLabel('Select Folder to Scan for Pokémon Saves:')
        self.layout.addWidget(self.folder_label)
        
        self.selected_folder_label = QLabel('No folder selected')
        self.layout.addWidget(self.selected_folder_label)
        
        self.select_folder_btn = QPushButton('Choose Folder')
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_btn)
        
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)
        
        self.select_file_btn = QPushButton('Select Individual File')
        self.select_file_btn.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_btn)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter Username')
        self.layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)
        
        self.backup_btn = QPushButton('Backup Selected Saves')
        self.backup_btn.clicked.connect(self.backup_saves)
        self.layout.addWidget(self.backup_btn)
        
        self.export_zip_btn = QPushButton('Export as ZIP')
        self.export_zip_btn.clicked.connect(self.export_as_zip)
        self.layout.addWidget(self.export_zip_btn)
        
        self.setLayout(self.layout)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.selected_folder_label.setText(folder)
            self.scan_for_saves(folder)
            self.save_settings(folder)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Pokémon Save File', '', 'Save Files (*.sav *.dsv *.gci *.dat)')
        if file_path:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setCheckState(False)
            self.file_list.addItem(item)
    
    def scan_for_saves(self, folder):
        self.file_list.clear()
        extensions = ['.sav', '.dsv', '.gci', '.dat']  # Common Pokémon save file extensions
        for root, _, files in os.walk(folder):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions) and re.search(r'pok[eé]mon', file, re.IGNORECASE):
                    item = QListWidgetItem(file)
                    item.setCheckState(False)
                    self.file_list.addItem(item)
        
        if self.file_list.count() == 0:
            QMessageBox.warning(self, 'No Pokémon Saves Found', 'No Pokémon save files were automatically detected. You can select an individual file manually.')
    
    def backup_saves(self):
        selected_saves = [self.file_list.item(i).text() for i in range(self.file_list.count())
                          if self.file_list.item(i).checkState()]
        if not selected_saves:
            QMessageBox.warning(self, 'No Files Selected', 'Please select at least one save file to back up.')
            return
        
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'Missing Credentials', 'Please enter a username and password.')
            return
        
        QMessageBox.information(self, 'Backup Started', f'Backing up {len(selected_saves)} files...')
        # TODO: Implement GitHub upload logic
    
    def export_as_zip(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, 'Missing Username', 'Please enter a username before exporting.')
            return
        
        date_str = datetime.now().strftime('%m-%d-%y')
        zip_filename = f"{username}-backup{date_str}.zip"
        
        selected_saves = [self.file_list.item(i).text() for i in range(self.file_list.count())
                          if self.file_list.item(i).checkState()]
        if not selected_saves:
            QMessageBox.warning(self, 'No Files Selected', 'Please select at least one save file to export.')
            return
        
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder to Save ZIP')
        if not folder:
            return
        
        zip_path = os.path.join(folder, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in selected_saves:
                file_path = os.path.join(self.selected_folder_label.text(), file)
                zipf.write(file_path, os.path.basename(file_path))
        
        QMessageBox.information(self, 'Export Complete', f'Saves exported to {zip_path}')
    
    def save_settings(self, folder):
        settings = {'last_folder': folder}
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                last_folder = settings.get('last_folder', '')
                if last_folder:
                    self.selected_folder_label.setText(last_folder)
                    self.scan_for_saves(last_folder)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PokemonSaveBackup()
    window.show()
    sys.exit(app.exec_())
