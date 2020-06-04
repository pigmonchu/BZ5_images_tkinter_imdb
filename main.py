from tkinter import *
from tkinter import ttk

import cinema

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Busca peliculas')
        s = cinema.Controlator(self)
        s.pack(side=TOP, fill=BOTH)


    def main(self):
        self.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.main()

