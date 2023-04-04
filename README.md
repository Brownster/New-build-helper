Title: Create New User on Linux Server

Description:

This is a Python script that allows users to create a new user on a Linux server with root access. It uses the Paramiko library to establish an SSH connection to the server, switch to the root user, and create a new user with the specified username and password.

The script also comes with a graphical user interface (GUI) built using the tkinter library. The GUI allows users to enter the required information, such as the IP address of the server, the root password, the login username and password, and the details of the new user. The script also includes a feature to hash out the password fields in the GUI for added security.

In addition, the script includes a dropdown menu that allows users to select the type of login function they want to use. Currently, the script only supports Linux servers with root access, but additional login functions can be added to support other types of servers.

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
