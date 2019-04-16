########################################################
## Module  : GI.DefaultCSS ## Author   : Marcos Bento ##
## ------------------------## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from . import Event
from .VariablesCSS import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
default = {
    'button': {
        'color': 'black',
        'font-size': 14,
        'text-align': 'center',
        'height': 14,
        'line-height': 14,
        'padding': (5, 10),
        'background-color': '#dfdfdf',
        'border': (1, 'inbutton', '#9f9f9f')
    },
    'check': {
      'width': 12,
      'height': 12,
      'background-color': '#f5f5f5',
      'border': (1, 'solid', '#bfbfbf'),
      '-on-background-canvas': ('rectangle', 2, 2, calc('100% - 4px'), calc('100% - 4px'), 'green', '')
    },
    'radio': {
      'width': 12,
      'height': 12,
      'background-color': '#f5f5f5',
      'border': (1, 'solid', '#bfbfbf'),
      'border-radius': '50%',
      '-on-background-canvas': ('ellipse', 2, 2, calc('100% - 4px'), calc('100% - 4px'), 'green', '')
    },
    'slider':  {
      'width': 32,
      'height': 16,
      'background-color': '#f5f5f5',
      'border': (1, 'solid', '#bfbfbf'),
      'border-radius': '50h',
      'background-canvas': ('ellipse', calc('(100w - 100h) + 2px'), 2, calc('100h - 4px'), calc('100% - 4px'), 'gray', ''),
      '-on-background-canvas': ('ellipse', 2, 2, calc('100h - 4px'), calc('100% - 4px'), 'green', ''),
      '-off-background-canvas': ('ellipse', calc('(100w - 100h) + 2px'), 2, calc('100h - 4px'), calc('100% - 4px'), 'gray', '')
    },
}

def status(self):
    if self.getAttr('status') == 'on':
        self.setAttr('status', 'off')
        self.style['background-canvas'] = self.style['-off-background-canvas']
    else:
        self.setAttr('status', 'on')
        self.style['background-canvas'] = self.style['-on-background-canvas']

def slider(self):
    if self.getAttr('status') == 'on':
        self.setAttr('status', 'off')
        self.style['-transition-background-canvas'] = self.style['-off-background-canvas']
        transition(self, 20)
    else:
        self.setAttr('status', 'on')
        self.style['-transition-background-canvas'] = self.style['-on-background-canvas']
        transition(self, 20)

def up(widget):
    try:
        widget.style(default[widget.tagName])
        if widget.tagName == 'button':
            widget.value = 'Button' + str(widget.parents[0].getByTag('button').length + 1)
            widget.focus({'border': (1, 'outbutton', '#9f9f9f')})
        if widget.tagName == 'slider':
            Event.setdef(widget.on, 'click', slider)
        elif widget.tagName in ['check', 'radio']:
            Event.setdef(widget.on, 'click', status)
        if widget.tagName in ['button', 'check', 'radio', 'slider']: widget.hover({'border': (1, 'solid', '#9f9f9f')})
    except:
        pass
