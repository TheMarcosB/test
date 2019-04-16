###################################################################
## Module  : Graphic interface ## Author   : Marcos Bento        ##
## --------------------------- ## ------------------------------ ##
## Github  : TheMarcosBC       ## Twitter  : TheMarcosBC         ##
## --------------------------- ## ------------------------------ ##
## Facebook: TheMarcosBC       ## Instagram: TheMarcosBC         ##
###################################################################

# import default modules
import datetime, os, re, sys, tkinter, time
import tkinter.font as Font

# import local modules
from .Main import *
from . import Error, Image

# background
BgColor = '#efefef'; BgButton = '#dfdfdf'; BgEntry = '#ffffff'; BgScroll = '#4f4f4f'
# Border
BdColor = '#7f7f7f'; BdFocus = '#3498db'; BdHover = '#2f2f2f'
# font
FgColor = '#000000'; FgFocus = '#3498db'; FgHover = '#2f2f2f'

###################################################################
## ------------ here starts the module definitions ------------- ##
###################################################################
def fontSize(self):
    count = 0
    font = Font.Font(
       family = self.getStyle('font-family'),
       size = self.getStyle('font-size'),
       weight = self.getStyle('font-weight')
    )
    width, height = 0, font.metrics('linespace')
    for line in self.getText().split('\n'):
        w = font.measure(line) + (font.measure('0') / 2)
        if w > width:
            width = w
        count += 1
    return width, height * count

# Bases
class Time:
    @property
    def timer(self):
        return (time.time() * 1000.0) - self.__start__

    @property
    def count(self):
        return round(self.timer / self.__timer__)

    def stop(self):
        try:
            if self.__mode__ == 'timeout':
                parent = self.__parent__.__settimeout__
            else:
                parent = self.__parent__.__setinterval__
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
                    try:
                        self.__function__(self)
                    except:
                        self.__function__()
            elif timer >= self.__end__:
                try:
                    self.__function__(self)
                except:
                    self.__function__()
                self.stop()
        except:
            self.stop()

    def __init__(self, parent, function, timer, mode):
        self.__function__ = function
        self.__mode__ = mode
        self.__parent__ = parent
        self.__start__ = time.time() * 1000.0
        self.__end__ = self.__start__ + timer
        self.__timer__ = timer

class Call(dict):
    # execute commands
    def __cmd__(self, name, event):
        self.event = event
        cmd = self.__dict__.get('on' + name)
        # execute first command
        try: self.__callback__[name.lower()](event)
        except: pass

        # execute command by function
        try:
            try: cmd(self)
            except: cmd()
        except:
            pass
        self.event = None

    # click command
    def __click__(self, event):
        self.__focus__(event)
        return self.__cmd__('Click', event)

    def __press__(self, event):
        self.__focus__(event)
        return self.__cmd__('Press', event)

    # key command
    def __key__(self, event):
        self.__cmd__('Key', event)
        if isinstance(self, Window):
            try:
                widget = self.__focused__ if self.__focused__ else self.__hovered__
                if not isinstance(widget, (Input, TextBox, Window)) :
                    widget.__key__(event)
            except:
                pass

    def __keypress__(self, event):
        self.__cmd__('KeyPress', event)
        if isinstance(self, Window):
            try:
                widget = self.__focused__ if self.__focused__ else self.__hovered__
                if not isinstance(widget, (Input, TextBox, Window)) :
                    widget.__keypress__(event)
            except:
                pass

    def __keyup__(self, event):
        self.__cmd__('KeyUp', event)
        if isinstance(self, Window):
            try:
                widget = self.__focused__ if self.__focused__ else self.__hovered__
                if not isinstance(widget, (Input, TextBox, Window)) :
                    widget.__keyup__(event)
            except:
                pass

    # mouse command
    def __move__(self, event):
        self.__cmd__('Move', event)

    def __over__(self, event):
        self.__cmd__('Over', event)
        if not isinstance(self, (Input, TextBox, Window)):
            self.window.__hovered__ = self

    def __out__(self, event):
        self.__cmd__('Out', event)
        if not isinstance(self, Window):
            self.window.__hovered__ = None

    def __wheelup__(self, event):
        event.mousewheel = 'up'
        self.__cmd__('Wheel', event)
        if isinstance(self, Window) and self.__hovered__:
            try: self.__hovered__.__wheelup__(event)
            except: pass

    def __wheeldown__(self, event):
        event.mousewheel = 'down'
        self.__cmd__('Wheel', event)
        if isinstance(self, Window) and self.__hovered__:
            try: self.__hovered__.__wheeldown__(event)
            except: pass

    # create
    def __init__(self):
        # click
        self.widget.bind('<Button-1>', self.__click__)
        self.widget.bind('<ButtonPress>', self.__press__)
        # key
        self.widget.bind('<Key>', self.__key__)
        self.widget.bind('<KeyPress>', self.__keypress__)
        self.widget.bind('<KeyRelease>', self.__keyup__)
        # mouse
        self.widget.bind('<Motion>', self.__move__)
        self.widget.bind('<Enter>', self.__over__)
        self.widget.bind('<Leave>', self.__out__)
        self.widget.bind('<Button-4>', self.__wheelup__)
        self.widget.bind('<Button-5>', self.__wheeldown__)

