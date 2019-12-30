from abc import ABC , abstractmethod

class Point():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
    def draw(self, canvas):       
        return canvas.create_rectangle(self.x, self.y, self.x+10, self.y+10, fill=DEFAULT_CONFIG['fill'])
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y


class Shape(ABC):
    def __init__(self,x,y):
        self.type = self.__class__.__name__
        self.x = float(x)
        self.y = float(y)
        self.width = float(200)
        self.height = float(100)
        self.outline_color = DEFAULT_CONFIG['outline']
        self.outline_width = DEFAULT_CONFIG['width']
        self.fill = DEFAULT_CONFIG['fill']

    def __repr__(self):
        return "Shape(x: {},y: {},width: {},height: {},fill: {})".format(self.x, self.y,self.width,self.height,self.fill)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self,value):
        if value < 0:
            self.__x = 0
            return
        self.__x = float(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self,value):
        if value < 0:
            self.__y = 0
            return
        self.__y = float(value)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self,value):
        if value < 0:
            self.__width = 0
            return
        self.__width = float(value)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self,value):
        if value < 0:
            self.__height = 0
            return
        self.__height = float(value)

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def detect_cursor(self, point):
        pass