from tkinter import *
from tkinter import ttk
from configparser import ConfigParser
import requests
from PIL import Image, ImageTk
from io import BytesIO

config = ConfigParser()
config.read('config.ini')

SEARCH_URL = "http://www.omdbapi.com/?s={film}&apikey={key}"

class Controlator(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=400, height=550)
        self.pack_propagate(0)

        self.searcher = Searcher(self, self.busca)
        self.searcher.pack(side=TOP, fill=X, expand=True)

        self.film = Film(self)
        self.film.pack(side=TOP, fill=X, expand=True)

    def busca(self, peli):
        print('por aquí pasa')
        url = SEARCH_URL.format(film=peli, key=config['OMDB']['API_KEY'])
        results = requests.get(url)
        self.first_film = None
        if results.status_code == 200:
            films = results.json()
            if films.get("Response") == 'True':
                if len(films.get("Search")) > 0:
                    self.first_film = films.get("Search")[0]
                    self.film.the_film = self.first_film

class Searcher(ttk.Frame):
    first_film = None

    def __init__(self, parent, command):
        ttk.Frame.__init__(self, parent)

        lblSearcher = ttk.Label(self, text="Film:")
        self.ctrSearcher = StringVar()
        txtSearcher = ttk.Entry(self, width=30, textvariable=self.ctrSearcher)
        btnSearcher = ttk.Button(self, text="Search", command=lambda: command(self.ctrSearcher.get()))
        
        lblSearcher.pack(side=LEFT)
        txtSearcher.pack(side=LEFT)
        btnSearcher.pack(side=LEFT)


class Film(ttk.Frame):
    title = ''
    year = ''
    _type = ''
    urlImg = ''
    def __init__(self, parent, film=None):
        ttk.Frame.__init__(self, parent)
        if film:
            self.the_film = film

        self.lblTitle = ttk.Label(self, text=self.title)
        self.lblYear = ttk.Label(self, text=self.year)
        self.lblType = ttk.Label(self, text=self._type)
        self.photo = None
        self.lblImg = Label(self)

        self.lblTitle.pack(side=TOP) 
        self.lblYear.pack(side=TOP) 
        self.lblType.pack(side=TOP)
        self.lblImg.pack(side=TOP)

    @property 
    def the_film(self):
        return {'Title': self.title, 'Year': self.year, 'Type': self._type, 'Poster': self.urlImg}

    @the_film.setter
    def the_film(self, value):
        self.title = value.get('Title')
        self.year = value.get('Year')
        self._type = value.get('Type')
        self.urlImg = value.get('Poster')

        self.lblTitle.config(text=self.title)
        self.lblYear.config(text=self.year)
        self.lblType.config(text=self._type)

        if self.photo:
            del self.photo
            self.photo = None

        self.__set_image()

    def __set_image(self):
        if not self.urlImg or self.urlImg == "N/A":
            return

        r = requests.get(self.urlImg)
        if r.status_code == 200:
            bimage = r.content
            image = Image.open(BytesIO(bimage))
            self.photo = ImageTk.PhotoImage(image)

            self.lblImg.config(image=self.photo)
            self.lblImg.image = self.photo



