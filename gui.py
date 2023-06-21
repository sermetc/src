#! /usr/bin/env python3.11

import customtkinter
import tkinter
import image_gen
import requests
from PIL import Image
from io import BytesIO

class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.image = customtkinter.CTkImage(light_image=Image.open("./assets/dalle.png"),size=(500,500))
        self.image_label = customtkinter.CTkLabel(master=self, image=self.image, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def set_new_image(self, image):
        self.image.configure(light_image=Image.open(image))
        self.image_label.configure(image=self.image)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("DALL-E Python")
        self.geometry("1080x720")
        self.minsize(1080, 720)

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.generated_image_url = ""
        self.variation_source_image = ""
        self.IMAGE_WIDTH = "512"

        self.generate_button_state = "normal"

        self.prompt_entry = customtkinter.CTkEntry(master=self, width=500)
        self.prompt_entry.grid(row=2, column=0, sticky='ew', padx=30)

        self.generate_button = customtkinter.CTkButton(master=self, command=self.generate_image, text="Generate", state=self.generate_button_state)
        self.generate_button.grid(row=2, column=1)

        self.create_variation_button = customtkinter.CTkButton(master=self, command=self.create_variation, text="Variation", state=self.generate_button_state)
        self.create_variation_button.grid(row=1, column=2, sticky='s')

        self.save_button = customtkinter.CTkButton(master=self, command=self.save_image, text="Save")
        self.save_button.grid(row=2, column=2)

        self.image_frame = ImageFrame(master=self)
        self.image_frame.grid(row=0, column=0, padx=30, pady=30, rowspan=2, sticky='nsew')

        self.quality_options = customtkinter.CTkOptionMenu(master=self, values=["256x256", "512x512", "1024x1024"], command=self.set_quality)
        self.quality_options.set("512x512")
        # self.quality_options.place(relx=1, rely=0, anchor=customtkinter.NE)
        self.quality_options.grid(row=0, column=2, padx=30, pady=30, sticky='ne')
        
    def set_quality(self, choice):
        if choice == "256x256":
            self.IMAGE_WIDTH = "256"
            print("here")
        elif choice == "512x512":
            self.IMAGE_WIDTH = "512"
        elif choice == "1024x1024":
            self.IMAGE_WIDTH = "1024"
        else:
            self.IMAGE_WIDTH = "512"

    def generate_image(self):
        if self.prompt_entry.get() != "" and len(self.prompt_entry.get()) > 2:
            self.generate_button_state = "disabled"
            self.generated_image_url = image_gen.create_image(self.prompt_entry.get(), size=self.IMAGE_WIDTH)
            self.load_image_from_generation(self.generated_image_url)
            self.generate_button_state = "normal"

    def create_variation(self):
        self.generate_button_state = "disabled"
        self.save_image()
        self.generated_image_url = image_gen.variate_existing_image_from_path(self.variation_source_image, size=self.IMAGE_WIDTH)
        self.load_image_from_generation(self.generated_image_url)
        self.generate_button_state = "normal"
    
    def load_image_to_front(self):
        pass

    def load_image_from_generation(self, url):
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        self.image_frame.set_new_image(image_bytes)

    def save_image(self):
        if self.generated_image_url:
            dialog = customtkinter.CTkInputDialog(text="Enter a name:", title="Saving...")
            if dialog:
                self.variation_source_image = image_gen.save_generated_image_from_url_with_name(self.generated_image_url, dialog.get_input())                

if __name__ == "__main__":
    app = App()
    app.mainloop()
