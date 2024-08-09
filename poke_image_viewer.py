"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import poke_api
from PIL import ImageTk
import image_lib
import ctypes

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# TODO: Create the images directory if it does not exist
if not os.path.isdir(images_dir):
    os.mkdir(images_dir)
# Create the main window
root = Tk()
root.title("Pokemon Viewer")

#Function for getting combobox value
def pokemon_selection_handler(event):
    selected_index = pokemon_combobox.current()
    pokemon_name = pokemon_nameslist[selected_index]
    file_path = poke_api.download_pokemon_artwork(pokemon_name, images_dir)
    poke_ball_image['file'] = file_path
    selected_pokemon_name = pokemon_combobox.get()
    
    if selected_pokemon_name:
        action_button.config(state="normal")
    
    return

#Function for Button click
def apply_image_on_button_click():
    selected_pokemon_name = pokemon_combobox.get()
    image_file_path = os.path.join(images_dir, f"{selected_pokemon_name}.jpg")
    
    if os.path.exists(image_file_path):
        image_lib.set_desktop_background_image(image_file_path)
    else:
        print(f"Image file not found: {image_file_path}")

# TODO: Set the icon
app_id = 'COMP593.PokeImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
pokemon_ball_file_path = os.path.join(script_dir,'poke_ball.ico')
root.iconbitmap(pokemon_ball_file_path )
a=0

# TODO: Create frames
fr_1 = ttk.Frame(root)
fr_1.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
fr_1.rowconfigure(0, weight=1)
fr_1.columnconfigure(0, weight=1)

fr_2 = ttk.Frame(root)
fr_2.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

fr_3 = ttk.Frame(root)
fr_3.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

# TODO: Populate frames with widgets and define event handler functions
# Inserting poke_ball image in fr_1
image_path = os.path.join(script_dir, 'poke_ball.png')
poke_ball_image = PhotoImage(file=image_path)
logo_label = ttk.Label(fr_1, image=poke_ball_image)
logo_label.grid(padx=10, pady=10)

# Inserting the Combobox in fr_2
pokemon_nameslist = poke_api.get_pokemon_nameslist(1000)
pokemon_combobox = ttk.Combobox(fr_2, values=pokemon_nameslist, state='readonly')
pokemon_combobox.set("Select a Pokemon")
pokemon_combobox.grid(row=1, column=2, padx=5, pady=5) 

#Displaying image after user selection from Combobox
pokemon_combobox.bind('<<ComboboxSelected>>', pokemon_selection_handler )

# Inserting button in fr_3
action_button = Button(fr_3, text="Set as Desktop Image", command=apply_image_on_button_click, state="disabled")
action_button.grid(row=1, column=2, padx=5, pady=5) 

root.mainloop()