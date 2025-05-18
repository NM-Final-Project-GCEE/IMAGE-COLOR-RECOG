import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from math import sqrt
from PIL import Image, ImageTk

# Load the color dataset
def load_color_data():
    colors = pd.read_csv('colors.csv')
    colors['RGB'] = colors[['R', 'G', 'B']].apply(tuple, axis=1)
    return colors

# Calculate Euclidean distance
def get_color_distance(rgb1, rgb2):
    return sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

# Find closest color
def get_closest_color(rgb, color_data):
    return min(color_data.itertuples(), key=lambda row: get_color_distance(rgb, row.RGB))

# Mouse click callback
def on_mouse_click(event):
    if image_rgb:
        x, y = event.x, event.y

        # Prevent out-of-range access
        if 0 <= x < display_width and 0 <= y < display_height:
            orig_x = int(x * image_width / display_width)
            orig_y = int(y * image_height / display_height)
            rgb = image_rgb.getpixel((orig_x, orig_y))
            update_ui(rgb)

# Update UI labels and color box
def update_ui(rgb):
    closest = get_closest_color(rgb, color_data)
    rgb_label.configure(text=f'RGB: {rgb}')
    color_name_label.configure(text=f'Color: {closest.name}')
    hex_color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    color_box.configure(fg_color=hex_color)  # use fg_color for CTkLabel
    print(f'Detected Color: {closest.name}, RGB: {rgb}')

# Open and display image
def open_image():
    global image_rgb, image_width, image_height, display_width, display_height
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
    if file_path:
        image = Image.open(file_path).convert('RGB')
        image_rgb = image
        image_width, image_height = image.size
        display_width, display_height = 600, 400  # Resize for display

        resized_image = image.resize((display_width, display_height))
        image_tk = ImageTk.PhotoImage(resized_image)

        # Set the image and clear the placeholder text
        image_label.configure(image=image_tk, text="")
        image_label.image = image_tk  # Prevent garbage collection
        image_label.bind('<Button-1>', on_mouse_click)
    if not file_path:
        image_label.configure(image=None, text="No Image Loaded")


# Initialize CTk
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.title("Color Detection App")

color_data = load_color_data()
image_rgb = None  # To be loaded
image_width = image_height = display_width = display_height = 0

# Layout
frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=20)

# Left: image display
image_label = ctk.CTkLabel(frame, text="No Image Loaded")
image_label.grid(row=0, column=0, padx=10, pady=10)

# Right: info panel
info_frame = ctk.CTkFrame(frame,width=100)
info_frame.grid(row=0, column=1, padx=15, pady=15)
info_frame.grid_propagate(False)

open_button = ctk.CTkButton(info_frame, text="Open Image", command=open_image)
open_button.pack(pady=10)

rgb_label = ctk.CTkLabel(info_frame, text="RGB: None")
rgb_label.pack(pady=5)

color_name_label = ctk.CTkLabel(info_frame, text="Color: None")
color_name_label.pack(pady=5)

color_box = ctk.CTkLabel(info_frame, width=100, height=50, fg_color="white", text="",corner_radius=5)
color_box.pack(pady=5)

# Run the app
root.mainloop()
