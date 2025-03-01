# Pokémon Center Save Backup

## Overview
Pokémon Center Save Backup is a tool designed to help users backup their Pokémon save files easily. With a Pokémon Center-themed GUI built using PyQt5, the tool scans a selected folder for Pokémon save files, allows users to choose files to back up, and supports uploading to GitHub. It also provides an option to export selected saves as a ZIP file.

## Features
- **Folder Selection:** Select a directory to scan for Pokémon save files.
- **File Filtering:** Detects save files with names containing "pokemon" or "pokémon" (case insensitive).
- **Manual File Selection:** If automatic detection fails, users can manually select a save file.
- **User Authentication:** Requires a username and password (hashed and stored securely).
- **Backup to GitHub:** Uploads selected save files to a user-specified GitHub repository.
- **Export as ZIP:** Saves selected files as a single ZIP archive, named `(username)-backup(date).zip`.
- **Persistent Settings:** Remembers the last selected folder for convenience.

## Installation
### Requirements
- Python 3.x
- PyQt5 (`pip install PyQt5`)
- bcrypt (`pip install bcrypt`)

### Clone the Repository
```sh
git clone https://github.com/goddardYYZ/PokemonSaveBackup.git
cd PokemonSaveBackup
```

### Run the Application
```sh
python main.py
```

## Usage
1. **Select a folder** containing Pokémon save files.
2. **Choose detected files** or manually select a file if necessary.
3. **Enter your username and password** for authentication.
4. **Click "Backup Selected Saves"** to upload the files to GitHub.
5. **Click "Export as ZIP"** to save selected files as a compressed archive.

## Contributing
Feel free to submit pull requests or report issues on GitHub.

## License
This project is licensed under the MIT License.

