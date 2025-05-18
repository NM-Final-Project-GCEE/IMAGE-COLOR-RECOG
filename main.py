import tkinter as tk
from tkinter import filedialog
import pandas as pd
from math import sqrt
from PIL import Image, ImageTk

# Load the CSV dataset of color names and RGB values
def load_color_data():
    colors = pd.read_csv("colors.csv")  # Make sure 'colors.csv' is in the same directory
    colors['RGB'] = colors[['R', 'G', 'B']].apply(tuple, axis=1)
    return colors

# Calculate the Euclidean distance between two RGB colors
def get_color_distance(rgb1, rgb2):
    return sqrt((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2)

# Find the closest matching color from the dataset
def get_closest_color(rgb, color_data):
    min_distance = float('inf')
    closest_color = None
    for index, row in color_data.iterrows():
        color_rgb = row['RGB']
        distance = get_color_distance(rgb, color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color = row
    return closest_color

# Handle the mouse click event to capture the pixel RGB
def on_mouse_click(event):
    x, y = event.x, event.y
    
    # Adjust the coordinates to match the resized image
    original_x = int(x * image_width / display_width)
    original_y = int(y * image_height / display_height)
    
    rgb = image_rgb.getpixel((original_x, original_y))  # Get the RGB value of the clicked pixel
    update_ui(rgb)

# Update the UI with the detected color information
def update_ui(rgb):
    closest_color = get_closest_color(rgb, color_data)
    color_name = closest_color['name']
    color_rgb = closest_color['RGB']
    
    # Update UI labels
    rgb_label.config(text=f"RGB: {rgb}")
    color_name_label.config(text=f"Color: {color_name}")
    
    # Update the color display box
    color_box.config(bg=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    
    # Display the detected color's RGB value
    print(f"Detected Color: {color_name} {color_rgb}")

# Open the image file
def open_image():
    global image_rgb, image_width, image_height, display_width, display_height
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Open the image and get its original dimensions
        image = Image.open(file_path)
        image_rgb = image.convert('RGB')  # Convert image to RGB mode
        image_width, image_height = image.size
        
        # Resize the image to fit within the Tkinter window (set display dimensions)
        display_width, display_height = 600, 400  # Resize to fit window size
        image_resized = image.resize((display_width, display_height))  # Resize image
        
        # Convert the resized image to a format Tkinter can use
        image_tk = ImageTk.PhotoImage(image_resized)
        
        # Display the image in the Tkinter window
        image_label.config(image=image_tk)
        image_label.image = image_tk  # Keep a reference to avoid garbage collection
        
        # Bind the mouse click event to the image label
        image_label.bind("<Button-1>", on_mouse_click)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Color Detection App")

# Load the color dataset
color_data = load_color_data()

# Create a frame for the image and the color info
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Label to display the image
image_label = tk.Label(frame)
image_label.grid(row=0, column=0, padx=10, pady=10)

# Frame for color info (right side)
info_frame = tk.Frame(frame)
info_frame.grid(row=0, column=1, padx=10, pady=10)

# Open image button
open_button = tk.Button(info_frame, text="Open Image", command=open_image)
open_button.pack(pady=5)

# Labels to display color information
rgb_label = tk.Label(info_frame, text="RGB: None")
rgb_label.pack(pady=5)

color_name_label = tk.Label(info_frame, text="Color: None")
color_name_label.pack(pady=5)

# Color display box
color_box = tk.Label(info_frame, width=20, height=2, bg="white")
color_box.pack(pady=5)

# Run the Tkinter loop
root.mainloop()
