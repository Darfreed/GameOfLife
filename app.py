from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter.filedialog import askopenfile,asksaveasfile
from grafika import *

class MyApp:
    def __init__(self, parent):
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.x = 100
        self.y = 100
        self.shapes = []
        self.shape = None
        self.action = ""
        self.parent = parent
        self.drawWidgets()

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.canvas = Canvas(self.parent, width=screen_width / 2, height=screen_height / 2, bg=self.color_bg)
        self.canvas.pack(fill=BOTH,expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.focus_set()

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Soubor',menu=filemenu)
        filemenu.add_command(label='Otevřít...',command=self.open_file) 
        filemenu.add_command(label='Uložit...',command=self.save_file)  
        filemenu.add_command(label='Konec',command=self.parent.destroy)
        canvasmenu = Menu(menu)
        menu.add_cascade(label='Plátno',menu=canvasmenu)
        canvasmenu.add_command(label='Barva pozadí',command=self.change_bg)

    #dekodovani souboru json
    def object_decoder(self, obj):
        if obj['type'] == 'Rectangle':
            shape = Rectangle(obj['_Shape__x'], obj['_Shape__y'])
        if obj['type'] == 'Oval':
            shape = Oval(obj['_Shape__x'], obj['_Shape__y'])
        shape.width = obj['_Shape__width']
        shape.height = obj['_Shape__height']
        shape.outline_color = obj['outline_color']
        shape.outline_width = obj['outline_width']
        shape.fill = obj['fill']
        return shape

    #otevreni vnejsiho avatara
    def open_file(self):
        filetypes = [('Všechny soubory','*.*'),('JavaScript Object Notation','*.json')]
        file = askopenfile(filetypes = filetypes, title = "Otevření souboru")
        self.shapes = json.loads(file.read(),object_hook=self.object_decoder)
        self.redraw_canvas()
        pass
    
    #ulozeni avatara jako *.json
    def save_file(self):
        filetypes = [('Všechny soubory','*.*'),('JavaScript Object Notation','*.json'),('eXtesible Markup Language','*.xml')]
        file = asksaveasfile(filetypes = filetypes, title = "Uložení souboru", initialdir = "./")
        json_data = json.dumps([ob.__dict__ for ob in self.shapes])
        file.write(json_data)
        print(json_data)
        pass 

    #change of background
    def change_bg(self):  
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.canvas['bg']=self.color_bg

    def redraw_canvas(self):  
        self.clear_canvas()
        for shape in self.shapes:
            shape.draw(self.canvas) 
    
    def on_mouse_move(self, event):
        print("Pohyb myši nad canvasem")
    
    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasx(event.y)
        point = Point(self.start_x, self.start_y)
        self.action == ""
        for s in self.shapes:
            if s.detect_cursor(point): 
                self.shape = s
                self.old_x = self.shape.x
                self.old_y = self.shape.y
                self.old_width = self.shape.width
                self.old_height = self.shape.height
                self.action = "edit"
        print("Stisk levého tlačítka myši")

    def on_move_press(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        if (self.action == "new"):
            self.shape.x = self.start_x if self.start_x <= cur_x else cur_x
            self.shape.y = self.start_y if self.start_y <= cur_y else cur_y
            self.shape.width = abs(self.start_x - cur_x)
            self.shape.height = abs(self.start_y - cur_y)
        print(cur_x , cur_y)
        print("Tažení myši nad canvasem")

    def on_button_release(self, event):
        self.action = ""
        print("Uvolnění tlačíka myši")

root = Tk()
myapp = MyApp(root)
root.mainloop()