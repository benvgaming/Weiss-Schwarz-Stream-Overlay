# Weiss-Schwarz-Stream-Overlay

![image](https://github.com/user-attachments/assets/2a6909b5-74c7-43c5-93f2-3846dc888a8e)

## Purpose and Main Functionalities

This codebase is a Python project that creates a stream overlay for the Weiss Schwarz card game. The overlay displays player names, current clock, level, and the sets they are playing. It includes functionality to add and remove damage, and to load card images based on input card codes.

## Codebase Structure

The main script is `WS_Stream_Overlay.py`, which uses the `tkinter` library to create the GUI. The script defines an `Application` class that sets up the main window and two `Player` frames, each representing a player in the game. The `Player` class handles the player's name, set code, key card image, and damage/level tracking.

## Running the Codebase

To run the codebase, you need to have Python installed on your system. Additionally, the following dependencies are required:
- `tkinter`
- `Pillow`

You can install the dependencies using pip:
```
pip install tkinter Pillow
```

After downloading both the WS_Stream_Overlay.zip AND WS_Stream_Overlay_Images.zip files, extract both of them into the same folder. In the end, it should look like this:

![image](https://github.com/user-attachments/assets/b86d51ff-4f6f-4828-bcf0-51f130b432db)

To start the overlay, run the `WS_Stream_Overlay.py` script:
```
python WS_Stream_Overlay.py
```

The script that loads the card image only works for Japanese cards and English exclusive sets. If you input anything else or an invalid card code, the script will default back to the Shiyoko image. The function that loads the hex-image might take a while because it has to cycle through all the possible URL configurations on the English website and check if they're valid or not.

Please let me know if you encounter any issues.
