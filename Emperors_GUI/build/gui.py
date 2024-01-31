import tkinter as tk
import customtkinter as ctk
from tkinter import Canvas, PhotoImage
from customtkinter import CTk, CTkImage
from pathlib import Path
import chrono24
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import os


class MyGUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.current_path = os.getcwd()
        self.path = os.path.join(self.current_path, r"Emperors_GUI\build\assets\frame0")
        self.ASSETS_PATH = Path(__file__).parent / Path(self.path)
        self.setup_ui()

    def setup_ui(self):
        self.geometry("1000x550")
        self.configure(bg="#56465a")

        self.canvas = Canvas(
            self,
            bg="#C0C0C0",
            height=550,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))

        self.load_image()

        self.resizable(False, False)

    def load_image(self):
        self.canvas.create_image(500.0, 275.0, image=self.image_1)
        self.canvas.create_image(160.0, 67.0, image=self.image_5)
        self.canvas.create_image(318.0, 56.99999483597253, image=self.image_6)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)


    
if __name__ == "__main__":
    app = MyGUI()
    app.mainloop()