class Base(Call):
    __istext__ = False

    @property
    def __real__(self):
        try: return self.__frame__
        except: return self.widget

    # style
    def getStyle(self, key):
        try:
            attr = '--' + str(key)
            devolve = self[attr] if self[attr] != None else self[key]
        except:
            if key in ['-width', '-height']:
                border = self['--border'] if self['--border'] != None else self['border']
                devolve = self[key] + (border * 2)
            else:
                devolve = self[key]
        # set cursor
        if key in ['cursor', '-cursor', '--cursor']:
            devolve = {
                'normal': 'arrow',
                'pointer': 'hand2'
            }.get(devolve, 'arrow')
        # devolve
        return devolve

    def style(self, *argsv, **argsk):
        try: dict.update(self, argsv[0])
        except: pass
        dict.update(self, argsk)

    # string
    def __repr__(self):
        return '<TheMarcosBC.GI.%s>' % (self.tag.capitalize())

    def __str__(self):
        return self.__repr__()

    # create
    def __init__(self):
        self.event = None
        self.__end__ = {}
        self.__callback__ = {}

class Scroll(dict):
    def update(self):
        # parent
        parent = self.parent
        width, height = parent['-width'], parent['-height']

        # scroll
        bgColor = parent.getStyle('background')
        barColor = parent.getStyle('scroll-background')
        scroll = parent.getStyle('scroll')
        size = parent.getStyle('scroll-size')

        # scroll widget x
        bgX = self.bgX
        barX = self.barX

        # scroll widget y
        bgY = self.bgY
        barY = self.barY

        # scroll x
        sizeX = parent['-scroll-size-x']
        notX = scroll in ['auto', 'auto-x'] and sizeX <= 0

        # scroll y
        sizeY = parent['-scroll-size-y']
        notY = scroll in ['auto', 'auto-y'] and sizeY <= 0

        # scroll hide
        if scroll in [None, 'x', 'y'] or notX or notY:
            if self.isX and scroll in [None, 'x'] or notX:
                self.isX = False
                bgY.place(width=0, height=0, x=-1, y=-1)

            if self.isY and scroll in [None, 'y'] or notY:
                self.isY = False
                bgX.place(width=0, height=0, x=-1, y=-1)

        # scroll show
        else:
            upSize = size != self['bar-size']
            upBg = bgColor != self['bg']
            upBar = barColor != self['bar']
            w, h = parent['-scroll-bar-width'], parent['-scroll-bar-height']
            x, y = parent['-scroll-bar-x'], parent['-scroll-bar-y']

            if scroll in ['auto', 'auto-x', True, 'x']:
                self.isX = True

                # style x
                if upBg: bgX.configure(bg=bgColor)
                if upBar: barX.configure(bg=barColor)

                # configure x
                if upSize: bgX.place(width=size + 4, height=height, x=width - (size + 4), y=0)
                if upSize or (self['bar-height'], self['bar-y']) != (h, y):
                    self['bar-height'], self['bar-y'] = h, y
                    barX.place(width=size, height=h, x=2, y=y)

            if scroll in ['auto', 'auto-y', True, 'y']:
                self.isY = True

                # style y
                if upBg: bgY.configure(bg=bgColor)
                if upBar: barY.configure(bg=barColor)

                # configure y
                if upSize: bgY.place(width=width, height=size + 4, x=0, y=height - (size + 4))
                if upSize or (self['bar-width'], self['bar-x']) != (w, x):
                    self['bar-width'], self['bar-x'] = w, x
                    barY.place(width=w, height=size, x=x, y=2)

            if upBg: self['bg'] = bgColor
            if upBar: self['bar'] = barColor
            if upSize: self['bar-size'] = size

    def __init__(self, parent):
        self.parent = parent
        parent.__scroll__ = self

        # scroll widget x
        self.bgX = tkinter.Frame(parent.widget)
        self.bgX.configure(highlightthickness=0, bd=0)
        self.barX = tkinter.Label(self.bgX)
        self.barX.configure(highlightthickness=0, bd=0)
        self.isX = False

        # scroll widget y
        self.bgY = tkinter.Frame(parent.widget)
        self.bgY.configure(highlightthickness=0, bd=0)
        self.barY = tkinter.Label(self.bgY)
        self.barY.configure(highlightthickness=0, bd=0)
        self.isY = False

        # attributes
        dict.update(self, {
            # background
            'bg': None, 'bar': None,
            # bar
            'bar-size': None, 'bar-width': None, 'bar-height': None, 'bar-x': None, 'bar-y': None,
            # bar
            'scroll-width': None, 'scroll-height': None
        })

