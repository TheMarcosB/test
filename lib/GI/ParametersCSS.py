###########################################################
## Module  : GI.ParametersCSS ## Author   : Marcos Bento ##
## -------------------------- ## ----------------------- ##
## Github  : TheMarcosBC      ## Twitter  : TheMarcosBC  ##
## -------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC      ## Instagram: TheMarcosBC  ##
###########################################################

# import default modules
import os

# import local modules
from .. import Image

###########################################################
## -------- here starts the module definitions --------- ##
###########################################################
class allow(str):
    def __new__(cls, allowed, value=''):
        self = str.__new__(cls, value)
        self.allowed = allowed
        return self

class color(tuple):
    def __new__(cls, value):
        return tuple.__new__(cls, Image.getrgba(value))

class string(allow):
    def __new__(cls, value, allowed):
        return allow.__new__(cls, allowed, value)

# path
class font(str):
    def exists(self, path):
        return self in os.listdir(path)

class path(str):
    def __new__(cls, value):
        self = str.__new__(cls, value)
        self.exists = os.path.isdir
        return self

class image(str):
    def __new__(cls, value):
        self = str.__new__(cls, value)
        self.exists = os.path.isfile
        return self

# items
class complete(tuple):
    def __new__(cls, *argsv):
        return tuple.__new__(cls, argsv)

class link(str):
    def __new__(cls, key, *argsv):
        self = str.__new__(cls, key)
        self.keys = argsv
        return self

class items(tuple):
    def __new__(cls, default):
        self = tuple.__new__(cls)
        self.default = default
        return self

# number
class auto(str):
    def __new__(cls, value, allowed, arg):
        self = str.__new__(cls, value)
        self.allowed = allowed
        self.arg = arg
        return self

class inch(int):
    def __new__(cls, value, arg):
        self = int.__new__(cls, value)
        self.arg = arg
        return self

class number(int):
    def __new__(cls, value, arg):
        self = int.__new__(cls, value)
        self.allowed = ['auto']
        self.arg = arg
        return self

# defaults
border = ['solid', 'inbutton', 'outbutton', 'inset', 'outset']
canvas = ['ellipse', 'image', 'line', 'rectangle', 'text']
corners = ['top', 'right', 'bottom', 'left']
filters = ['blur', 'brightness', 'contrast', 'grayscale', 'invert', 'opacity', 'saturate', 'sepia']
repeat = ['loop-round', 'loop-stretch', 'repeat', 'repeat-x', 'repeat-y', 'round', 'round-x', 'round-y']
size = ['contain', 'cover', 'fill']
x = ['top', 'center', 'bottom']
y = ['right', 'center', 'left']
args = {
    # widget
    'size': (auto('auto', ['auto'], 'w'), auto('auto', ['auto'], 'h')),
    'width': link('size', 0),
    'height': link('size', 1),
    'box-shadow': (0, 0, 0, 0, color('black'), string('outset', ['inset', 'outset'])),
    'cursor': 'arrow',
    'display': string('block', ['block', 'none']),
    'float': string('normal', ['left', 'normal', 'right']),
    'opacity': 1.0,
    'position': string('none', ['absolute', 'fixed', 'none']),
    'position-items': (auto('none', ['none'], 'h'), auto('none', ['none'], 'w'), auto('none', ['none'], 'h'), auto('none', ['none'], 'w')),
    'top': link('position-items', 0),
    'right': link('position-items', 1),
    'bottom': link('position-items', 2),
    'left': link('position-items', 3),
    'transition': string('on', ['on', 'off']),
    # background
    'background-attachment': string('scroll', ['fixed', 'scroll']),
    'background-canvas': items((allow(canvas), inch(0, 'w'), inch(0, 'h'), inch(0, 'w'), inch(0, 'h'), color('black'), '')),
    'background-color': color('transparent'),
    'background-filter': items((allow(filters), 0.0)),
    'background-image': image(''),
    'background-repeat': string('no-repeat', repeat),
    'background-position': (auto('left', x, 'w'), auto('top', y, 'h')),
    'background-size': (auto('auto', size, 'w'), auto('auto', size, 'h')),
    # border
    'border': (complete(0, 0, 0, 0), string('solid', border), color('black')),
    'border-color': link('border', 2),
    'border-width': link('border', 0),
    'border-style': link('border', 1),
    'border-top': link('border', 0, 0),
    'border-right': link('border', 0, 1),
    'border-bottom': link('border', 0, 2),
    'border-left': link('border', 0, 3),
    'border-radius': complete(inch(0, 'h'), inch(0, 'w'), inch(0, 'h'), inch(0, 'w')),
    'border-radius-top': link('border-radius', 0),
    'border-radius-right': link('border-radius', 1),
    'border-radius-bottom': link('border-radius', 2),
    'border-radius-left': link('border-radius', 3),
    # margin
    'margin': complete(inch(0, 'h'), number(0, 'w'), inch(0, 'h'), number(0, 'w')),
    'margin-top': link('margin', 0),
    'margin-right': link('margin', 1),
    'margin-bottom': link('margin', 2),
    'margin-left': link('margin', 3),
    # padding
    'padding': complete(inch(0, 'h'), inch(0, 'w'), inch(0, 'h'), inch(0, 'w')),
    'padding-top': link('padding', 0, 0),
    'padding-right': link('padding', 0, 1),
    'padding-bottom': link('padding', 0, 2),
    'padding-left': link('padding', 0, 3),
    # image
    'filter': items((allow(filters), 0.0)),
    'object-fit': string('contain', size),
    'object-position': (auto('center', x, 'w'), auto('center', y, 'h')),
    # font
    'color': color('black'),
    'font-size': inch(13, 'h'),
    'font-family': font('sans'),
    'font-path': path(''),
    'font-style': allow(['italic', 'oblique']),
    'font-weight': allow(['bold']),
    'line-height': auto('none', ['none'], 'h'),
    # text
    'text-align': string('left', ['left', 'right', 'center', 'justify']),
    'text-decoration': string('none', ['line-through', 'none', 'overline', 'underline']),
    'text-shadow': (0, 0, 0, color('black')),
    # word
    'letter-spacing': 0,
    'word-break': string('none', ['break-all', 'keep-all', 'none']),
    'word-spacing': 0,
}
