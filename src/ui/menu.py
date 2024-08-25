from . import tk


class MyMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        filemenu = tk.Menu(self, tearoff=0)

        filemenu.add_command(label="Decode file", command=parent.controler.decode)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        self.add_cascade(label="Help", menu=helpmenu)

        parent.config(menu=self)

    def about(self):
        tk.messagebox.showinfo(
            "About", "Steganography, oculta tus archivos en imagenes"
        )
