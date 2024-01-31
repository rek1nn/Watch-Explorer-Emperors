from Emperors_GUI.build.gui import MyGUI
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


class MyApp(MyGUI):
    def __init__(self, items_total=4) -> None:
        super().__init__()
        self.items_total = items_total
        self.frames_names = ["first_item", "second_item", "third_item", "fourth_item"]
        # Widget for item name
        self.entry_item = ctk.CTkEntry(self, 
                                  placeholder_text="Enter the name of watches...",
                                  placeholder_text_color="#e1f2ff",
                                  width=475,
                                  height=35,
                                  fg_color="#333741",
                                  text_color="#e1f2ff",
                                  font=("Arial",17))
        self.entry_item.place(relx=0.5, rely=0.3, anchor="center")
        # Image for search button
        self.path = os.getcwd()
        self.img = os.path.join(self.path,"image_4.png")
        self.pil_img = Image.open(self.img)
        self.photo_img = CTkImage(self.pil_img)
        # Button to get info about item
        self.search_button = ctk.CTkButton(self,
                                    text="",
                                    image=self.photo_img,
                                    width=30,
                                    height=35,
                                    command=self.submit_item,
                                    fg_color="#adbfd2")
        self.search_button.place(relx=0.737, rely=0.3, anchor="w")
        # Button for next page
        self.next_page_button = ctk.CTkButton(self,
                                    text="NEXT PAGE",
                                    width=75,
                                    height=35,
                                    command=self.load_next_page)
        self.next_page_button.place(relx=0.936, rely=0.95, anchor="center")

        # Frame for item image
        self.items_frame = None

    def submit_item(self):
        item_name = self.entry_item.get()
        self.get_info(item_name)

    def get_info(self, item_name):
        try:
            """Search for item and get info about it"""
            item = chrono24.query(item_name)
            item_info = list(item.search(limit=self.items_total))

            if item_info:
                self.process_searching(item_info)
                return item_info
            else:
                raise ValueError("No item info available, try again")
        except Exception as e:
            print(e)

    def process_searching(self, info):
        if self.items_frame:
            self.items_frame.destroy()

        """----------------Pool for searching----------------"""
        # Search field
        self.items_frame = ctk.CTkFrame(self, fg_color="#898989", width=950, height=300)
        self.items_frame.place(relx=0.5, rely=0.63, anchor="center")
        # First small frame 
        self.first_item_frame = ctk.CTkFrame(self.items_frame, fg_color="#898989", width=237, height=340)
        self.first_item_frame.place(relx=0, rely=0, anchor="nw")

        # Second small frame
        self.second_item_frame = ctk.CTkFrame(self.items_frame, fg_color="#898989", width=237, height=340)
        self.second_item_frame.place(relx=0.25, rely=0, anchor="nw")

        # Third small frame
        self.third_item_frame = ctk.CTkFrame(self.items_frame, fg_color="#898989", width=237, height=340)
        self.third_item_frame.place(relx=0.5, rely=0, anchor="nw")

        # Fourth small frame
        self.fourth_item_frame = ctk.CTkFrame(self.items_frame, fg_color="#898989", width=237, height=340)
        self.fourth_item_frame.place(relx=0.75, rely=0, anchor="nw")

        """----------------Processing photo adition----------------"""
        img_urls = []
        for i, url in enumerate(info[-4:]):
            img_url = url.get("image_urls", [])[0] if url.get("image_urls") else None

            if img_url:
                img_urls.append(img_url)
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                response = requests.get(img_url, headers=headers, stream=True)
                response.raise_for_status()

                with Image.open(BytesIO(response.content)) as image:
                    image.thumbnail((175, 175))  # resize image
                    photo = ImageTk.PhotoImage(image)

                current_frame = getattr(self, f"{self.frames_names[i]}_frame")

                # Create a label for each frame
                item_photo = tk.Label(current_frame, image=photo)
                item_photo.image = photo  # Keep a reference to avoid garbage collection
                item_photo.pack()

        """----------------Processing photo adition----------------"""
        for i, item in enumerate(info[-4:]):
            current_frame = getattr(self, f"{self.frames_names[i]}_frame")

            self.open_website_btn = ctk.CTkButton(current_frame, 
                                                text="Review", 
                                                command=lambda url=item.get("url"): self.open_website(url),
                                                height=34,
                                                width=53)
            self.open_website_btn.pack()

            if len(item.get("title")) > 35:
                short_tile = item.get("title")[:35] + "...."
                title_label = ctk.CTkLabel(current_frame, text=short_tile)
                title_label.pack()
            else:
                title_label = ctk.CTkLabel(current_frame, text=item.get("title"))
                title_label.pack()


            if len(item.get("description", "")) > 35:
                short_description = str(item.get("description")[:35] + "...")
                description_label = ctk.CTkLabel(current_frame, text=short_description)
                description_label.pack()
            else:
                description_label = ctk.CTkLabel(current_frame, text=item.get("description", ""))
                description_label.pack()

            if item.get("price") == "null":
                price_label = ctk.CTkLabel(current_frame, text="Price on request")
                price_label.pack()
            else:
                price_label = ctk.CTkLabel(current_frame, text=item.get("price"))
                price_label.pack()
        
    def open_website(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"An unexpected error occured! {e}")

    def load_next_page(self):
        # Generate 4 news items
        self.items_total += 4

        if self.items_frame:
            self.items_frame.destroy()

        # Run chunk again
        self.get_info(self.entry_item.get())

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()