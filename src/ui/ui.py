from .menu import MyMenu
from ..steganography.utils import *
from . import tk
from .controler import TkinterControler


class MyTk(tk.Tk):

    tempRoot = "temp/temporaly.png"
    outputRoot = "outputs/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.original_image = None
        # Window size
        self.maxsize(800, 600)
        self.minsize(800, 600)

        # Controler
        self.controler = TkinterControler(self)

        # Menu
        menu = MyMenu(self)
        self.config(menu=menu)

        center_frame = tk.Frame(self, background="grey")
        label_title = tk.Label(
            center_frame,
            text="Steganography",
            font=("Helvetica", 20),
            background="grey",
            foreground="white",
        )

        button_encode = tk.Button(
            center_frame,
            text="Encode",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.controler.encode,
        )

        ### Left frame
        left_frame = tk.Frame(center_frame, background="white", width=300)
        left_frame.pack_propagate(False)

        self.image_label = tk.Label(left_frame, background="white")

        button_choose_image = tk.Button(
            left_frame,
            text="Choose Image",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.controler.load_image,
        )

        ### Right frame
        right_frame = tk.Frame(center_frame, width=300, background="white")
        right_frame.pack_propagate(False)
        button_choose_file = tk.Button(
            right_frame,
            text="Choose file",
            font=("Helvetica", 10),
            background="grey",
            foreground="white",
            width=15,
            command=self.controler.load_file,
        )
        self.file_selected_label = tk.Label(right_frame, background="white")

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
        self.mainloop()
