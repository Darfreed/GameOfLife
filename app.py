# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox, colorchooser
from dialogs import *
from cells import *
from tkinter.filedialog import askopenfile,asksaveasfile
import json
import random


class MyApp:
    def __init__(self, parent):
        self.color_fg = 'black'
        self.color_bg = 'grey'
        self.live_cell_color = 'black'
        self.cell_color = 'white'
        self.play = False
        self.x = 0
        self.y = 0 
        self.label_generation = None

        self.width = 20
        self.height = 20
        self.side = 25
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

        self.generation = 0
        self.squares = []
        self.square = None
        self.parent = parent
        self.drawWidgets()

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=len(self.template[0]) * DEFAULT_CONFIG["side"] , height=len(self.template) * DEFAULT_CONFIG["side"])
        self.canvas = Canvas(self.parent, width=len(self.template[0]) * DEFAULT_CONFIG["side"] , height=len(self.template) * DEFAULT_CONFIG["side"], bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        button_start = Button(self.container, text="Start", command=self.start)
        button_start.pack(side=LEFT)
        button_pause = Button(self.container, text="Pauza", command=self.pause)
        button_pause.pack(side=LEFT)
        button_new = Button(self.container, text="Nový", command=self.new)
        button_new.pack(side=LEFT)
        self.label_generation = Label(self.container, text=f"Generace: {self.generation}")
        self.label_generation.pack(side=RIGHT)

        self.container.pack(fill=BOTH)


        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Soubor', menu=filemenu)
        filemenu.add_command(label='Otevřít...',command=self.open_file) 
        filemenu.add_command(label='Uložit...',command=self.save_file)
         
        filemenu.add_command(label='Konec', command=self.parent.destroy)
        canvasmenu = Menu(menu)
        menu.add_cascade(label='Pole', menu=canvasmenu)
        canvasmenu.add_command(label='Velikost pole', command=self.w_params)
        canvasmenu.add_command(label='Barva polí', command=self.change_cell_color)
        canvasmenu.add_command(label='Barva živých buňek', command=self.change_live_cell_color)
        canvasmenu.add_command(label='Barva linek', command=self.change_outline_color)
        canvasmenu.add_command(label='Barva pozadí', command=self.change_bg)
        examplemenu = Menu(menu)
        menu.add_cascade(label='Ukázky', menu=examplemenu)
        examplemenu.add_command(label='Zátiší', command=self.still)
        examplemenu.add_command(label='Oscilátory', command=self.oscillators)
        examplemenu.add_command(label='Lodě', command=self.ships)
        examplemenu.add_command(label='Náhodně', command=self.random)
        menu.add_command(label='O programu',command=self.info)

    #uložení pole v souboru json
    def save_file(self):
        self.play = False
        filetypes = [('JavaScript Object Notation','*.json'),('Všechny soubory','*.*')]
        file = asksaveasfile(filetypes = filetypes, title = "Uložení souboru", initialdir = "./")
        #zapsání tříd do slovníku v json
        json_data = json.dumps({"height":self.height,"width":self.width,"side":self.side,"data":self.template})
        file.write(json_data)
        pass

    #otevření pole souboru json
    def open_file(self):
        self.play = False
        filetypes = [('Všechny soubory','*.*'),('JavaScript Object Notation','*.json')]
        file = askopenfile(filetypes = filetypes, title = "Otevření souboru")
        json_data = json.loads(file.read())
        #rozhození dat do tříd
        self.width = json_data["width"]
        self.height = json_data["height"]
        self.side = json_data["side"]
        self.template = json_data["data"]
        self.generation = 0
        self.create_game()
        pass

    #spusteni hry
    def start(self):
        if self.play:
            pass
        else:
            self.play = True
            self.loop()

    #vyčištění pole
    def new(self):
        self.generation = 0
        self.play = False
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])) :
                self.template[i][j] = 0
        self.create_game()
    
    #zastavení hry
    def pause(self):
        self.play = False
        self.loop()

    # změna barvy pozadí
    def change_bg(self):  
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.canvas['bg'] = self.color_bg

    #vytvoreni noveho pole
    def create_template(self):
        new_template = []
        for i in range(self.height):
            row = []
            for j in range(self.width) :
                row.append(0)
            new_template.append(row)
        return new_template

    #změna parametru pole
    def w_params(self):
        self.play = False
        self.generation = 0
        dialog = CellDialog(self.parent, self)
        self.parent.wait_window(dialog.top)
        DEFAULT_CONFIG["side"] = self.side
        self.template = self.create_template()
        self.create_game()

    #informace
    def info(self):
        self.play = False
        dialog = InfoDialog(self.parent)
        pass

    # změna barvy živých buněk - nefunguje
    def change_live_cell_color(self):
        DEFAULT_CONFIG["live_cell_color"] = colorchooser.askcolor(color=self.live_cell_color)[1]
        self.create_game()

    # změna barvy mrtvých buněk - nefunguje
    def change_cell_color(self):
        DEFAULT_CONFIG["fill"] = colorchooser.askcolor(color=self.cell_color)[1]
        self.create_game()

    # změna barvy linek
    def change_outline_color(self):
        DEFAULT_CONFIG["outline"] = colorchooser.askcolor(color=self.cell_color)[1]
        self.create_game()

    # vyčištění plátna
    def clear_canvas(self):
        self.canvas.delete("all")

    # překreslení plátna
    def redraw_canvas(self):
        self.clear_canvas()
        for square in self.squares:
            square.draw(self.canvas)

    # výpis generací
    def generations(self):
        self.label_generation.config(text=f"Generace: {self.generation}")

    # vytvoření hry
    def create_game(self):
        self.squares = []
        self.square = None
        self.x = 0
        self.y = 0
        #procházení polí v template
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

    # funkce hry
    def game(self):
        new_template = self.create_template()
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])):
                # počítání živých buněk v poli 3x3 kolem aktulání buňky
                neighborhood = 0
                for a in range(3):
                    for b in range(3):
                        # pro nekonečnou plochu
                        if (i-1+a) > len(self.template)-1:
                            x = 0
                        elif (i-1+a) < 0:
                            x = len(self.template)-1
                        else:
                            x = i-1+a
                        if (j-1+b) > len(self.template[i])-1:
                            y = 0
                        elif (j-1+b) < 0:
                            y = len(self.template[i])-1
                        else:
                            y = j-1+b
                        # počítání sousedů (živých buňek)
                        if self.template[x][y] == 1:
                            neighborhood += 1
                # pravidla pro živé buňky
                if self.template[i][j] == 1:
                    if neighborhood < 3:
                        new_template[i][j] = 0
                    if neighborhood == 3 or neighborhood == 4:
                        new_template[i][j] = 1
                    if neighborhood > 4:
                        new_template[i][j] = 0
                # pravidla pro mrtvé buňky
                if self.template[i][j] == 0:
                    if neighborhood == 3:
                        new_template[i][j] = 1
                    else:
                        new_template[i][j] = 0
        if (self.template == new_template):
            self.play = False
        else:
            self.template = new_template
        self.create_game()

    # časová smyčka
    def loop(self): 
        n = 0
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])):
                n += 1 if self.template[i][j] == 1 else 0
        self.generations()
        if self.play == True and n>0:
            self.generation += 1
            self.game()
            root.after(200, self.loop)
        else:
            self.play = False

    # při kliknutí myší
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
                    if self.square.fill_color == DEFAULT_CONFIG["fill"]:
                        x = int(round(self.square.x) / DEFAULT_CONFIG["side"])
                        y = int(round(self.square.y) / DEFAULT_CONFIG["side"])
                        self.template[y][x] = 1

                    elif self.square.fill_color == DEFAULT_CONFIG["live_cell_color"]:
                        x = int(round(self.square.x) / DEFAULT_CONFIG["side"])
                        y = int(round(self.square.y) / DEFAULT_CONFIG["side"])
                        self.template[y][x] = 0
            self.create_game()

    #předpřipravený template pro stálý život
    def still(self):
        self.generation = 0
        self.play = False
        template = [
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
        for i in range(len(template)):  
            for j in range(len(template[i])):
                self.template[i][j] = template[i][j]
        self.create_game()

    #předpřipravený template pro oscilátory
    def oscillators(self):
        self.generation = 0
        self.play = False
        template = [
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
        for i in range(len(template)):  
            for j in range(len(template[i])):
                self.template[i][j] = template[i][j]
        self.create_game()

    #předpřipravený template pro lodě
    def ships(self):
        self.generation = 0
        self.play = False
        template = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for i in range(len(template)):  
            for j in range(len(template[i])):
                self.template[i][j] = template[i][j]
        self.create_game()

    #náhodný template
    def random(self):
        self.generation = 0
        self.play = False
        for i in range(len(self.template)):  
            for j in range(len(self.template[i])):
                self.template[i][j] = random.randrange(0, 2)
        self.create_game()


root = Tk()
root.title("Game of Life")
myapp = MyApp(root)
myapp.create_game()

root.mainloop()
