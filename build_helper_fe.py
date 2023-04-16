from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import pandas as pd
import paramiko

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
    
def filter_excel(file_path):
    df = pd.read_excel(file_path)
    filtered_df = df.loc[df['Exporter_name_os'] == 'exporter_linux']
    filtered_df = filtered_df.loc[~df['Exporter_name_app'].isin(['exporter_sm', 'exporter_acm', 'exporter_aes'])]
    return filtered_df

app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        ip_address = request.form.get("ip_address")
        root_password = request.form.get("root_password")
        login_user = request.form.get("login_user")
        login_password = request.form.get("login_password")
        new_user = request.form.get("new_user")
        new_password = request.form.get("new_password")
        create_linux_user = request.form.get("create_linux_user") == "on"
        create_sm_user = request.form.get("create_sm_user") == "on"
        add_gateway_snmp = request.form.get("add_gateway_snmp") == "on"

        try:
            create_new_user(ip_address, root_password, login_user, login_password, new_user, new_password, None, create_linux_user, create_sm_user, add_gateway_snmp)
            socketio.emit('message', f"Connecting to {ip_address} as {login_user}...")
        except Exception as e:
            flash(str(e), "error")

    return render_template("index.html")

    socketio.emit('message', "User created successfully.")
    ssh.close()

if __name__ == "__main__":
    socketio.run(app, debug=True)
