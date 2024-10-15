# Bandwidth-Limit

This Python-based application allows you to easily limit or update bandwidth limits on MikroTik routers via SSH. You can set upload and download limits for multiple routers at once, ensuring that network resources are distributed effectively.

## How to Download and Run the Application

### Step 1: Download Python

1. Go to [python.org](https://www.python.org/downloads/).
2. Click on the "Download" button for your operating system.
3. Follow the instructions on the website to install Python.


### Step 2: Download the Application

1. Go to the GitHub repository link: (https://github.com/Nysa11/Bandwidth-Limit).
2. Click on the green "Code" button and select "Download ZIP".
3. Extract (unzip) the downloaded ZIP file to a folder on your computer.

### Step 3: Install Required Libraries

1. Open the Command Prompt (Windows) or Terminal (Mac/Linux).
   - For Windows: Press `Win + R`, type `cmd`, and press Enter.
   - For Mac: Open Finder, go to Applications > Utilities, and open Terminal.
   - For Linux: Look for Terminal in your applications.

2. In the Command Prompt or Terminal, type the following command and press Enter:

   ```bash
   pip install PyQt5 paramiko

This command will install the additional tools needed for the application.

### Step 4: Run the Application

1. Still in the Command Prompt or Terminal, navigate to the folder where you extracted the application files. For example:

   ```bash
   cd C:\Users\YourName\Downloads\Bandwidth-Limit-main\Bandwidth-Limit-main
   
- Note: Make sure to change YourName to your actual username on your computer. For example, if your username is John, you should type:

   ```bash
   cd C:\Users\John\Downloads\Bandwidth-Limit-main\Bandwidth-Limit-main

2. Once you're in the correct folder, type the following command and press Enter to start the application:

   ```bash
   python bandwidth.py

### Step 5: Using the Application

1. Add a Router:
  - Enter the router’s name, IP address, username, password (if needed), and port number.
  - Click the "Add Router" button to save it to your list.

2. Delete a Router:
  - Select a router from the list and click the "Delete Selected Router" button to remove it.

3. Limit Bandwidth for All Routers:
  - Enter the desired upload and download limits (in kbps or mbps).
  - Click the "Apply Bandwidth Limit" button to apply the limits to all routers in your list.

4. Limit Bandwidth for a Specific Router:
  - Select a router from the list for which you want to set a bandwidth limit.
  - Enter the desired upload and download limits (in kbps or Mbps).
  - Click the "Apply Bandwidth Limit" button to apply the limits to the selected router.

5. Saving Your Routers
  - The application automatically saves the router information so you don’t lose it. When you open the application again, your routers will still be there!
