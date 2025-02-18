import sys
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox

class GHDLInstallerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select the GHDL version to install:", self)
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(["3.0.0", "4.0.0", "4.1.0", "nightly"])
        layout.addWidget(self.versionCombo)
        
        self.installButton = QPushButton("Install GHDL", self)
        self.installButton.clicked.connect(self.runInstaller)
        layout.addWidget(self.installButton)
        
        self.setLayout(layout)
        self.setWindowTitle("GHDL Installer")
        self.setGeometry(100, 100, 300, 150)
    
    def runInstaller(self):
        selected_version = self.versionCombo.currentText()
        print(f"Selected Version: {selected_version}")  # Debugging output

        try:
            result = subprocess.run(["bash", "./nghdl/update-ghdl-with-dependency.sh", selected_version], text=True)
            print("Script Output:", result.stdout)  # Debugging output
            QMessageBox.information(self, "Success", f"GHDL {selected_version} installation started.")
        except subprocess.CalledProcessError as e:
            print("Error Output:", e.stderr)  # Debugging output
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class KiCadInstallerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select the KiCad version to install:", self)
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(["7.0.11", "8.0.8"])
        layout.addWidget(self.versionCombo)
        
        self.updateButton = QPushButton("Update KiCad", self)
        self.updateButton.clicked.connect(self.runUpdate)
        layout.addWidget(self.updateButton)
        
        self.setLayout(layout)
        self.setWindowTitle("KiCad Update Manager")
        self.setGeometry(100, 100, 300, 150)
    
    def runUpdate(self):
        selected_version = self.versionCombo.currentText()
        
        try:
            subprocess.run(["bash", "./update-kicad-final.sh", selected_version], check=True, input=f"{selected_version}\n", text=True)
            QMessageBox.information(self, "Success", f"KiCad {selected_version} installation started.")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", "Failed to execute the update script.")

class NGSpiceInstallerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select the NGSPICE version to install:", self)
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(["38", "40", "43"])
        layout.addWidget(self.versionCombo)
        
        self.installButton = QPushButton("Install NGSPICE", self)
        self.installButton.clicked.connect(self.runInstaller)
        layout.addWidget(self.installButton)
        
        self.setLayout(layout)
        self.setWindowTitle("NGSPICE Installer")
        self.setGeometry(100, 100, 300, 150)
    
    def runInstaller(self):
        selected_version = self.versionCombo.currentText()
        print(f"Selected Version: {selected_version}")  # Debugging output

        try:
            result = subprocess.run(["bash", "./nghdl/update-ngspice-final.sh", selected_version], text=True)
            print("Script Output:", result.stdout)  # Debugging output
            QMessageBox.information(self, "Success", f"NGSPICE {selected_version} installation started.")
        except subprocess.CalledProcessError as e:
            print("Error Output:", e.stderr)  # Debugging output
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class VerilatorInstallerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select the Verilator version to install:", self)
        layout.addWidget(self.label)
        
        self.versionCombo = QComboBox(self)
        self.versionCombo.addItems(["4.228", "5.020", "5.026", "5.030"])
        layout.addWidget(self.versionCombo)
        
        self.installButton = QPushButton("Install Verilator", self)
        self.installButton.clicked.connect(self.runInstaller)
        layout.addWidget(self.installButton)
        
        self.setLayout(layout)
        self.setWindowTitle("Verilator Installer")
        self.setGeometry(100, 100, 300, 150)
    
    def runInstaller(self):
        selected_version = self.versionCombo.currentText()
        print(f"Selected Version: {selected_version}")  # Debugging output

        try:
            result = subprocess.run(["./nghdl/update-verilator-final.sh", selected_version], text=True)
            print("Script Output:", result.stdout)  # Debugging output
            QMessageBox.information(self, "Success", f"Verilator {selected_version} installation started.")
        except subprocess.CalledProcessError as e:
            print("Error Output:", e.stderr)  # Debugging output
            QMessageBox.critical(self, "Error", "Failed to execute the installation script.")

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.files = {
            "Check Packages": "./check-packages-final.sh",
            "Update Dependencies": "./update-dependency-final.sh",
        }
        self.package_versions = self.load_versions()
        self.initUI()
    
    def load_versions(self):
        try:
            with open("information.json", "r") as file:
                data = json.load(file)
                versions = {pkg["package_name"]: pkg["version"] for pkg in data["important_packages"]}
                return versions
        except Exception as e:
            print(f"Error loading versions: {e}")
            return {}
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.version_label = QLabel(self.get_version_text(), self)
        layout.addWidget(self.version_label)

        self.setLayout(layout)
        self.setWindowTitle("Update Manager")
        self.setGeometry(100, 100, 400, 300)

        self.download_button = QPushButton("Download Packages", self)
        self.download_button.clicked.connect(self.runDownloadPackages)
        layout.addWidget(self.download_button)

        self.kicad_button = QPushButton("Open KiCad Installer", self)
        self.kicad_button.clicked.connect(self.openKiCad)
        layout.addWidget(self.kicad_button)

        self.ghdl_button = QPushButton("Open GHDL Installer", self)
        self.ghdl_button.clicked.connect(self.openGHDL)
        layout.addWidget(self.ghdl_button)

        self.verilator_button = QPushButton("Open Verilator Installer", self)
        self.verilator_button.clicked.connect(self.openVerilator)
        layout.addWidget(self.verilator_button)

        self.ngspice_button = QPushButton("Open NGSPICE Installer", self)
        self.ngspice_button.clicked.connect(self.openNGSpice)
        layout.addWidget(self.ngspice_button)
        
        for title, script in self.files.items():
            button = QPushButton(title, self)
            button.clicked.connect(lambda checked, s=script: self.runUpdate(s))
            layout.addWidget(button)
        
        self.remove_button = QPushButton("Remove Packages", self)
        self.remove_button.clicked.connect(self.runRemovePackages)
        layout.addWidget(self.remove_button)
        
        self.setLayout(layout)
    
    def get_version_text(self):
        return f"KiCad: {self.package_versions.get('kicad', 'Unknown')}\n" \
               f"NGSPICE: {self.package_versions.get('ngspice', 'Unknown')}\n" \
               f"GHDL: {self.package_versions.get('ghdl', 'Unknown')}\n" \
               f"Verilator: {self.package_versions.get('verilator', 'Unknown')}"
    
    def runUpdate(self, script):
        subprocess.run(["bash", script], check=True)
    
    def runDownloadPackages(self):
        subprocess.run(["bash", "./nghdl/download_packages.sh", "download"], check=True)
    
    def runRemovePackages(self):
        subprocess.run(["bash", "./nghdl/download_packages.sh", "remove"], check=True)
    
    def openGHDL(self):
        self.ghdl_window = GHDLInstallerGUI()
        self.ghdl_window.show()
    
    def openKiCad(self):
        self.kicad_window = KiCadInstallerGUI()
        self.kicad_window.show()
    
    def openNGSpice(self):
        self.ngspice_window = NGSpiceInstallerGUI()
        self.ngspice_window.show()
    
    def openVerilator(self):
        self.verilator_window = VerilatorInstallerGUI()
        self.verilator_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainGUI()
    main_window.show()
    sys.exit(app.exec_())
