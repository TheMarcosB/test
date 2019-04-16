########################################################
## Module  : GI.interface  ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, re

# import local modules
from . import ParametersCSS, VariablesCSS, Widget
from .. import Array, Image, Number

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# tags
class _tag(str):
    def clear(self):
        self.end, self.length, self.left, self.right, self.top = 0, 0, 0, 0, 0

    @property
    def fixsize(self):
        w, h = self.w, self.h
        bt, br, bb, bl = self.style.borderWidth
        w -= br + bl
        h -= bt + bb
        return w, h

    @property
    def getsize(self):
        w, h = self.fixsize
        pt, pr, pb, pl = self.style.padding
        w -= pr + pl
        h -= pt + pb
        return w, h

    @property
    def fx(self): return self.x + self.style.borderWidth[3]
    @property
    def fy(self): return self.y + self.style.borderWidth[0]
    @property
    def px(self): return self.fx + self.style.padding[3]
    @property
    def py(self): return self.fy + self.style.padding[0]

    def __new__(cls, parent, widget, tag):
        self = str.__new__(cls, tag)
        self.focus, self.show, self.status = False, True, 'normal'
        self.items, self.parent, self.widget = [], parent, widget
        self.image, self.style, self.text = None, widget.style, ''
        self.end, self.length, self.left, self.right, self.top = 0, 0, 0, 0, 0
        self.expand, self.position, self.size = None, (0, 0), (0, 0)
        self.w, self.h = 0, 0
        self.y, self.x = 0, 0
        return self

class _window:
    def clear(self):
        self.end, self.length, self.left, self.right, self.top = 0, 0, 0, 0, 0

    @property
    def w(self): return self.window.widget.winfo_width()
    @property
    def h(self): return self.window.widget.winfo_height()
    @property
    def fixsize(self): return self.w, self.h
    @property
    def getsize(self): return self.w, self.h

    def __init__(self, widget):
        self.items, self.position, self.size, self.window = [], (0, 0), (0, 0), widget
        self.end, self.length, self.left, self.right, self.top = 0, 0, 0, 0, 0
        self.x, self.y, self.fx, self.fy, self.px, self.py  = 0, 0, 0, 0, 0, 0

# count
def _realdefault(key):
    default = ParametersCSS.args[key]
    if type(default) is ParametersCSS.link:
        items, key = ParametersCSS.args[default], default
        default = getItem(items, key.keys)
    return default

def _value(value, args=None):
    try:
        if isinstance(value, Number.inchcalc): return math.floor(value(args))
        elif isinstance(value, Number.percent): return math.floor(value(args[value.token]))
        else: return value
    except:
        pass

def _external(key, tag, internal=False):
    default, value = _realdefault(key), tag.style[key]
    if internal: args = {
        'w': {'l': 0, 'w': tag.w, 'h': tag.h, '%': tag.w},
        'h': {'l': 0, 'w': tag.w, 'h': tag.h, '%': tag.h}
        }
    else: args = {
        'w': {'l': tag.parent.w - tag.parent.length, 'w': tag.parent.w, 'h': tag.parent.h, '%': tag.parent.w},
        'h': {'l': tag.parent.w - tag.parent.length, 'w': tag.parent.w, 'h': tag.parent.h, '%': tag.parent.h}
        }
    if type(default) == ParametersCSS.items:
        default, devolve = default.default, []
        for item in value:
            count, new_item = 0, []
            for i in item:
                try: new_item.append(_value(i, args[default[count].arg]))
                except: new_item.append(_value(i))
                count += 1
            devolve.append(tuple(new_item))
        return tuple(devolve)
    else:
        if isinstance(value, tuple):
            count, devolve = 0, []
            for item in value:
                try: devolve.append(_value(item, args[default[count].arg]))
                except: devolve.append(_value(item))
                count += 1
            return tuple(devolve)
        else:
            try: return _value(value, args[default.arg])
            except: return _value(value)

def _internal(key, tag):
    return _external(key, tag, True)

def _corners(tag):
    devolve = []
    if tag.w > tag.h: args = {'l': 0, 'w': tag.w, 'h': tag.h, '%': tag.w}
    else: args = {'l': 0, 'w': tag.w, 'h': tag.h, '%': tag.h}
    for value in tag.style.borderRadius: devolve.append(_value(value, args))
    return tuple(devolve)

def _margin(tag, auto=False):
    count, devolve = 0, []
    width = {'w': tag.parent.w, 'h': tag.parent.h, '%': tag.parent.w}
    height = {'w': tag.parent.w, 'h': tag.parent.h, '%': tag.parent.h}
    for value in tag.style.margin:
        if count % 2 == 0:
            devolve.append(_value(value, height))
        else:
            if value == 'auto':
                if auto and (type(tag.parent) is _window or tag.parent.style.width != 'auto'): value = (tag.parent.w - tag.w) / 2
                else: value = 0
            devolve.append(_value(value, width))
        count += 1
    return tuple(devolve)

# configure
def _image(window, tag, size, style, text=None):
    image = Image.new(size, style.backgroundColor)
    image.expand(*_external('padding', tag))
    tag.w, tag.h = image.size
    if isinstance(style.backgroundImage, VariablesCSS.linear_gradient):
        image.linear_gradient(style.backgroundImage, style.backgroundImage.position)
    if isinstance(text, Image.Text):
        text.background(image)
        tag.text = tag.widget.value = text.text
    image.canvas(_internal('background-canvas', tag))
    image.corners(*_corners(tag))
    if style.boxShadow[-1] == 'inset': image.shadow_inside(*style.boxShadow)
    image.border(style.borderWidth, style.borderColor, style.borderStyle)
    if style.boxShadow[-1] == 'outset': image.shadow_outside(*style.boxShadow)
    tag.image = image.tkinter()
    window.canvas.itemconfig(tag, image=tag.image, state='normal')
    tag.w, tag.h = image.size

