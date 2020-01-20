DEFAULT_CONFIG = {"fill": "white",
                  "live_cell_color":"black",
                  "side": 25,
                  "outline": "grey",
                  "width": 1}

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y

class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.side = DEFAULT_CONFIG["side"]
        self.outline_color = DEFAULT_CONFIG["outline"]
        self.outline_width = DEFAULT_CONFIG["width"]
        self.fill_color = DEFAULT_CONFIG["fill"]
        self.live_cell_color = DEFAULT_CONFIG["live_cell_color"]

    def __repr__(self):
        return "Square(x: {}, y: {}, side: {}, fill_color: {} )".format(self.x, self.y, self.side, self.fill_color)

    def draw(self, canvas):
        pass

class Build(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill_color = DEFAULT_CONFIG["fill"]

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)

    def detect_cursor(self,point):
        return (self.x <= point.x <= self.x + self.side and self.y <= point.y <= self.y + self.side)


class LiveCell(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fill_color = DEFAULT_CONFIG["live_cell_color"]

    def draw(self, canvas):
        return canvas.create_rectangle(self.x, self.y, self.x + self.side, self.y + self.side, fill=self.fill_color,
                                       outline=self.outline_color, width=self.outline_width)
    
    def detect_cursor(self,point):
        return (self.x <= point.x <= self.x + self.side and self.y <= point.y <= self.y + self.side)
