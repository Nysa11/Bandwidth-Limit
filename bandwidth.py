import paramiko
import sys
import json
from PyQt5 import QtWidgets

# File to store router data
ROUTERS_FILE = "routers.json"

# List to store router details (Loaded from file)
routers_list = []

# Load routers from JSON file
def load_routers():
    global routers_list
    try:
        with open(ROUTERS_FILE, 'r') as file:
            routers_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        routers_list = []

# Save routers to JSON file
def save_routers():
    with open(ROUTERS_FILE, 'w') as file:
        json.dump(routers_list, file, indent=4)

# Function to check if a queue exists and update bandwidth limits
def edit_bandwidth_limit(ip, username, password, port, download_limit, upload_limit):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the router
        ssh.connect(ip, username=username, password=password, port=int(port))

        # Check if a simple queue named 'bandwidth-limit' exists
        check_queue_command = "/queue simple print where name=bandwidth-limit"
        stdin, stdout, stderr = ssh.exec_command(check_queue_command)
        queue_exists = stdout.read().decode('utf-8')

        if "bandwidth-limit" in queue_exists:
            # If the queue exists, update its bandwidth limits
            update_queue_command = f"/queue simple set [find name=bandwidth-limit] max-limit={download_limit}/{upload_limit}"
            ssh.exec_command(update_queue_command)
            print(f"Bandwidth limits updated successfully on router {ip}")
        else:
            # If the queue doesn't exist, create a new one
            queue_command = f"/queue simple add max-limit={download_limit}/{upload_limit} name=bandwidth-limit target=0.0.0.0/0"
            ssh.exec_command(queue_command)
            print(f"New bandwidth limit queue created on router {ip}")

        ssh.close()

    except Exception as e:
        print(f"Failed to connect to router {ip}: {str(e)}")

class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MikroTik Bandwidth Limiter")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.new_router_btn = QtWidgets.QPushButton("New Router")
        self.edit_bandwidth_btn = QtWidgets.QPushButton("Edit Bandwidth Limit")

        self.layout.addWidget(self.new_router_btn)
        self.layout.addWidget(self.edit_bandwidth_btn)

        self.new_router_btn.clicked.connect(self.open_new_router_window)
        self.edit_bandwidth_btn.clicked.connect(self.open_edit_bandwidth_window)

        self.setLayout(self.layout)

    def open_new_router_window(self):
        self.new_router_window = NewRouterWindow()
        self.new_router_window.show()

    def open_edit_bandwidth_window(self):
        self.edit_bandwidth_window = EditBandwidthWindow()
        self.edit_bandwidth_window.show()

class NewRouterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add/Delete Router")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.new_router_layout = QtWidgets.QFormLayout()
        self.new_router_name = QtWidgets.QLineEdit()
        self.new_router_ip = QtWidgets.QLineEdit()
        self.new_router_username = QtWidgets.QLineEdit()
        self.new_router_password = QtWidgets.QLineEdit()
        self.new_router_port = QtWidgets.QLineEdit()
        self.add_router_btn = QtWidgets.QPushButton("Add Router")
        self.delete_router_btn = QtWidgets.QPushButton("Delete Selected Router")

        self.new_router_layout.addRow("Name:", self.new_router_name)
        self.new_router_layout.addRow("IP Address:", self.new_router_ip)
        self.new_router_layout.addRow("Username:", self.new_router_username)
        self.new_router_layout.addRow("Password (leave blank if none):", self.new_router_password)
        self.new_router_layout.addRow("Port:", self.new_router_port)
        self.new_router_layout.addRow(self.add_router_btn, self.delete_router_btn)

        self.router_table = QtWidgets.QTableWidget()
        self.router_table.setColumnCount(5)
        self.router_table.setHorizontalHeaderLabels(["Name", "IP", "Username", "Password", "Port"])
        self.router_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.router_table.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        self.router_table.horizontalHeader().setStretchLastSection(True)

        self.populate_router_table()

        self.layout.addLayout(self.new_router_layout)
        self.layout.addWidget(self.router_table)
        self.setLayout(self.layout)

        self.add_router_btn.clicked.connect(self.add_router)
        self.delete_router_btn.clicked.connect(self.delete_router)

    def populate_router_table(self):
        self.router_table.setRowCount(0)
        for router in routers_list:
            row_position = self.router_table.rowCount()
            self.router_table.insertRow(row_position)
            self.router_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(router['name']))
            self.router_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(router['ip']))
            self.router_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(router['username']))
            self.router_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(router['password'] or ""))
            self.router_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(router['port']))

    def add_router(self):
        name = self.new_router_name.text()
        ip = self.new_router_ip.text()
        username = self.new_router_username.text()
        password = self.new_router_password.text()  # Allow empty password
        port = self.new_router_port.text()

        if name and ip and username and port:
            routers_list.append({
                'name': name,
                'ip': ip,
                'username': username,
                'password': password,  # Store even if password is empty
                'port': port
            })
            save_routers()
            QtWidgets.QMessageBox.information(self, "Success", f"Router {name} added!")

            self.new_router_name.clear()
            self.new_router_ip.clear()
            self.new_router_username.clear()
            self.new_router_password.clear()
            self.new_router_port.clear()
            self.populate_router_table()

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields except password!")

    def delete_router(self):
        selected_row = self.router_table.currentRow()
        if selected_row >= 0:
            router = routers_list[selected_row]
            routers_list.pop(selected_row)
            save_routers()
            QtWidgets.QMessageBox.information(self, "Success", f"Router {router['name']} deleted!")
            self.populate_router_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a router to delete!")

class EditBandwidthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Bandwidth on Routers")
        self.setGeometry(100, 100, 800, 400)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Bandwidth limit inputs
        self.limit_bandwidth_layout = QtWidgets.QFormLayout()
        self.download_limit = QtWidgets.QLineEdit()
        self.upload_limit = QtWidgets.QLineEdit()
        self.apply_limit_btn = QtWidgets.QPushButton("Apply Bandwidth Limit")

        # Labels for the bandwidth inputs
        self.limit_bandwidth_layout.addRow("Download Limit (e.g., 10M for 10Mbps):", self.download_limit)
        self.limit_bandwidth_layout.addRow("Upload Limit (e.g., 5M for 5Mbps):", self.upload_limit)
        self.limit_bandwidth_layout.addRow(self.apply_limit_btn)

        self.layout.addLayout(self.limit_bandwidth_layout)
        self.setLayout(self.layout)

        # Button click handler
        self.apply_limit_btn.clicked.connect(self.apply_bandwidth_limit)

    def apply_bandwidth_limit(self):
        download_limit = self.download_limit.text()
        upload_limit = self.upload_limit.text()

        if not routers_list:
            QtWidgets.QMessageBox.warning(self, "Error", "No routers to update bandwidth!")
            return

        if not download_limit or not upload_limit:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter valid bandwidth limits!")
            return

        success_count = 0
        failed_count = 0

        for router in routers_list:
            try:
                edit_bandwidth_limit(router['ip'], router['username'], router['password'], router['port'], download_limit, upload_limit)
                success_count += 1
            except Exception as e:
                print(f"Failed to update bandwidth for router {router['name']}: {e}")
                failed_count += 1

        QtWidgets.QMessageBox.information(self, "Result", f"Bandwidth limit applied successfully to {success_count} routers, failed for {failed_count} routers.")

if __name__ == "__main__":
    load_routers()  # Load existing routers from file
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