class Widget(Base):
    # settings
    def __graphic__(self):
        if self != self.__end__:
            self.__end__.update(self)
            border = self.getStyle('border-color')
            self.widget.configure(
                bg = self.getStyle('background'),
                cursor = self.getStyle('cursor'),
                highlightbackground = border,
                highlightcolor = border,
                highlightthickness = self.getStyle('border'),
                bd = 0
            )
            if self.__istext__:
                self.widget.configure(
                    fg = self.getStyle('color'),
                    font = (self.getStyle('font-family'), self.getStyle('font-size'), self.getStyle('font-weight'))
                )

    def __conf__(self):
        widget = self.widget
        parent = self.parent
        # get size
        size = widget.winfo_width(), widget.winfo_height()
        w, h = self.getStyle('width'), self.getStyle('height')
        width, height = self['-width'], self['-height']
        border = self.getStyle('border') * 2
        # set width
        if w == '100%':
            width = parent['-width']
            self['-width'] = width
        elif type(w) is int:
            width = w
            self['-width'] = w
        # set height
        if h == '100%':
            height = parent['-height']
            self['-height'] = height
        elif type(h) is int:
            height = h
            self['-height'] = h
        # set border
        if border > 0:
            height += border
            width += border
        # set size
        if (width, height) != size:
            widget.place(width=width, height=height)

    def update(self):
        self.__conf__()
        self.__graphic__()

    # attribute styles
    def __delattrs__(self):
        for k, v in dict.items(self):
            if k[0 : 2] == '--':
                self[k] = None
            elif k in ['.width', '.height'] and v != None:
                try: self['-' + k[1 : ]] = int(v)
                except: pass
                self[k] = None
        try: self.__clear__()
        except: pass

    def __setattrs__(self, update):
        try:
            for k, v in update.items():
                key = '--' + str(k)
                if key in dict.keys(self):
                    self[key] = v
                    if k in ['width', 'height']:
                        bk = '.' + k
                        try:
                            if self[bk] == None:
                                self[bk] = int(self['-' + k])
                        except:
                            pass
        except:
            pass

    # action styles
    def focus(self, *argsv, **argsk):
        try: self.__focused__.update(argsv[0])
        except: pass
        self.__focused__.update(argsk)

    def hover(self, *argsv, **argsk):
        try: self.__hovered__.update(argsv[0])
        except: pass
        self.__hovered__.update(argsk)

    # action commands
    def __focus__(self, event):
        focus = self.window.__focused__

        if not focus or self.widget != focus.widget:
            try:
                focus.__delattrs__()
                focus['-focus'] = False
            except:
                pass

            self['-focus'] = True
            self.window.__focused__ = self
            self.__setattrs__(self.__focused__)

    def __over__(self, event):
        self.__setattrs__(self.__hovered__)
        self['-hover'] = True
        Call.__over__(self, event)

    def __out__(self, event):
        self.__delattrs__()
        self['-hover'] = False
        if self['-focus']:
            self.__setattrs__(self.__focused__)
        Call.__out__(self, event)

    # create
    def __init__(self, parent):
        Base.__init__(self)
        parent.items.append(self)
        # parents
        self.parent = parent
        self.window = parent.window
        self.widget = self.__create__(parent.__real__)
        # tags
        self.cls = None
        self.id = None
        self.name = None
        # action
        self.__focused__ = {}
        self.__hovered__ = {}
        # style
        self.style(parent)
        self.style({
            # size
            'width': 'auto', 'height': 'auto', '-width': 0, '-height': 0,
            # size attributes
            '.width': None, '.height': None, '--width': None, '--height': None,
            # position
            'float': 'auto', 'position': 'auto', 'x': 0, 'y': 0,
            # position attributes
            '--float': None, '--position': None, '--x': None, '--y': None,
            # scroll
            'scroll': None, '--scroll': None, '--scroll-size': None,
            # scroll size
            '-scroll-size-x': 0, 'scroll-size-y': 0, '-scroll-bar-width': 0, '-scroll-bar-height': 0,
            # scroll position
            'scroll-x': 0, 'scroll-y': 0, '-scroll-bar-x': 0, '-scroll-bar-y': 0,
            # background
            '--background': None, '--scroll-background': None, '--scroll-bar': None,
            # font
            '--color': None, '--font-family': None, '--font-size': None, '--font-weight': None, '--text-align': None,
            # border
            'border': 0, 'border-color': '#000000', '--border': None, '--border-color': None,
            # margin
            'margin-top': 0, 'margin-right': 0, 'margin-bottom': 0, 'margin-left': 0,
            # margin attributes
            '--margin-top': None, '--margin-right': None, '--margin-bottom': None, '--margin-left': None,
            # padding
            'padding-x': 0, 'padding-y': 0, '--padding-x': None, '--padding-y': None,
            # action
            '--cursor': None, '-focus': False, '-hover': False
        })
        # add callbacks
        Call.__init__(self)

