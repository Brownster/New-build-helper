import pandas as pd
import paramiko
from flask import Flask, render_template, request, redirect, url_for, flash

# You may need to move the filter_excel, create_new_user, and other functions here

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
            flash("User created successfully.", "success")
        except Exception as e:
            flash(str(e), "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
