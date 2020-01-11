# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox, colorchooser
#from dialogs import *
from cells import *
import random


class MyApp:
    def __init__(self, parent):
        self.color_bg = 'grey'
        self.live_cell_color = 'black'
        self.cell_color = 'white'
        self.play = False
        self.x = 0
        self.y = 0 
        self.template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        
        self.squares = []
        self.square = None
        self.parent = parent
        self.drawWidgets()

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=500 , height=500)
        self.canvas = Canvas(self.parent, width=500, height=500, bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        button_start = Button(self.container, text="Start", command=self.start)
        button_start.pack(side=LEFT)
        button_new = Button(self.container, text="Nový", command=self.new)
        button_new.pack(side=LEFT)

        button_random = Button(self.container, text="Náhodně", command=self.random)
        button_random.pack(side=RIGHT)
        button_pulsar = Button(self.container, text="Pulzor", command=self.pulsar)
        button_pulsar.pack(side=RIGHT)
        button_oscillators = Button(self.container, text="Oscilátory", command=self.oscillators)
        button_oscillators.pack(side=RIGHT) 
        button_still = Button(self.container, text="Stálý život", command=self.still)
        button_still.pack(side=RIGHT)

        self.container.pack(fill=BOTH)

        self.canvas.focus_set()

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Menu', menu=filemenu)
        filemenu.add_command(label='Konec', command=self.parent.destroy)
        canvasmenu = Menu(menu)
        menu.add_cascade(label='Barvy', menu=canvasmenu)
        canvasmenu.add_command(label='Barva plátna', command=self.change_bg)
        canvasmenu.add_command(label='Barva polí', command=self.change_cell_color)
        canvasmenu.add_command(label='Barva živých buňek', command=self.change_live_cell_color)


    def start(self):
        self.play = True
        self.game()

    def new(self):
        self.play = False
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])) :
                self.template[i][j] = 0
        self.create_game()

    def change_bg(self):  
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.canvas['bg'] = self.color_bg

    def change_live_cell_color(self):
        self.live_cell_color = colorchooser.askcolor(color=self.live_cell_color)[1]
        pass

    def change_cell_color(self):
        self.cell_color = colorchooser.askcolor(color=self.cell_color)[1]
        pass
        

    def clear_canvas(self):
        self.canvas.delete("all")

    def redraw_canvas(self):
        self.clear_canvas()
        for square in self.squares:
            square.draw(self.canvas)

    def create_game(self):
        self.squares = []
        self.square = None
        self.x = 0
        self.y = 0
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])): 
                if self.template[i][j] == 0:
                    self.square = Build(self.x, self.y)
                if self.template[i][j] == 1:
                    self.square = LiveCell(self.x, self.y)
                self.squares.append(self.square)
                self.x += DEFAULT_CONFIG["side"]
            self.y += DEFAULT_CONFIG["side"]
            self.x -= DEFAULT_CONFIG["side"] * len(self.template[i])
        self.redraw_canvas()

    def game(self):
        new_template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])):
                neighborhood = 0
                for a in range(3):
                    for b in range(3):
                        if ((j-1+b) < len(self.template[i])) and ((j-1+b) >= 0) and ((i-1+a) < len(self.template)) and ((i-1+a) >= 0):
                            if self.template[i-1+a][j-1+b] == 1:
                                neighborhood += 1
                if self.template[i][j] == 1:
                    if neighborhood < 3:
                        new_template[i][j] = 0
                    if neighborhood == 3 or neighborhood == 4:
                        new_template[i][j] = 1
                    if neighborhood > 4:
                        new_template[i][j] = 0
                if self.template[i][j] == 0:
                    if neighborhood == 3:
                        new_template[i][j] = 1
                    else:
                        new_template[i][j] = 0
        self.template = new_template
        self.create_game()

                    

    def on_button_press(self, event):
        if self.play:
            pass
        else:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasx(event.y)
            point = Point(self.start_x, self.start_y)
            for s in self.squares:
                if s.detect_cursor(point): 
                    self.square = s 
                    if self.square.fill_color == "white":
                        self.square.fill_color = "black"

                    elif self.square.fill_color == "black":
                        self.square.fill_color = "white"
            self.redraw_canvas()

    def still(self):
        self.template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
            [0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
            [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        self.create_game()

    def oscillators(self):
        self.template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        self.create_game()

    def pulsar(self):
        self.template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        self.create_game()

    def random(self):
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])):
                self.template[i][j] = random.randrange(0, 2)
                print = random.randrange(0, 2)
        self.create_game()


root = Tk()
myapp = MyApp(root)
myapp.create_game()
root.mainloop()