class Label(Widget):
    tag = 'label'
    __create__ = tkinter.Label
    __istext__ = True

    # string
    def addText(self, value):
        self.__text__.set(self.__text__.get() + str(value))

    def getText(self):
        return self.__text__.get()

    def setText(self, value):
        self.__text__.set(str(value))

    # settings
    def update(self):
        text = self.getText()
        if text != self['.text']:
            self['.text'] = text
            size = fontSize(self)
            # update size
            self['-width'], self['-height'] = size
            self['-width'] += self.getStyle('padding-x') * 2
            self['-height'] += self.getStyle('padding-y') * 2
        Widget.update(self)

    # create
    def __init__(self, parent, text=''):
        Widget.__init__(self, parent)
        self.__text__ = tkinter.StringVar()
        self.__text__.set('Label' if not text and self.tag == 'label' else text)
        self['.text'] = ''
        self.widget.configure(textvariable=self.__text__)

# frame
class Window(Base):
    # commands
    def fullscreen(self):
        # fullscreen mode
        if not self['-fullscreen']:
            self['-fullscreen'] = True
            self.widget.attributes('-fullscreen', True)
        # no fullscreen
        else:
            self['-fullscreen'] = False
            self.widget.attributes('-fullscreen', False)

    def loop(self):
        while True:
            for timeout in self.__settimeout__:
                timeout.__running__()
            for interval in self.__setinterval__:
                interval.__running__()
            self.update()

    def maximize(self):
        if not self['-maximize']:
            self['-maximize'] = True
            self.widget.attributes('-zoomed', True)
        else:
            self['-maximize'] = False
            self.widget.attributes('-zoomed', False)

    def setTimeout(self, call, timer):
        self.__settimeout__.append(Time(self, call, timer, 'timeout'))

    def setInterval(self, call, timer):
        self.__setinterval__.append(Time(self, call, timer, 'interval'))

    def title(self, title='TheMarcosBC.GI'):
        self.widget.title(str(title))

    # items
    def __items__(self, key, type):
        devolve = None
        for item in self.items:
            if type == 'widget' and item.widget == key:
                devolve = item
                break
            elif isinstance(item, Frame):
                try:
                    item = item.__items__(key, type)
                    if item != None:
                        devolve = item
                        break
                except:
                    pass
        return devolve

    def getByWidget(self, widget):
        return self.__items__(widget, 'widget')

    def getByClass(self, key):
        return self.__items__(key, 'class')

    def getById(self, key):
        return self.__items__(key, 'id')

    def getByName(self, key):
        return self.__items__(key, 'name')

    def getByTag(self, key):
        return self.__items__(key, 'id')

    # settings
    def __graphic__(self):
        if self != self.__end__:
            self.__end__.update(self)
            self.widget.configure(
                bg=self.getStyle('background'),
                cursor=self.getStyle('cursor')
            )

    def __conf__(self):
        window = self.widget
        getPosition = window.winfo_x(), window.winfo_y()
        getSize = window.winfo_width(), window.winfo_height()
        # position
        position = self['x'], self['y']
        # size
        size = self['-width'], self['-height']
        max = self['max-width'], self['max-height']
        min = self['min-width'], self['min-height']
        # size limit
        if not None in max: window.maxsize(max)
        if not None in min: window.minsize(min)
        # set system style
        if not self['system-style']: window.overrideredirect(0)
        # set absolute size
        if type(self['width']) is int and type(self['height']) is int:
            window.geometry('%dx%d' % (self['width'], self['height']))
            self['-width'] = self['width']
            self['-height'] = self['height']
        # set normal size
        elif size != getSize:
            self['-width'] = getSize[0]
            self['-height'] = getSize[1]
        # set absolute position
        if self['position'] == 'absolute': window.geometry('%d+%d' % position)
        # set normal position
        elif position != getPosition:
            self['x'] = getPosition[0]
            self['y'] = getPosition[1]

    def update(self, **argsk):
        scroll = self.__scroll__
        isframe = argsk.get('frame') == True

        # widget
        _width, _height = 0, 0
        _x = self['scroll-x'] if self.getStyle('width') != 'auto' else 0
        _y = self['scroll-y'] if self.getStyle('height') != 'auto' else 0
        auto = isframe and self.getStyle('width') == 'auto'
        self.__conf__()

        # main
        jump = 0
        length = 0
        max = self['-width']

        # position
        left = _x
        right = _x
        top = _y

        for item in self.items:
            widget = item.widget
            item.update()

            if item.getStyle('position') == 'absolute':
                x, y = item.getStyle('x'), item.getStyle('y')

                if (x, y) != (widget.winfo_x(), widget.winfo_y()):
                    widget.place(x=x, y=y)

            else:
                side = item.getStyle('float')
                width, height = item.getStyle('-width'), item.getStyle('-height')

                # margin
                marginL, marginR = item.getStyle('margin-left'), item.getStyle('margin-right')
                marginT, marginB = item.getStyle('margin-top'), item.getStyle('margin-bottom')
                marginX = marginL + marginR
                marginY = marginT + marginB

                # full size
                w =  width + marginX
                h =  height + marginY

                if side in ['left', 'right']:
                    if side == 'left' if auto else max >= length + w:
                        # set left
                        if side == 'left':
                            x = left + marginL
                            left += width + marginL

                        # set right
                        else:
                            right += width + marginR
                            x = max - right

                        # new jump
                        if h > jump:
                            jump = h

                        # set lenght
                        length += w

                    else:
                        length = w # new length
                        top += jump # update top
                        _height += jump # update height
                        jump = h # new jump

                        # set left
                        if auto or side == 'left':
                            x = marginL
                            left = _x + width + marginL
                            right = _x

                        # set right
                        else:
                            right = _x + width + marginR
                            x = max - right
                            left = _x

                    # set position
                    y = top + item['margin-top']

                    if (item['x'], item['y']) != (x, y):
                        item['x'] = x
                        item['y'] = y
                        widget.place(x=x, y=y)

                else:
                    top += jump
                    _height += jump
                    x = _x + marginL
                    y = top + marginT

                    if (x, y) != (widget.winfo_x(), widget.winfo_y()):
                        item['x'] = x
                        item['y'] = y
                        widget.place(x=x, y=y)

                    jump = 0
                    left = _x + w
                    right = _x
                    length = w
                    top += h
                    _height += h

                if length > _width:
                    _width = length

        if isframe and self.getStyle('width') == 'auto':
            self['-width'] = _width

        else:
            _size = _width - self['-width']
            _scroll = _size if _size > 0 else 0


        if isframe and self.getStyle('height') == 'auto':
            self['-height'] = _height + jump

        else:
            _size = (_height + jump)

            if scroll['scroll-height'] != _size:
                scroll['scroll-height'] = _size
                self['-scroll-size-y'] = _size
                self['-scroll-bar-height'] = self['-height'] / (_size / self['-height']) if _size > 0 else 0

        self.__scroll__.update()
        self.__graphic__()

        if not isframe:
            self.widget.update()

    # commands
    def __focus__(self, event):
        focus = self.__focused__
        if focus and focus.widget != event.widget:
            focus.__delattrs__()
            focus['-focus'] = False
            self.__focused__ = None

    # create
    def __init__(self):
        Base.__init__(self)
        self.items = []
        self.tag = 'window'
        # widget
        self.parent = None
        self.widget = tkinter.Tk()
        self.window = self
        self.__focused__ = None
        self.__settimeout__ = []
        self.__setinterval__ = []
        # set style
        self.style({
            # size
            'width': 'auto', 'height': 'auto', '-width': 200, '-height': 200,
            # size lock
            'max-width': None, 'max-height': None, 'min-width': None, 'min-height': None,
            # position
            'x': 0, 'y': 0, 'position': 'auto',
            # scroll
            'scroll': None, 'scroll-size': 10,
            # scroll size
            '-scroll-size-x': 0, '-scroll-size-y': 0, '-scroll-bar-width': 0, '-scroll-bar-height': 0,
            # scroll position
            'scroll-x': 0, 'scroll-y': 0, '-scroll-bar-x': 0, '-scroll-bar-y': 0,
            # background
            'background': BgColor, 'scroll-background': BgScroll, 'scroll-bar': BdColor,
            # font
            'color': FgColor, 'font-family': 'Helvetica', 'font-size': 10, 'font-weight': 'normal', 'text-align': 'left',
            # action
            'cursor': 'arrow', 'system-style': True, '-fullscreen': False, '-maximize': False
        })
        # add callbacks
        Call.__init__(self)
        # add scroll
        Scroll(self)
        # set title
        self.title()

