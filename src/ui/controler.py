from ..steganography.utils import *
import os
from tkinter import filedialog
from tkinter import messagebox, PhotoImage
from PIL import UnidentifiedImageError


class TkinterControler:
    def __init__(self, tk_ui: "MyTk") -> None:
        self.tk_ui = tk_ui

    def encode(self):
        if (
            self.tk_ui.image_label.cget("image")
            and self.tk_ui.file_selected_label.cget("text")
            and self.tk_ui.original_image
        ):

            file_path = self.tk_ui.file_selected_label.cget("text").split(": ")[1]
            output_path = self.tk_ui.outputRoot + "output.png"

            encode_message(self.tk_ui.original_image, file_path, output_path)
            messagebox.showinfo("Steganography", "File encoded successfully!")  # type: ignore

            # Reset values and delete temporatly image
            self.tk_ui.image_label.config(image="")
            self.tk_ui.image_label.image = None  # type: ignore
            self.tk_ui.file_selected_label.config(text="")
            self.tk_ui.image_label.text = None  # type: ignore
            os.remove(self.tk_ui.tempRoot)

        else:
            messagebox.showinfo("No image or file selected")  # type: ignore

    def decode(self):
        file_name = filedialog.askopenfilename(
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        try:
            decode_message(file_name)
            messagebox.showinfo("Steganography", "File decoded successfully!")  # type: ignore

        except ValueError:
            messagebox.showinfo("Steganography", "No message found in the image")  # type: ignore
        except UnidentifiedImageError:
            messagebox.showinfo("Steganography", "Debe ser de tipo imagen")  # type: ignore
        except Exception as e:
            print(type(e))
            messagebox.showinfo("Steganography", "Error en el decoder")  # type: ignore

    def load_image(self):
        file_name = filedialog.askopenfilename()
        self.tk_ui.original_image = file_name  # type: ignore
        resize_image(path=file_name, output_path=self.tk_ui.tempRoot)

        image_var = PhotoImage(file=self.tk_ui.tempRoot, width=200, height=200)

        self.tk_ui.image_label.config(image=image_var)
        self.tk_ui.image_label.image = image_var  # type: ignore

    def _load_file(self):
        file_name = filedialog.askopenfilename()
        file_name_format = file_name.split("/")[-1]
        self.tk_ui.file_selected_label.config(text=f"Archivo: {file_name_format}")
