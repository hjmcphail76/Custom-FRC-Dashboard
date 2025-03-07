from math import cos, sin, radians
import time
import tkinter as tk
from PIL import Image, ImageTk

import nt_interface


# time.sleep(1)  # Make sure nt_interface is done setting up and finds the right IP

root = tk.Tk()
root.title("Custom FRC Dashboard")
root.geometry("800x480")

image = Image.open("2025 REEFSCAPE Blue.png")


photo = ImageTk.PhotoImage(image)

# Get image dimensions
image_width, image_height = image.size

picture = tk.Label(root, image=photo)
picture.place(relx=0.5, rely=0.5, anchor="center")


def create_buttons_in_circle(center_x, center_y, radius, buttons=[]):
    """Function to create buttons in a circle around a center point"""
    for i in range(6):
        angle = (
            -i * (360 / 6) + (180 / 6) * 3
        )  # Evenly divide angles with an offset so they are positioned correctly (1 is at bottom)
        angle_rad = radians(angle)  # Convert to radians

        # Calculate button positions
        x = center_x + radius * cos(angle_rad)
        y = center_y + radius * sin(angle_rad)

        if i < len(buttons):  # Update existing buttons
            buttons[i].place(x=x, y=y, anchor="center")
        else:  # Create new buttons
            button = tk.Button(root, text=f"Button {i + 1}")
            button.config(fg="black", width=8, height=4, bg="red")
            button.place(x=x, y=y, anchor="center")
            buttons.append(button)
    return buttons


def create_level_buttons():
    """Create L1-L3 Buttons"""
    buttons = []
    for i in range(3):
        button = tk.Button(
            root, text=f"L{i+1}", bg="red", fg="black", font=("Courier", 44)
        )
        button.grid_configure(column=0, row=i, sticky="nsew")
        root.rowconfigure(i, weight=1)
        buttons.append(button)
    root.columnconfigure(4, weight=1)
    return buttons


def create_hp_buttons():
    """Create Left and Right HP buttons"""
    buttons = []
    l = tk.Button(root, text="Left HP", bg="red", fg="black", font=("Courier", 44))
    r = tk.Button(root, text="Right HP", bg="red", fg="black", font=("Courier", 44))

    l.grid_configure(row=0, column=4, sticky="new")
    r.grid_configure(row=0, column=5, sticky="new")
    buttons.append(l)
    buttons.append(r)
    return buttons


def create_position_buttons():
    names = ["Left", "Algae", "Right"]
    buttons = []
    for i in range(3):
        button = tk.Button(
            root, text=names[i], bg="red", fg="black", font=("Courier", 30)
        )
        button.grid_configure(column=i + 3, row=3, sticky="nsew")
        root.columnconfigure(i + 3, weight=1)
        buttons.append(button)
    return buttons


def update_positions(event):
    """Function to update reef button positions when the window is resized"""
    center_x = picture.winfo_x() + image_width // 2
    center_y = picture.winfo_y() + image_height // 2

    # Update button positions
    create_buttons_in_circle(center_x, center_y, 200, reefButtons)


def reef_side_selected(index):
    """Function called when a reef button is clicked."""
    for i in range(len(reefButtons)):
        reefButtons[i].config(bg="red")
    reefButtons[index].config(bg="green")
    nt_interface.setNum("Reef Side", index + 1)


def level_selected(index):
    """Function called when a level button is clicked."""
    for i in range(len(levelButtons)):
        levelButtons[i].config(bg="red")
    levelButtons[index].config(bg="green")

    nt_interface.setNum("Level", index + 1)


def position_selected(index):
    """Function called when a position button is clicked."""
    for i in range(len(positionButtons)):
        positionButtons[i].config(bg="red")
    positionButtons[index].config(bg="green")

    nt_interface.setNum("Position", index)  # No +1 since it goes 0,1,2


def hp_selected(index):
    """Function called when a HP button is clicked."""
    for i in range(len(hpButtons)):
        hpButtons[i].config(bg="red")
    hpButtons[index].config(bg="green")

    nt_interface.setNum("HumanPlayer", index)


# Create buttons initially and set commands
hpButtons = create_hp_buttons()
reefButtons = create_buttons_in_circle(400, 240, 200)
positionButtons = create_position_buttons()
levelButtons = create_level_buttons()


for i in range(6):
    reefButtons[i].config(command=lambda i=i: reef_side_selected(i))

for i in range(3):
    levelButtons[i].config(command=lambda i=i: level_selected(i))

for i in range(3):
    positionButtons[i].config(command=lambda i=i: position_selected(i))

for i in range(2):
    hpButtons[i].config(command=lambda i=i: hp_selected(i))

# Bind the <Configure> event to dynamically update positions
root.bind("<Configure>", update_positions)

root.mainloop()