class Frame(Widget):
    tag = 'frame'
    __create__ = tkinter.Frame
    # get items
    getByClass = Window.getByClass
    getById = Window.getById
    getByName = Window.getByName
    getByTag = Window.getByTag

    # settings
    def update(self):
        Window.update(self, frame=True)
        self.__frame__.configure(
            bg = self.getStyle('background'),
            cursor = self.getStyle('cursor')
        )
        self.__frame__.place(
            width = self['-width'] - (self.getStyle('scroll-size') if self.__scroll__.isX else 0),
            height = self['-height'] - (self.getStyle('scroll-size') if self.__scroll__.isY else 0),
            x = 0,
            y = 0
        )

    # create
    def __init__(self, parent):
        Widget.__init__(self, parent)
        self.items = []
        self.__frame__ = tkinter.Frame(self.widget)
        self.__frame__.configure(highlightthickness=0, bd=0)
        self['width'] = '100%'
        # add scroll
        Scroll(self)

# labels
class Button(Label):
    tag = 'button'

    # create
    def __init__(self, parent, text='Button'):
        Label.__init__(self, parent, text)
        self.style({
            'height': 26,
            'color': FgHover,
            'background': BgButton,
            'border': 1,
            'border-color': BdColor,
            'font-size': 10,
            'font-weight': 'bold',
            'padding-x': 15
        })
        self.focus({
            'color': FgFocus,
            'border-color': BdFocus
        })
        self.hover({
            'color': FgColor,
            'border-color': BdHover
        })

