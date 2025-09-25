import tkinter
from tkinter import messagebox
from password_generator import PasswordGenerator
import pyperclip
import json

# ------------------------- PASSWORD GENERATOR ---------------------------- #
pwgen = PasswordGenerator()

# -------------------------- MANAGE PASSWORDS ----------------------------- #

PASSWORD_FILE = "passwords.json"
CONFIG_FILE = "config.txt"

def save_password(website, username, password):
    '''appends a new credential into the password file'''
    # create an entry for the new password data
    new_entry = { website :
                      {
                          "email": username,
                          "password": password
                      }
                  }

    try:
        # open the existing PASSWORD_FILE and append to it
        # read the old data
        with open(PASSWORD_FILE, "r") as file_passwords:
            data = json.load(file_passwords)

        # update the old data and update it
        with open(PASSWORD_FILE, "w") as file_passwords:
            data.update(new_entry)
            json.dump(data, file_passwords, indent=4)
    except FileNotFoundError:
        # we ended up here since PASSWORD_FILE does not exist
        # create PASSWORD_FILE and store this as the first entry
        with open(PASSWORD_FILE, "w") as file_passwords:
            data = {}
            data.update(new_entry)
            json.dump(data, file_passwords, indent=4)

def load_passwords():
    '''loads all the accounts from the password file'''
    try:
        with open(PASSWORD_FILE, "r") as file_passwords:
            data = json.load(file_passwords)
            return data
    except FileNotFoundError:
        return {}

def get_default_username():
    '''gets the default username from config.txt or returns an empty string if file does not exist'''
    username = ""
    try:
        with open(CONFIG_FILE) as file_config:
            username = file_config.readline().strip()
    except FileNotFoundError:
        pass
    return username

# ---------------------------- UI SETUP ------------------------------- #

# create a window
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# place a lock image onto the window
canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
photo_lock = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo_lock)
canvas.grid(row=0, column=1)

# create a row for website + search button
label_website= tkinter.Label(text="Website")
label_website.grid(row=1, column=0)
input_website = tkinter.Entry(width=24)
input_website.grid(row=1, column=1)
input_website.focus()
def button_search_password_click():
    accounts = load_passwords()
    try:
        user_and_pass = accounts[input_website.get()]
        email = user_and_pass['email']
        password = user_and_pass['password']
        messagebox.showinfo(input_website.get(), f"Email: {email}\nPassword: {password}")
    except KeyError:
        messagebox.showerror(input_website.get(), f"No credentials have been stored for \"{input_website.get()}\"")
button_generate_password = tkinter.Button(text="Search", command=button_search_password_click)
button_generate_password.grid(row=1, column=2)

# create a row for email/username
label_username = tkinter.Label(text="Email/Username")
label_username.grid(row=2, column=0)
input_username = tkinter.Entry(width=35)
input_username.grid(row=2, column=1, columnspan=2)
default_username = get_default_username()
input_username.insert(tkinter.END, default_username)

# create a row for password + generate password button
label_password = tkinter.Label(text="Password")
label_password.grid(row=3, column=0)
input_password = tkinter.Entry(width=24)
input_password.grid(row=3, column=1)
def button_generate_password_click():
    # generate a password
    password = pwgen.generate_password()

    # add the password to the paperclip so that it can be pasted into a website
    pyperclip.copy(password)

    # display the newly generated password
    if len(input_password.get()) > 0:
        input_password.delete(0, tkinter.END)
    input_password.insert(tkinter.END, password)
button_generate_password = tkinter.Button(text="Generate", command=button_generate_password_click)
button_generate_password.grid(row=3, column=2)

# create a row for the add button
def button_add_click():
    # ensure fields are all filled out
    if len(input_website.get()) == 0:
        messagebox.showerror(title="Website Blank", message="Unable to save since website is blank")
        return
    if len(input_username.get()) == 0:
        messagebox.showerror(title="Username Blank", message="Unable to save since username is blank")
        return
    if len(input_password.get()) == 0:
        messagebox.showerror(title="Password Blank", message="Unable to save since password is blank")
        return

    # double check that the user wants to save the credentials
    save_password(input_website.get(), input_username.get(), input_password.get())
    input_website.delete(0, tkinter.END)
    input_password.delete(0, tkinter.END)
    input_website.focus()
button_add = tkinter.Button(text="Add", width=32, command=button_add_click)
button_add.grid(row=4, column=1, columnspan=2)

# loop for user input
window.mainloop()