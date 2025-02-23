import os
import subprocess

def get_path(location):
    """Returns the absolute path for common system folders."""
    system_paths = {
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "music": os.path.join(os.path.expanduser("~"), "Music"),
        "videos": os.path.join(os.path.expanduser("~"), "Videos"),
        "onedrive": os.path.join(os.path.expanduser("~"), "OneDrive"),
        "appdata": os.path.join(os.path.expanduser("~"), "AppData"),
        "localappdata": os.path.join(os.path.expanduser("~"), "AppData", "Local"),
        "programfiles": os.environ.get("ProgramFiles", "C:\\Program Files"),
        "programfilesx86": os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        "rdisk": "R:\\",
        "cdrive": "C:\\",
        "ddrive": "D:\\"
    }
    return system_paths.get(location.lower(), location)  # Return mapped path or original location

def execute_command(action, location, name):
    """Executes file and folder operations like creating, deleting, opening, and finding files or directories."""
    path = os.path.join(get_path(location), name)

    if action.lower() == "create":
        if "." in name:  # Check if it's a file (e.g., test.txt)
            command = f'type NUL > "{path}"'  # Creates an empty file
        else:
            command = f'mkdir "{path}"'  # Creates a folder
    elif action.lower() == "delete":
        if os.path.isdir(path):
            command = f'rd /s /q "{path}"'  # Deletes folder
        else:
            command = f'del /f /q "{path}"'  # Deletes file
    elif action.lower() == "open":
        if os.path.exists(path):
            subprocess.run(f'explorer "{path}"', shell=True)  # Opens file/folder in Explorer
            print(f'Opened: {path}')
            return
        else:
            print(f'Error: {path} does not exist.')
            return
    elif action.lower() == "find":
        search_command = f'explorer /select,"{path}"'  # Highlights file in Explorer
        subprocess.run(search_command, shell=True)
        print(f'Finding: {path}')
        return
    else:
        print("Invalid action. Use 'create', 'delete', 'open', or 'find'.")
        return

    subprocess.run(command, shell=True)
    print(f'Executed: {command}')

