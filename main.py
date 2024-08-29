from curses.ascii import isdigit
import tkinter as tk
from tkinter import messagebox
import random
import string
from threading import Thread, Event
import pyperclip
import sys
import traceback


def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = ''.join(traceback.format_exception(
        exc_type, exc_value, exc_traceback))
    with open('error_log.log', 'w') as error_file:
        error_file.write(error_msg)
    messagebox.showerror(
        "Error", f"An error occurred. Details have been written to error_log.log")


sys.excepthook = handle_exception

TIMER = 10
LENGTH = '16'
current_thread = None
stop_event = Event()

def callback(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

def generate_password():
    global current_thread, stop_event

    # Stop the previous thread if it's running
    if current_thread and current_thread.is_alive():
        stop_event.set()
        current_thread.join()

    message_label.config(text='')
    length = length_entry.get()
    if not (length.isdigit()) or int(length) <= 0:
        length = LENGTH
        length_entry.delete(0, 'end')
        length_entry.insert(0, LENGTH)
    use_special = special_var.get()

    characters = string.ascii_letters + string.digits
    if use_special:
        characters += "-_?!@#$%"

    password = ''.join(random.choice(characters) for _ in range(int(length)))

    pyperclip.copy(password)
    result_entry_text.set(password)

    stop_event.clear()
    current_thread = Thread(target=clear_clipboard, daemon=True)
    current_thread.start()


def clear_clipboard():
    for i in range(TIMER, -1, -1):
        if stop_event.is_set():
            return
        message_label.config(
            text=f'Password has been copied to clipboard. It will be erased in {i} seconds.')
        stop_event.wait(1)

    if not stop_event.is_set():
        pyperclip.copy('')
        message_label.config(
            text='The password has been erased from the clipboard.')


# Create the main window
root = tk.Tk()
root.title("Random Password Generator")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window width and height
window_width = 400
window_height = 300

# Calculate the x and y coordinates to center the window
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

# Set the window geometry
root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

# Create and place widgets
length_label = tk.Label(root, text="Password Length:")
length_label.pack(pady=5)

vcmd = (root.register(callback))

length_entry = tk.Entry(root, justify='center',validate='all', validatecommand=(vcmd, '%P'))
length_entry.pack(pady=5)
length_entry.insert(0, str(LENGTH))  # Default length

special_var = tk.BooleanVar(value=True)
special_check = tk.Checkbutton(
    root, text="Include Special Characters", variable=special_var)
special_check.pack(pady=5)

generate_button = tk.Button(
    root, text="Generate Password", command=generate_password)
generate_button.pack(pady=10)

result_label = tk.Label(root, text="Generated Password:")
result_label.pack(pady=5)

result_entry_text = tk.StringVar()
result_entry = tk.Entry(
    root, textvariable=result_entry_text, state="readonly", justify='center')
result_entry.pack(pady=5)

message_label = tk.Label(root, fg='red', wraplength=300)
message_label.pack(pady=5)

# Start the GUI event loop
root.mainloop()
