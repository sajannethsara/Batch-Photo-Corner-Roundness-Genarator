from tkinter import filedialog , messagebox
import customtkinter
import os
from PIL import Image, ImageDraw, ImageOps
# Global variable to store the folder path
selected_folder_path = ""
selected_integer = 0

def create_new_directory(base_directory, new_folder_name):
    # Combine the base directory and new folder name to get the full path
    new_directory_path = f"{base_directory}/{new_folder_name}"
    
    # Check if the directory already exists
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
        # print(f"Directory '{new_folder_name}' created at '{new_directory_path}'.")
    else:
        new_directory_path = f"{new_directory_path}_New"
        os.makedirs(new_directory_path)
        # print(f"Directory '{new_folder_name}' already exists at '{new_directory_path}'.")

    return new_directory_path


def get_image_files(directory):
    # List to store the file paths
    image_files = []

    # Loop through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is an image with the specified extensions
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Add the file path to the list
                image_files.append(f"{root}/{file}")

    return image_files

def get_image_file_names(directory):
    # List to store the file paths
    image_files = []

    # Loop through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is an image with the specified extensions
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Add the file path to the list
                image_files.append(file)

    return image_files

def add_rounded_corners(image_path, output_path, corner_radius):
    # Open the input image
    image = Image.open(image_path).convert("RGBA")

    # Create a mask for rounded corners
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(0, 0), image.size], 
        corner_radius, 
        fill=255
    )

    # Apply the rounded corners mask to the image
    rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    # Save the resulting image
    rounded_image.save(output_path, format="PNG")
    print(f"Rounded corner image saved as {output_path}")


# Function to validate and store the input
def batch_genarate():
    global selected_integer
    global selected_folder_path
    input_value = int_entry.get()
    p = input_value.isdigit() and 1 <= int(float(input_value)) <= 100
    # Check if the input is a valid integer between 1 and 100
    if input_value.isdigit() and 1 <= int(float(input_value)) <= 100:
        selected_integer = int(input_value)
        # messagebox.showinfo("Success", f"Valid input: {selected_integer}")
    elif input_value == '':
        selected_integer = 20
    else:
        messagebox.showerror("Error", "Please enter a valid integer between 1 and 100.")
    
    if selected_folder_path == "" :
        messagebox.showerror("Error", "Select the Batch Folder first.")
    if  (p or selected_integer == 20) and selected_folder_path != '':
        image_files = get_image_files(selected_folder_path)
        image_file_names = get_image_file_names(selected_folder_path)
        out_folder_name = create_new_directory(selected_folder_path,f"Corner_Rounded_{selected_integer}")

        c = 0
        for path in image_files:
            # add_rounded_corners(path,)
            output_path = f"{out_folder_name}/{image_file_names[c]}"
            print(output_path)
            c = c + 1
            add_rounded_corners(path,output_path,selected_integer)
        messagebox.showinfo("Success", f"Cheack : {out_folder_name}")
        
        #Get all the images into array
        #Loop through it and save
        

    

# Function to browse and select a folder
def browse_folder():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory(title="Select the batch folder")
    if selected_folder_path:
        folder_label.configure(text=f"Batch Folder: {selected_folder_path}")



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x500")
root.resizable(False , False)
root.title("Batch Photo Corner Roundness Genarator")

#Top Image
top_frame = customtkinter.CTkFrame(root , fg_color="transparent")
top_frame.pack(side="top" , expand=True)
cover_image = customtkinter.CTkImage(dark_image=Image.open("Cover.png"),light_image=Image.open("Cover2.png") , size=(500,250))
my_lable = customtkinter.CTkLabel(top_frame , text="" , image=cover_image)
my_lable.pack(pady=0)

bottom_frame = customtkinter.CTkFrame(root,fg_color="transparent")
bottom_frame.pack(side="bottom" , fill="both", expand=True)


b1_frame = customtkinter.CTkFrame(bottom_frame,fg_color="transparent")

folder_label = customtkinter.CTkLabel(b1_frame, text="")
folder_label.pack(pady=4 , side='left', padx=20)

b1_frame.pack()


b1_frame = customtkinter.CTkFrame(bottom_frame,fg_color="transparent")
f_label = customtkinter.CTkLabel(b1_frame, text="Select the Folder First :")
f_label.pack(pady=4 , side='left', padx=20)
browse_button = customtkinter.CTkButton(b1_frame, text="Browse Folder", command=browse_folder)
browse_button.pack(pady=10 , side='left' ,padx=2)
b1_frame.pack()


b2_frame = customtkinter.CTkFrame(bottom_frame,fg_color="transparent")
instruction_label = customtkinter.CTkLabel(b2_frame, text="Corner Radius (1-100) : ")
instruction_label.pack(pady=10 , side='left' , padx=20)
int_entry = customtkinter.CTkEntry(b2_frame , placeholder_text="20")
int_entry.pack(pady=10 , side='left' , padx=2)
b2_frame.pack()


b3_frame = customtkinter.CTkFrame(bottom_frame,fg_color="transparent")
start_button = customtkinter.CTkButton(b3_frame,text="Start", command=batch_genarate )
start_button.pack(pady=10 , fill='both' ,expand=True)
b3_frame.pack()



root.mainloop()