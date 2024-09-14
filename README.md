# Weiss-Schwarz-Stream-Overlay

![image](https://github.com/user-attachments/assets/8dcf5e0e-57e5-4245-9dbf-66486271ba56)



My second ever python project. I tried my hand at making a little stream overlay for my friend Weissandchill for Weiss Schwarz that displays the Playername, current Clock and Level of the players and which sets they are playing. This is also the first time I've ever used tkinter, so don't expect too much please.

The images that display the clock and level have been made by Weissandchill.

Do not remove any of the folders/files and do not move the .exe into a different folder, the program will not work.

After downloading both the WS_Stream_Overlay.zip AND WS_Stream_Overlay_Images.zip files extract both of them into the same folder.
In the end it should look like this:

![image](https://github.com/user-attachments/assets/b86d51ff-4f6f-4828-bcf0-51f130b432db)


The script that loads the card image only works for japanese cards and english exclusive sets. If you input anything else or an invalid card code the script will default back to the shiyoko image.
The function that loads the hex-image might take a while, because it has to cycle through all the possible url configurations on the english website and check if they're valid or not.


Why are there 2 separate "New Game" buttons, 1 for each player?
Cuz this is the first time I've worked with classes in python and I couldn't work out how to reset with a single button, so I put the "New Game" button into the same class as each player.
If you know how I could do that please let me know and I'll try to update the Overlay.

The Shiyoko image is a placeholder until the user inputs a valid card code to load. Should the loading fail the program will default back to the Shiyoko.
I did not test every single image in the japanese card database, but the load should work if you input a valid card code. The exception might be some random very old cards.
If you encounter any problems please let me know.
