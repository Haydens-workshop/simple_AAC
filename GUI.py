import tkinter as tk
import os
import pygame
import json


pygame.mixer.init()


def load_data(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
    return data


def play_sound(sound_path):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

##### Eventually Sounds will go here #####
def create_sound_button(name, container, color, row, col, width, height):
    sound_path = os.path.join(sounds_path, f"{name}.wav")
    button = tk.Button(container, text=name, bg=color,
                       command=lambda: play_sound(sound_path))
    button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
    container.grid_columnconfigure(col, weight=1, minsize=width)
    container.grid_rowconfigure(row, weight=1, minsize=height)

###### category of who/what goes where  #####
def place_buttons(data, container, color_dict):
    for widget in container.winfo_children():
        widget.destroy()
    
    # ##### Update container dimensions  #####
    container.update_idletasks() 
    num_per_row = max(1, container.winfo_width() // min_button_width)
    button_width = max(min_button_width, container.winfo_width() // num_per_row)
    button_height = min_button_height

    ###### Place each button #####
    for i, name in enumerate(data):
        color = color_dict.get(name, color_dict["default"])
        create_sound_button(name, container, color, i // num_per_row, i % num_per_row, button_width, button_height)

root = tk.Tk()
root.title("Simple Words")

###### Window dimensions #####
window_width = 800  
window_height = 600  
root.geometry(f"{window_width}x{window_height}")

###### Minimum button dimensions #####
min_button_width = 75
min_button_height = 50

# Determine the base directory for the script
base_dir = os.path.dirname(os.path.realpath(__file__))

###### Paths relative to the base directory #####
sounds_path = os.path.join(base_dir, "AAC", "Sounds")
people_json_path = os.path.join(base_dir, "people", "people.json")
verbs_json_path = os.path.join(base_dir, "verbs", "verbs.json")
adjectives_json_path = os.path.join(base_dir, "adjectives", "adjectives.json")
affirmations_json_path = os.path.join(base_dir, "affirmations", "affirmations.json")

###### Load data for people, verbs, adjectives, and affirmations #####
people = load_data(people_json_path)["people"]
verbs = load_data(verbs_json_path)["verbs"]
adjectives = load_data(adjectives_json_path)["adjectives"]
affirmations = load_data(affirmations_json_path)["affirmations"]

###### Colors for each category #####
people_color = "lightpink"
verb_color = "lightgreen"
adj_color = "lightblue"
default_affirmation_color = "lightyellow"
affirmation_color_dict = {
    "Yes": "green",
    "Go": "green",
    "Please": "green",
    "Thank you": "green",
    "Stop": "red",
    "No": "red",
    "default": default_affirmation_color
}

##### Create frames for each category #####
people_frame = tk.Frame(root)
verbs_frame = tk.Frame(root)
adjectives_frame = tk.Frame(root)
affirmations_frame = tk.Frame(root)

people_frame.pack(fill='x', expand=True)
verbs_frame.pack(fill='x', expand=True)
adjectives_frame.pack(fill='x', expand=True)
affirmations_frame.pack(fill='x', expand=True)

###### re-place buttons when the window is resized ##### 
def on_resize(event):
    if event.widget == root:
        place_buttons(people, people_frame, {"default": people_color})
        place_buttons(verbs, verbs_frame, {"default": verb_color})
        place_buttons(adjectives, adjectives_frame, {"default": adj_color})
        place_buttons(affirmations, affirmations_frame, affirmation_color_dict)


root.bind('<Configure>', on_resize)


root.after(100, lambda: on_resize(tk.Event(widget=root)))

root.mainloop()
