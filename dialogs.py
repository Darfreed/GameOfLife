from tkinter import * 

class ObjectDialog:
    def __init__(self, parent, obj):
        top = self.top = Toplevel(parent)
        self.obj = obj
        top.title("Parametry")
        top.transient(parent)
        #zablokuje práci na hlavním panelu - modální okno
        top.grab_set()
        # nastaví zaměření na dialog
        top.focus_set()
        x = parent.winfo_x()
        y = parent.winfo_y()
        top.geometry("%dx%d+%d+%d" % (600, 150, x + 100, y + 100))
        #proměnné pro vkládání parametrů okna
        spin_width_value = StringVar()
        spin_width_value.set(self.obj.width)
        spin_height_value = StringVar()
        spin_height_value.set(self.obj.height)
        spin_side_value = StringVar()
        spin_side_value.set(self.obj.side)
        #kontejner pro pozici objektu
        container1 = Frame(top, width = 400, pady=10, padx=10)

        label_pozice = Label(container1, text = "Velikost pole", pady=5)
        label_pozice.pack()

        label_width = Label(container1, text="width:")
        label_width.pack(side=LEFT)
        self.spinbox_width = Spinbox(container1, from_=0, to=parent.winfo_width(), textvariable=spin_width_value)
        self.spinbox_width.pack(side=LEFT, padx=10)
        label_width.pack()
        
        label_height = Label(container1, text="height:")
        label_height.pack(side=LEFT)
        self.spinbox_height = Spinbox(container1, from_=0, to=parent.winfo_height(), textvariable=spin_height_value)
        self.spinbox_height.pack(side=LEFT, padx=10)
        label_height.pack()

        label_side = Label(container1, text="cell width:")
        label_side.pack(side=LEFT)
        self.spinbox_side = Spinbox(container1, from_=0, to=parent.winfo_width(), textvariable=spin_side_value)
        self.spinbox_side.pack(side=LEFT, padx=10)

        container1.pack(fill=BOTH)

        button_ok = Button(top, text = "OK", command = self.ok)
        button_ok.pack(side=LEFT, padx=10,pady=10,fill=BOTH,expand=True)
        button_cancel = Button(top, text = "Cancel", command = self.cancel)
        button_cancel.pack(side=LEFT, padx=10,pady=10,fill=BOTH,expand=True)


    def ok(self, event=None):
        self.obj.width = int(self.spinbox_width.get())
        self.obj.height = int(self.spinbox_height.get())
        self.obj.side = int(self.spinbox_side.get())
        self.top.destroy()
    
    def cancel(self, event = None):
        self.top.destroy()