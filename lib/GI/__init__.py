###################################################################
## Module  : Graphic interface ## Author   : Marcos Bento        ##
## --------------------------- ## ------------------------------ ##
## Github  : TheMarcosBC       ## Twitter  : TheMarcosBC         ##
## --------------------------- ## ------------------------------ ##
## Facebook: TheMarcosBC       ## Instagram: TheMarcosBC         ##
###################################################################

# import default modules
import time, tkinter

# import local modules
from . import Event, Interface, Widget
from .VariablesCSS import *
from .. import Image, Unique
from ..Main import *

# fixed variables
windows = {}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class _window(dict):
    def __init__(self):
        self.widget = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.widget)
        self.canvas.configure(bg='white', highlightthickness=0, bd=0)
        self.canvas.pack(expand=True, fill='both')
        self.document = None
        self.focused = None
        self.items = []
        self.length = None
        self.settimeout = []
        self.setinterval = []
        self['title'] = 'TheMarcosBC.GI'
        self.widget.title('TheMarcosBC.GI')
        self.on = Event.new()
        Event.call(self)
        self.widget.update()

class _time:
    @property
    def timer(self):
        return (time.time() * 1000.0) - self.__start__

    @property
    def count(self):
        return round(self.timer / self.__timer__)

    def stop(self):
        try:
            if self.__mode__ == 'timeout':
                parent = windows[self.__parent__.__id__].settimeout
            else:
                parent = windows[self.__parent__.__id__].setinterval
            index = parent.index(self)
            del parent[index]
        except:
            pass

    def __running__(self):
        try:
            timer = time.time() * 1000.0
            if self.__mode__ == 'interval':
                if timer >= self.__end__:
                    self.__end__ = timer + self.__timer__
                    self.__function__(self)
            elif timer >= self.__end__:
                self.__function__(self)
                self.stop()
        except Exception as e:
            print(e)

    def __init__(self, parent, function, timer, mode):
        self.__function__ = function
        self.__mode__ = mode
        self.__parent__ = parent
        self.__start__ = time.time() * 1000.0
        self.__end__ = self.__start__ + timer
        self.__timer__ = timer

# widget
class window(dict):
    def fullscreen(self):
        if not windows[self.__id__]['fullscreen']:
            windows[self.__id__]['fullscreen'] = True
            windows[self.__id__].widget.attributes('-fullscreen', True)
        else:
            windows[self.__id__]['fullscreen'] = False
            windows[self.__id__].widget.attributes('-fullscreen', False)

    def maximize(self):
        if not windows[self.__id__]['maximize']:
            windows[self.__id__]['maximize'] = True
            windows[self.__id__].widget.attributes('-zoomed', True)
        else:
            windows[self.__id__]['maximize'] = False
            windows[self.__id__].widget.attributes('-zoomed', False)

    # time
    def setTimeout(self, call, timer):
        windows[self.__id__].settimeout.append(_time(self, call, timer, 'timeout'))

    def setInterval(self, call, timer):
        windows[self.__id__].setinterval.append(_time(self, call, timer, 'interval'))

    # size
    @property
    def width(self): return windows[self.__id__].widget.winfo_width()
    @property
    def height(self): return windows[self.__id__].widget.winfo_height()
    @width.setter
    def width(self, value):
        windows[self.__id__].widget.geometry('%dx%d' % (value, self.height))
        windows[self.__id__].widget.update()
    @height.setter
    def height(self, value):
        windows[self.__id__].widget.geometry('%dx%d' % (self.width, value))
        windows[self.__id__].widget.update()

    # title
    @property
    def title(self, value): return windows[self.__id__]['title']
    @title.setter
    def title(self, value):
        windows[self.__id__]['title'] = str(value)
        windows[self.__id__].widget.title(windows[self.__id__]['title'])

    def __init__(self):
        self.__id__ = lockStr(Unique.id())
        windows[self.__id__] = _window()
        windows[self.__id__].main = self

class document:
    createTag = Widget.frame.createTag

    @property
    def length(self): return self.items.length

    # create
    def __init__(self, window):
        self.window = window
        window.document = self
        windows[window.__id__].document = self
        Widget._items(self)


def loop():
    while True:
        for win in windows.values():
            for timeout in win.settimeout:
                timeout.__running__()
            for interval in win.setinterval:
                interval.__running__()
            Interface.up(win)
