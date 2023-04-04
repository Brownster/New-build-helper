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

        # Create a dropdown for login type
        self.login_type_var = tk.StringVar(value="Linux with root access")
        tk.OptionMenu(self, self.login_type_var, "Linux with root access", "Windows with administrator access").grid(row=0, column=0, columnspan=2)

        tk.Label(self, text="IP Address").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.ip_address_var).grid(row=1, column=1)

        tk.Label(self, text="Root Password").grid(row=2, column=0)
        tk.Entry(self, show="*", textvariable=self.root_password_var).grid(row=2, column=1)

        tk.Label(self, text="Login User").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.login_user_var).grid(row=3, column=1)

        tk.Label(self, text="Login Password").grid(row=4, column=0)
        tk.Entry(self, show="*", textvariable=self.login_password_var).grid(row=4, column=1)

        tk.Label(self, text="New User").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.new_user_var).grid(row=5, column=1)

        tk.Label(self, text="New Password").grid(row=6, column=0)
        tk.Entry(self, show="*", textvariable=self.new_password_var).grid(row=6, column=1)

        # Create submit button
        tk.Button(self, text="Create New User", command=self.submit).grid(row=7, column=0, columnspan=2)

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
