Title: Create New User on Linux Server

Description:

This application is a graphical user interface (GUI) tool for creating new users on a remote system using SSH. It is built using Python, the Tkinter library for creating the interface, and Paramiko for handling SSH connections. The main features of this app are as follows:

    The app allows the user to input an IP address, root password, login user and password, new user, and new password.
    The user can choose from three options via checkboxes: create a Linux user, create an SM user, or add a gateway SNMP configuration.
    The user can browse and select an Excel file, which is then filtered to only include rows with specific criteria. The GUI is populated with the data from the filtered rows, and the user can navigate through them using the "Next" button.
    Upon clicking "Create New User," the application connects to the remote system using the provided credentials and executes the appropriate commands based on the selected options.
    An additional window is opened to display the output of the SSH session in real-time, allowing the user to monitor the progress of the operations being performed on the remote system.

This app is designed to facilitate and automate the process of adding new users and applying configurations to remote systems, making the process more streamlined and user-friendly.

Installation:

To use this script, you will need to have Python 3 installed on your computer, as well as the Paramiko and tkinter libraries. You can install these libraries using pip, the Python package manager, by running the following commands in your terminal:

pip install paramiko
pip install tkinter

Usage:

To run the script, simply open the terminal, navigate to the directory where the script is saved, and run the following command:

python create_new_user.py

This will open the GUI, where you can enter the required information and create a new user on your Linux server.

License:

This script is released under the MIT License, which means you are free to use, modify, and distribute the script as long as you include the original license in your distribution. See the LICENSE file for more details.
