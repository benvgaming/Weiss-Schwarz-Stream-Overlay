import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps
import urllib.request
import os


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weiss Schwarz Damage Overlay")

        player1_lbl = tk.Label(self, text="Player 1", height=2)
        player1_lbl.grid(row=0, column=0)
        frame = Player1(self)
        frame.grid(row=1, column=0)

        player2_lbl = tk.Label(self, text="Player 2", height=2)
        player2_lbl.grid(row=0, column=1)
        frame = Player2(self)
        frame.grid(row=1, column=1)


class Player1(ttk.Frame):
    clock = 0
    level = 0
    playername = ""
    playerset = ""
    display_name = str(playername) + " (" + str(playerset) + ")"
    y_position_name = 0.492
    x_position_name = 0.407
    display_font = "Calibri Bold"
    font_size = 16

    def __init__(self, parent):
        super().__init__(parent)

        # Playername
        self.lbl = ttk.Label(self, text="Input Name")
        self.lbl.grid(row=0, column=0)
        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=1)
        self.entry.bind("<Return>", self.save_playername)
        self.entry_btn = ttk.Button(self, text="Add", command=self.save_playername)
        self.entry_btn.grid(row=0, column=2)

        # Playerset
        self.lbl3 = ttk.Label(self, text="Input Setcode")
        self.lbl3.grid(row=1, column=0)
        self.entry2 = ttk.Entry(self)
        self.entry2.grid(row=1, column=1)
        self.entry2.bind("<Return>", self.save_playerset)
        self.entry_btn2 = ttk.Button(self, text="Add", command=self.save_playerset)
        self.entry_btn2.grid(row=1, column=2)

        # Player Key Card
        self.lbl_key_card = ttk.Label(self, text="Input Card ID (e.g.: HOL/W104-070)")
        self.lbl_key_card.grid(row=2, column=0)
        self.entry_key_card = ttk.Entry(self)
        self.entry_key_card.grid(row=2, column=1)
        self.entry_key_card.bind("<Return>", self.save_key_card)
        self.entry_btn_key_card = ttk.Button(self, text="Load Card", command=self.save_key_card)
        self.entry_btn_key_card.grid(row=2, column=2)

        # Adding Damage
        self.entry_btn3 = tk.Button(self, text="+1 Damage", command=self.add_damage, height=2)
        self.entry_btn3.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Removing Damage
        self.entry_btn4 = tk.Button(self, text="-1 Damage", command=self.remove_damage, height=2)
        self.entry_btn4.grid(row=4, column=0, columnspan=3, sticky="ew")

        # Creating the Image for the Stream Overlay
        self.canvas = tk.Canvas(self, bg="#00ff00", width=500, height=199)
        self.background = tk.PhotoImage(file="./player_left/00.png")
        self.playerbg = self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        self.set_image = tk.PhotoImage(file="./default_player_hex.png")
        self.playersetimg = self.canvas.create_image(52, 23, anchor="nw", image=self.set_image)
        self.canvas.grid(row=5, column=0, columnspan=3)

        # Display Name Label
        self.lbl4 = tk.Label(self, text=self.display_name, bg="black", fg="white", font=(self.display_font, self.font_size))
        self.lbl4.place(relx=self.x_position_name, rely=self.y_position_name, anchor="nw")

        # Reset Clock/Level
        self.entry_btn5 = tk.Button(self, text="New Game", command=self.new_game, height=2)
        self.entry_btn5.grid(row=6, column=0, columnspan=3, sticky="ew")

    def save_playername(self, event=None):
        self.playername = str(self.entry.get())
        self.display_name = str(self.playername) + " (" + str(self.playerset) + ")"
        self.lbl4.configure(text=self.display_name)

    def save_playerset(self, event=None):
        self.playerset = str(self.entry2.get().upper())
        self.display_name = str(self.playername) + " (" + str(self.playerset) + ")"
        self.lbl4.configure(text=self.display_name)

    def add_damage(self):
        if self.clock == 6:
            self.clock -= 6
            self.level += 1
        elif self.clock < 6:
            self.clock += 1
        if self.level >= 4:
            self.clock = 0
            self.level = 4
        self.new_img = tk.PhotoImage(file="./player_left/" + str(self.level) + str(self.clock) + ".png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def remove_damage(self):
        if self.clock > 0:
            self.clock -= 1
        elif self.clock == 0:
            self.clock += 6
            self.level -= 1
        if self.level < 0:
            self.clock = 0
            self.level = 0
        self.new_img = tk.PhotoImage(file="./player_left/" + str(self.level) + str(self.clock) + ".png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def new_game(self):
        self.clock = 0
        self.level = 0
        self.new_img = tk.PhotoImage(file="./player_left/00.png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def save_key_card(self, event=None):
        try:
            card_code = str(self.entry_key_card.get().lower())
            char_remov = ["/", "-"]
            for char in char_remov:
                card_code = card_code.replace(char, "_")

            if len(card_code) > 0:
                set_initial = str(card_code[0])
                first_underscore = card_code.find("_")
                second_underscore = card_code.find("_", first_underscore + 1)
                set_code = str(card_code[:second_underscore])
                card_id = str(card_code[first_underscore + 1:])

                jp_card = f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/{set_initial}/{set_code}/{card_code}.png"
                normal_pattern_en = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/{set_initial}/{set_code}/{card_code.upper()}.png"
                sds_2_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/SDS2/{card_code.upper()}.png"
                ggst_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/GGST/{card_id.upper()}.png"
                aotfs_td_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/AOTFS/TD/{card_code.upper()}.png"
                aotfs_bp_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/AOTFS/BP/{card_code.upper()}.png"
                rwby1_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/RWBY/{card_code.upper()}.png"
                rwby2_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/RWBY/{card_id.upper()}.png"
                atla_td_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/ATLA/TD/{card_code.upper()}.png"
                atla_bp_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/ATLA/BP/{card_code.upper()}.png"

                list_of_urls = []
                list_of_urls.extend((jp_card, normal_pattern_en, sds_2_card, ggst_card, aotfs_td_card, aotfs_bp_card, rwby1_card, rwby2_card, atla_td_card, atla_bp_card))

                for url in list_of_urls:
                    try:
                        urllib.request.urlretrieve(url, "player_left.png")
                        break
                    except:
                        continue

                def make_hexagonal(im):
                    mask = Image.new("L", im.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.regular_polygon(bounding_circle=(im.width // 2, im.width // 2, im.width // 2), n_sides=6, rotation=30, fill=255)
                    out = ImageOps.fit(im, mask.size, centering=(0, 0))
                    out.putalpha(mask)
                    return out

                with Image.open("./player_left.png") as im:
                    adjust_size = (400, 559)
                    im = im.resize(adjust_size)
                    im = im.convert("RGBA")
                    im = im.crop((0, 0, im.width, im.width))
                    hex_img = make_hexagonal(im)
                    hex_img.save("./player_left_hex.png")
                    adjust_size = (148, 148)
                    hex_img = hex_img.resize(adjust_size)
                    hex_img.save("./player_left_hex.png")
                    os.remove("./player_left.png")

                self.hex_img = tk.PhotoImage(file="./player_left_hex.png")
                self.canvas.imgref = self.hex_img
                self.canvas.itemconfig(self.playersetimg, image=self.hex_img)

        except:
            self.hex_img = tk.PhotoImage(file="./default_player_hex.png")
            self.canvas.imgref = self.hex_img
            self.canvas.itemconfig(self.playersetimg, image=self.hex_img)


class Player2(ttk.Frame):
    clock = 0
    level = 0
    playername = ""
    playerset = ""
    display_name = str(playername) + " (" + str(playerset) + ")"
    y_position_name = 0.492
    x_position_name = 0.592
    display_font = "Calibri Bold"
    font_size = 16

    def __init__(self, parent):
        super().__init__(parent)

        # Playername
        self.lbl = ttk.Label(self, text="Input Name")
        self.lbl.grid(row=0, column=0)
        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=1)
        self.entry.bind("<Return>", self.save_playername)
        self.entry_btn = ttk.Button(self, text="Add", command=self.save_playername)
        self.entry_btn.grid(row=0, column=2)

        # Playerset
        self.lbl3 = ttk.Label(self, text="Input Setcode")
        self.lbl3.grid(row=1, column=0)
        self.entry2 = ttk.Entry(self)
        self.entry2.grid(row=1, column=1)
        self.entry2.bind("<Return>", self.save_playerset)
        self.entry_btn2 = ttk.Button(self, text="Add", command=self.save_playerset)
        self.entry_btn2.grid(row=1, column=2)

        # Player Key Card
        self.lbl_key_card = ttk.Label(self, text="Input Card ID (e.g.: HOL/W104-070)")
        self.lbl_key_card.grid(row=2, column=0)
        self.entry_key_card = ttk.Entry(self)
        self.entry_key_card.grid(row=2, column=1)
        self.entry_key_card.bind("<Return>", self.save_key_card)
        self.entry_btn_key_card = ttk.Button(self, text="Load Card", command=self.save_key_card)
        self.entry_btn_key_card.grid(row=2, column=2)

        # Adding Damage
        self.entry_btn3 = tk.Button(self, text="+1 Damage", command=self.add_damage, height=2)
        self.entry_btn3.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Removing Damage
        self.entry_btn4 = tk.Button(self, text="-1 Damage", command=self.remove_damage, height=2)
        self.entry_btn4.grid(row=4, column=0, columnspan=3, sticky="ew")

        # Creating the Image for the Stream Overlay
        self.canvas = tk.Canvas(self, bg="#00ff00", width=500, height=199)
        self.background = tk.PhotoImage(file="./player_right/00.png")
        self.playerbg = self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        self.set_image = tk.PhotoImage(file="./default_player_hex.png")
        self.playersetimg = self.canvas.create_image(300, 23, anchor="nw", image=self.set_image)
        self.canvas.grid(row=5, column=0, columnspan=3)

        # Display Name Label
        self.lbl4 = tk.Label(self, text=self.display_name, bg="white", fg="black", font=(self.display_font, self.font_size))
        self.lbl4.place(relx=self.x_position_name, rely=self.y_position_name, anchor="ne")

        # Reset Clock/Level
        self.entry_btn5 = tk.Button(self, text="New Game", command=self.new_game, height=2)
        self.entry_btn5.grid(row=6, column=0, columnspan=3, sticky="ew")

    def save_playername(self, event=None):
        self.playername = str(self.entry.get())
        self.display_name = str(self.playername) + " (" + str(self.playerset) + ")"
        self.lbl4.configure(text=self.display_name)

    def save_playerset(self, event=None):
        self.playerset = str(self.entry2.get().upper())
        self.display_name = str(self.playername) + " (" + str(self.playerset) + ")"
        self.lbl4.configure(text=self.display_name)

    def add_damage(self):
        if self.clock == 6:
            self.clock -= 6
            self.level += 1
        elif self.clock < 6:
            self.clock += 1
        if self.level >= 4:
            self.clock = 0
            self.level = 4
        self.new_img = tk.PhotoImage(file="./player_right/" + str(self.level) + str(self.clock) + ".png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def remove_damage(self):
        if self.clock > 0:
            self.clock -= 1
        elif self.clock == 0:
            self.clock += 6
            self.level -= 1
        if self.level < 0:
            self.clock = 0
            self.level = 0
        self.new_img = tk.PhotoImage(file="./player_right/" + str(self.level) + str(self.clock) + ".png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def new_game(self):
        self.clock = 0
        self.level = 0
        self.new_img = tk.PhotoImage(file="./player_right/00.png")
        self.canvas.imgref = self.new_img
        self.canvas.itemconfig(self.playerbg, image=self.new_img)

    def save_key_card(self, event=None):
        try:
            card_code = str(self.entry_key_card.get().lower())
            char_remov = ["/", "-"]
            for char in char_remov:
                card_code = card_code.replace(char, "_")

            if len(card_code) > 0:
                set_initial = str(card_code[0])
                first_underscore = card_code.find("_")
                second_underscore = card_code.find("_", first_underscore + 1)
                set_code = str(card_code[:second_underscore])
                card_id = str(card_code[first_underscore + 1:])

                jp_card = f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/{set_initial}/{set_code}/{card_code}.png"
                normal_pattern_en = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/{set_initial}/{set_code}/{card_code.upper()}.png"
                sds_2_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/SDS2/{card_code.upper()}.png"
                ggst_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/GGST/{card_id.upper()}.png"
                aotfs_td_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/AOTFS/TD/{card_code.upper()}.png"
                aotfs_bp_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/AOTFS/BP/{card_code.upper()}.png"
                rwby1_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/RWBY/{card_code.upper()}.png"
                rwby2_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/RWBY/{card_id.upper()}.png"
                atla_td_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/ATLA/TD/{card_code.upper()}.png"
                atla_bp_card = f"https://en.ws-tcg.com/wp/wp-content/images/cardimages/ATLA/BP/{card_code.upper()}.png"

                list_of_urls = []
                list_of_urls.extend((jp_card, normal_pattern_en, sds_2_card, ggst_card, aotfs_td_card, aotfs_bp_card, rwby1_card, rwby2_card, atla_td_card, atla_bp_card))

                for url in list_of_urls:
                    try:
                        urllib.request.urlretrieve(url, "player_right.png")
                        break
                    except:
                        continue

                def make_hexagonal(im):
                    mask = Image.new("L", im.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.regular_polygon(bounding_circle=(im.width // 2, im.width // 2, im.width // 2), n_sides=6, rotation=30, fill=255)
                    out = ImageOps.fit(im, mask.size, centering=(0, 0))
                    out.putalpha(mask)
                    return out

                with Image.open("./player_right.png") as im:
                    adjust_size = (400, 559)
                    im = im.resize(adjust_size)
                    im = im.convert("RGBA")
                    im = im.crop((0, 0, im.width, im.width))
                    hex_img = make_hexagonal(im)
                    hex_img.save("./player_right_hex.png")
                    adjust_size = (148, 148)
                    hex_img = hex_img.resize(adjust_size)
                    hex_img.save("./player_right_hex.png")
                    os.remove("./player_right.png")

                self.hex_img = tk.PhotoImage(file="./player_right_hex.png")
                self.canvas.imgref = self.hex_img
                self.canvas.itemconfig(self.playersetimg, image=self.hex_img)

        except:
            self.hex_img = tk.PhotoImage(file="./default_player_hex.png")
            self.canvas.imgref = self.hex_img
            self.canvas.itemconfig(self.playersetimg, image=self.hex_img)


if __name__ == "__main__":
    main()