# text
class Input(Label):
    tag = 'input'
    __create__ = tkinter.Entry

    # create
    def __init__(self, parent, text=''):
        Label.__init__(self, parent, text)
        self.style({
            'width': 100,
            'height':  26,
            'color': FgColor,
            'font-size': 10,
            'background': BgEntry,
            'border': 1,
            'border-color': BdColor
        })
        self.__focused__['border-color'] = BdFocus
        self.__hovered__['border-color'] = BdHover

class TextBox(Widget):
    tag = 'textbox'
    __istext__ = True
    __create__ = tkinter.Text

    # string
    def addText(self, value):
        self.widget.insert('end', value)

    def getText(self):
        return self.widget.get('1.0', 'end')

    def setText(self, value):
        self.widget.delete('1.0', 'end')
        self.widget.insert('end', value)

    # create
    def __init__(self, parent):
        Widget.__init__(self, parent)
        self.style({
            'width': 200,
            'height':  75,
            'color': FgColor,
            'font-size': 10,
            'background': BgEntry,
            'border': 1,
            'border-color': BdColor
        })

class TextView(Widget):
    tag = 'textview'
    __create__ = tkinter.Text
    __istext__ = True

    # string
    def addText(self, value):
        self.widget.configure(state='normal')
        self.widget.insert('end', value)
        self.widget.configure(state='disabled')

    def getText(self):
        return self.widget.get('1.0', 'end')

    def setText(self, value):
        self.widget.configure(state='normal')
        self.widget.delete('1.0', 'end')
        self.widget.insert('end', value)
        self.widget.configure(state='disabled')

    # settings
    def configure(self):
        widget = self.widget
        size = widget.winfo_width(), widget.winfo_height()
        text = self.getText()
        if text != self['.text']:
            self['.text'] = text
            self['-width'], self['-height'] = fontSize(self)
        if (self['-width'], self['-height']) != size:
            widget.place(width=self['-width'], height=self['-height'])

    def __ctrlc__(self, event):
        print(event.keysym, event.char)
        self.window.widget.clipboard_clear()
        self.window.widget.clipboard_append(self.widget.selection_get())

    # create
    def __init__(self, parent):
        Widget.__init__(self, parent)
        self.widget.configure(state='disabled')
        self.__callback__['key'] = self.__ctrlc__
        self['.text'] = self.getText()

