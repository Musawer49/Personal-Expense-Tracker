import os 
import shutil 

# Folder to Organize
folder_path = r"C:\Users\Musaw\OneDrive\Desktop\Test Folder" 

# File extensions and their destination folders
folders = { ".mp4": "Videos", 
        ".mkv": "Videos", 
        ".avi": "Videos", 
        ".mov": "Videos", 
        ".jpg": "Images", 
        ".jpeg": "Images", 
        ".png": "Images", 
        ".mp3": "Audios", 
        ".wav": "Audios", 
        ".pdf": "Documents", 
        ".docx": "Documents", 
        ".txt": "Documents" 
        } 

# Get all files in the folder
files = os.listdir(folder_path) 

# Process each files
for file in files:
    file_path = os.path.join(folder_path, file)

    if os.path.isfile(file_path):
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()

        if file_extension in folders:

            destination_folder = os.path.join(folder_path, folders[file_extension])

            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)

            destination = os.path.join(destination_folder, file)

            shutil.move(file_path, destination)

            print(f"{file} moved to {folders[file_extension]} folder.")

