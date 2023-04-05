import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import paramiko


def filter_excel(file_path):
    df = pd.read_excel(file_path)
    filtered_df = df.loc[df['Exporter_name_os'] == 'exporter_linux']
    filtered_df = filtered_df.loc[~df['Exporter_name_app'].isin(['exporter_sm', 'exporter_acm', 'exporter_aes'])]
    return filtered_df

def toggle_checkboxes(self, enabled):
    if enabled:
        state = tk.NORMAL
    else:
        state = tk.DISABLED

    self.linux_user_checkbox.config(state=state)
    self.sm_user_checkbox.config(state=state)
    self.gateway_snmp_checkbox.config(state=state)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create input fields and labels
        self.ip_address_var = tk.StringVar()
        self.root_password_var = tk.StringVar()
        self.login_user_var = tk.StringVar()
        self.login_password_var = tk.StringVar()
        self.new_user_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        #store the state of the checkboxes
        self.create_linux_user_var = tk.BooleanVar(value=True)
        self.create_sm_user_var = tk.BooleanVar(value=False)
        self.add_gateway_snmp_var = tk.BooleanVar(value=False)
        #checkboxes 
        self.linux_user_checkbox = tk.Checkbutton(self, text="Create Linux User", variable=self.create_linux_user_var)
        self.linux_user_checkbox.grid(row=0, column=0)
        self.sm_user_checkbox = tk.Checkbutton(self, text="Create SM User", variable=self.create_sm_user_var)
        self.sm_user_checkbox.grid(row=0, column=1)
        self.gateway_snmp_checkbox = tk.Checkbutton(self, text="Add Gateway SNMP", variable=self.add_gateway_snmp_var)
        self.gateway_snmp_checkbox.grid(row=1, column=0, columnspan=2)

        tk.Label(self, text="IP Address").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.ip_address_var).grid(row=2, column=1)

        tk.Label(self, text="Root Password").grid(row=3, column=0)
        tk.Entry(self, show="*", textvariable=self.root_password_var).grid(row=3, column=1)

        tk.Label(self, text="Login User").grid(row=4, column=0)
        tk.Entry(self, textvariable=self.login_user_var).grid(row=4, column=1)

        tk.Label(self, text="Login Password").grid(row=5, column=0)
        tk.Entry(self, show="*", textvariable=self.login_password_var).grid(row=5, column=1)

        tk.Label(self, text="New User").grid(row=6, column=0)
        tk.Entry(self, textvariable=self.new_user_var).grid(row=6, column=1)

        tk.Label(self, text="New Password").grid(row=7, column=0)
        tk.Entry(self, show="*", textvariable=self.new_password_var).grid(row=7, column=1)

        # Create submit button
        tk.Button(self, text="Create New User", command=self.submit).grid(row=8, column=0, columnspan=2)

        # Add browse button for selecting Excel file
        tk.Button(self, text="Browse Excel File", command=self.browse_file).grid(row=9, column=0, columnspan=2)

        # Add next button for loading next row
        tk.Button(self, text="Next", command=self.load_next_row).grid(row=10, column=0, columnspan=2)

        # Initialize filtered DataFrame
        self.filtered_df = None
        self.current_index = 0


    #Browse file method
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:  # File is selected
            self.filtered_df = filter_excel(file_path)
            self.load_data()
            self.toggle_checkboxes(False)  # Disable checkboxes
        else:
            self.toggle_checkboxes(True)  # Enable checkboxes if no file is selected


    def load_data(self):
        if self.filtered_df is None:
            self.toggle_checkboxes(True)  # Enable checkboxes
        elif self.current_index < len(self.filtered_df):
            row = self.filtered_df.iloc[self.current_index]
            self.ip_address_var.set(row['IP Address'])
            self.login_type_var.set("Linux with root access")
            self.toggle_checkboxes(False)  # Disable checkboxes
        else:
            self.toggle_checkboxes(True)  # Enable checkboxes


    def load_next_row(self):
        if self.filtered_df is None:
            self.toggle_checkboxes(True)  # Enable checkboxes
        else:
            self.current_index += 1
            self.load_data()



    def submit(self):
        ip_address = self.ip_address_var.get()
        root_password = self.root_password_var.get()
        login_user = self.login_user_var.get()
        login_password = self.login_password_var.get()
        new_user = self.new_user_var.get()
        new_password = self.new_password_var.get()

        create_linux_user = self.create_linux_user_var.get()
        create_sm_user = self.create_sm_user_var.get()
        add_gateway_snmp = self.add_gateway_snmp_var.get()

        if self.filtered_df is not None:
            row = self.filtered_df.iloc[self.current_index]
            exporter_name_app = row["Exporter_name_app"]
        else:
            exporter_name_app = None

        try:
            create_new_user(ip_address, root_password, login_user, login_password, new_user, new_password, exporter_name_app, create_linux_user, create_sm_user, add_gateway_snmp)
            messagebox.showinfo("Success", "User created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))



def create_new_user(ip_address, root_password, login_user, login_password, new_user, new_password, exporter_name_app, create_linux_user, create_sm_user, add_gateway_snmp):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip_address, username=login_user, password=login_password)

    if login_user != "root":
        ssh.exec_command("echo '{}' | sudo -S su".format(root_password))

    if create_linux_user:
        ssh.exec_command("useradd -m {}".format(new_user))
        ssh.exec_command("echo '{}:{}' | chpasswd".format(new_user, new_password))

    if create_sm_user or (exporter_name_app == "exporter_sm"):
        # Run the commands for adding an SM user
        stdin, stdout, stderr = ssh.exec_command("addCustAccount")
        stdin.write(f"{new_user}\n")
        stdin.write(f"{new_password}\n")
        stdin.write(f"{new_password}\n")
        stdin.flush()

    # Add other actions for add_gateway_snmp if necessary
    if add_gateway_snmp:
        pass

    ssh.close()

if __name__ == "__main__":
    app = App()
    app.title("New User Creator")
    app.mainloop()

    def submit(self):
        ip_address = self.ip_address_var.get()
        root_password = self.root_password_var.get()
        login_user = self.login_user_var.get()
        login_password = self.login_password_var.get()
        new_user = self.new_user_var.get()
        new_password = self.new_password_var.get()

        # Get the selected login type
        login_type = self.login_type_var.get()

        # Call the appropriate function based on the selected login type
        if login_type == "Linux with root access":
            create_new_user(ip_address, root_password, login_user, login_password, new_user, new_password)
        elif login_type == "Windows with administrator access":
            create_new_user_windows(ip_address, login_user, login_password, new_user, new_password)
