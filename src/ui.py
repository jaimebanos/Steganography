from re import I
from .steganography.utils import *
import tkinter
from tkinter import filedialog
from PIL import Image, UnidentifiedImageError
import os


class myTk(tkinter.Tk):

    tempRoot = "temp/temporaly.png"
    outputRoot = "outputs/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_image = None
        # Window size
        self.maxsize(800, 600)
        self.minsize(800, 600)

        center_frame = tkinter.Frame(self, background="grey")
        label_title = tkinter.Label(
            center_frame,
            text="Steganography",
            font=("Helvetica", 20),
            background="grey",
            foreground="white",
        )

        button_encode = tkinter.Button(
            center_frame,
            text="Encode",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.encode,
        )

        button_decode = tkinter.Button(
            center_frame,
            text="Decode",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.decode,
        )

        ### Left frame
        left_frame = tkinter.Frame(center_frame, background="white", width=300)
        left_frame.pack_propagate(False)

        self.image_label = tkinter.Label(left_frame, background="white")

        button_choose_image = tkinter.Button(
            left_frame,
            text="Choose Image",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.load_image,
        )

        ### Right frame
        right_frame = tkinter.Frame(center_frame, width=300, background="white")
        right_frame.pack_propagate(False)
        button_choose_file = tkinter.Button(
            right_frame,
            text="Choose file",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.load_file,
        )
        self.file_selected_label = tkinter.Label(right_frame, background="white")

        ### Packs
        center_frame.pack(padx=10, pady=10, expand=True, fill="both")
        label_title.pack(pady=10)

        ### Left packs
        left_frame.pack(padx=10, pady=30, fill="both", side="left")
        button_choose_image.pack(pady=10)
        self.image_label.pack(pady=10, padx=10, fill="both", expand=True)

        ### Right packs
        right_frame.pack(padx=10, pady=30, fill="both", side="right")
        button_choose_file.pack(pady=10)
        self.file_selected_label.pack(pady=10)

        button_encode.pack(pady=10, padx=10, side="bottom")
        button_decode.pack(pady=10, padx=10, side="bottom")
        self.mainloop()

    def load_image(self):

        file_name = filedialog.askopenfilename()
        self.original_image = file_name
        self._resize_image(file_name)

        image_var = tkinter.PhotoImage(file=self.tempRoot, width=200, height=200)

        self.image_label.config(image=image_var)
        self.image_label.image = image_var  # type: ignore

    def load_file(self):
        file_name = filedialog.askopenfilename()
        file_name_format = file_name.split("/")[-1]
        self.file_selected_label.config(text=f"Archivo: {file_name_format}")
        print(file_name)

    def _resize_image(self, path: str):
        base_width = 300
        img = Image.open(path)
        wpercent = base_width / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
        img.save(self.tempRoot)

    def encode(self):

        if (
            self.image_label.cget("image")
            and self.file_selected_label.cget("text")
            and self.original_image
        ):

            file_path = self.file_selected_label.cget("text").split(": ")[1]
            output_path = self.outputRoot + "output.png"

            encode_message(self.original_image, file_path, output_path)
            # decode_message(output_image_path, "test.py")
            tkinter.messagebox.showinfo("Steganography", "File encoded successfully!")  # type: ignore

            # Reset values and delete temporatly image
            self.image_label.config(image="")
            self.image_label.image = None  # type: ignore
            self.file_selected_label.config(text="")
            self.image_label.text = None  # type: ignore
            os.remove(self.tempRoot)

        else:
            tkinter.messagebox.showinfo("No image or file selected")  # type: ignore

    def decode(self):
        file_name = filedialog.askopenfilename(
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        try:
            decode_message(file_name)
            tkinter.messagebox.showinfo("Steganography", "File decoded successfully!")  # type: ignore

        except ValueError:
            tkinter.messagebox.showinfo("Steganography", "No message found in the image")  # type: ignore
        except UnidentifiedImageError:
            tkinter.messagebox.showinfo("Steganography", "Debe ser de tipo imagen")  # type: ignore
        except Exception as e:
            print(type(e))
            tkinter.messagebox.showinfo("Steganography", "Error en el decoder")  # type: ignore