class View(Frame):
    # string
    def addText(self, value):
        self.__text__.addText(value)

    def getText(self, value):
        return self.__text__.getText()

    def setText(self, value):
        self.__text__.setText(value)

    # settings
    def update(self):
        self.__text__.style({
            'background': 'white'
        })
        Frame.update(self)

    # create
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.style({
            'width': 300,
            'height': 400
        })
        self.__text__ = TextView(self)

# widget
class Image(Widget):
    tag = 'image'
    __create__ = tkinter.Label
    __istext__ = True

    # defaults
    def __noimage__(self):
        if self['.image']:
            self['.image'] = False
            self.widget.image = ''
            self.widget.configure(image='', text='No image')
        self.style({
            '-width': 100,
            '-height': 100,
            '--color': FgColor,
            '--background': BgColor,
            '--border': 1,
            '--border-color': BdColor
        })

    def __isimage__(self, path=None):
        self['.path'] = path
        try:
            data = open(path, 'rb').read()
            image = tkinter.PhotoImage(data=data)
            self.widget.configure(image=image, text='')
            self.widget.image = image
            self['.image'] = True
            self.style({
                '-width': image.width(),
                '-height': image.height(),
                '--color': None,
                '--background': None,
                '--border': None,
                '--border-color': None
            })
        except:
            self.__noimage__()

    def src(self, path=None):
        if path != None and self['.path'] != path:
            self.__isimage__(path)
        elif not self['.image']:
            self.__noimage__()

    # create
    def __init__(self, parent, file=None):
        Widget.__init__(self, parent)
        self['.image'] = False
        self['.path'] = None
        self.src(file)
        self.__clear__ = self.src

class Link(Label):
    tag = 'link'

    # defaults
    def __openlink__(self, event):
        if re.search('^[a-zA-Z]+://(.*?)', self.url):
            os.system('xdg-open ' + self.url)

    # create
    def __init__(self, parent, url=''):
        Label.__init__(self, parent)
        self.url = url
        self['color'] = FgFocus
        self.focus(color=FgHover)
        self.hover({
            'color': FgHover,
            'cursor': 'pointer'
        })
        self.__callback__['click'] = self.__openlink__

class Line(Widget):
    tag = 'line'
    __create__ = tkinter.Label
    # create
    def __init__(self, parent):
        Widget.__init__(self, parent)
        self.style({
            'width': '100%',
            'height': 1,
            'background': BdColor,
            'margin-top': 5,
            'margin-bottom': 5
        })