def _widget(window, tag):
    style, modified = tag.style, tag.style.modified()
    if tag.expand: width, height = tag.expand
    else: width, height = _external('size', tag)
    iswidth, isheight = (width != 'auto' and width > 0), (height != 'auto' and height > 0)
    issize = iswidth and isheight
    if isinstance(tag.widget, Widget.label) and (modified or tag.text != tag.widget.value or tag.size != (width, height)):
        tag.size = width, height
        text = Image.Text(tag.widget.value, tag.style)
        textsize = text.getsize
        if width == 'auto': width = textsize[0]
        if height == 'auto': height = textsize[1]
        text.size = width, height
        _image(window, tag, (width, height), style, text)
    elif isinstance(tag.widget, (Widget.canvas, Widget.frame)) and issize and (modified or tag.size != (width, height)):
        _image(window, tag, (width, height), style)
        tag.size = width, height
    elif isinstance(tag.widget, (Widget.canvas, Widget.frame)) and modified and (not iswidth or not isheight):
        tag.size, tag.w, tag.h = (width, height), 0, 0
        window.canvas.itemconfig(tag, state='hidden')
    if tag.expand: tag.expand = False

def _position(window, tag):
    if tag.style.position in ['absolute', 'fixed']:
        if tag.style.position == 'fixed': w, h, x, y = window.tag.getsize + (0, 0)
        else: w, h, x, y = tag.parent.fixsize + (tag.parent.fx, tag.parent.fy)
        top, right, bottom, left = _external('position-items', tag)
        marginTop, marginRight, marginBottom, marginLeft = _margin(tag)
        if right != 'none' and left != 'none':
            fx = left + marginLeft
            tag.x = x + fx
            tag.expand = w - (fx + right + marginRight), tag.size[0]
        elif right != 'none':
            tag.x = x + (w - (right + marginRight + tag.w))
        elif left != 'none':
            tag.x = x + left + marginLeft
        if top != 'none' and bottom != 'none':
            fy = top + marginTop
            tag.y = y + fy
            if tag.expand: tag.expand = tag.expand[0], h - (fx + bottom + marginBottom)
            else: tag.expand = tag.size[0], h - (fx + bottom + marginBottom)
        elif top != 'none':
            tag.y = y + top + marginTop
        elif bottom != 'none':
            tag.y = y + (h - (bottom + marginBottom + tag.h))
        _widget(window, tag)
    else:
        width, height = tag.parent.getsize
        marginTop, marginRight, marginBottom, marginLeft = _margin(tag, True)
        w, h = tag.w + marginRight + marginLeft, tag.h + marginTop + marginBottom
        float = tag.style.float
        if float in ['left', 'right']:
            if (type(tag.parent) is _tag and tag.parent.style.width == 'auto') or width - (tag.parent.length + w) >= 0:
                if float == 'right':
                    tag.x = tag.parent.px + (width - (tag.parent.right + tag.w + marginRight))
                    tag.parent.right += w
                else:
                    tag.x = tag.parent.px + tag.parent.left + marginLeft
                    tag.parent.left += w
                if h > tag.parent.end: tag.parent.end = h
                tag.parent.length += w
            else:
                if float == 'right':
                    tag.x = tag.parent.px + (width - (tag.w + marginRight))
                    tag.parent.left, tag.parent.right = 0, w
                else:
                    tag.x = tag.parent.px + marginLeft
                    tag.parent.left, tag.parent.right = w, 0
                tag.parent.length = w
                tag.parent.top += tag.parent.end
                tag.parent.end = h
        else:
            tag.parent.top += tag.parent.end
            tag.x = tag.parent.px + marginLeft
            tag.parent.left = w
            tag.parent.end = h
        tag.y = tag.parent.py + tag.parent.top + marginTop
    if tag.position != (tag.x, tag.y):
        tag.position = tag.x, tag.y
        window.canvas.coords(tag, tag.x, tag.y)

def _items(window, parent, widget):
    canvas = window.canvas.create_image((0, 0), anchor='nw', state='hidden')
    tag = _tag(parent, widget, canvas)
    parent.items.append(tag)
    if type(widget.items) is Widget._items and len(widget.items) > 0:
        for item in widget.items: _items(window, tag, item)

def _hidden(window, tag):
    window.canvas.itemconfig(tag, state='hidden')
    if isinstance(tag.widget, Widget.frame) and len(tag.items) > 0:
        for item in tag.items: _hidden(window, item, show)

def _config(window, tag):
    if not isinstance(tag.widget, Widget.frame) or (not 'auto' in tag.style.size):
        _widget(window, tag)
        _position(window, tag)
        if isinstance(tag.widget, Widget.frame):
            for item in tag.items: _config(window, item)
    else:
        size = _external('size', tag)
        for item in tag.items: _config(window, item)
        if size == ('auto', 'auto'): tag.expand = tag.length, tag.top + tag.end
        elif size[0] == 'auto': tag.expand = tag.length, size[1]
        else: tag.expand = size[0], tag.top + tag.end
        _widget(window, tag)
        _position(window, tag)
    tag.clear()

def up(window):
    length = window.document.getItems().length
    if window.length != length:
        window.canvas.delete('all')
        window.length = length
        window.tag = _window(window)
        for item in window.document.items: _items(window, window.tag, item)
    for tag in window.tag.items:
        if tag.style.display != 'none':
            if tag.style.position == 'absolute': absolute.append(tag)
            elif tag.style.position == 'fixed': fixed.append(tag)
            else: _config(window, tag)
        else:
            _hidden(window, tag)
    window.tag.clear()
    window.widget.update()
