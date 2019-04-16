########################################################
## Module  : GI.Event      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import tkinter

# import local modules
from ..Main import *
from .. import Class

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class new(Class.simple):
    def __delattr__(self, key):
        try: del Object.dict(self)['__callback__'][key]
        except: pass

    def __getattr__(self, key):
        return Object.dict(self)['__callback__'].get(key)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setattr__(self, key, value):
        Object.dict(self)['__callback__'][key] = value

    def __call__(self, key, value):
        self.__setattr__(key, value)

    def __init__(self):
        Object.dict(self)['__callback__'] = {}
        Object.dict(self)['__default__'] = {}

def deldef(self, key):
    try: del Object.dict(self)['__default__'][key]
    except: pass

def getdef(self, key):
    return Object.dict(self)['__default__'].get(key)

def setdef(self, key, value):
    Object.dict(self)['__default__'][key] = value

class call:
    def status(self, tag, status, items=None):
        for item in items if items else self.window.tag.items:
            if tag.widget.__id__ == item.widget.__id__:
                item.status = status
                item.style.update(status)
                if status == 'focus':
                    item.focus = True
                    if self.focused and self.focused != item:
                        self.focused.status = 'normal'
                        self.focused.focus = False
                        self.focused.style.update('normal')
                    self.focused = item
                else:
                    self.hovered = item
            elif status != 'focus' and item.focus and item.style.status['focus']:
                if item.status != 'focus':
                    item.status = 'focus'
                    item.style.update('focus')
            elif item.status != 'normal':
                item.status = 'normal'
                item.focus = False
                item.style.update('normal')
            if len(item.items) > 0: call.status(self, tag, status, item.items)

    def command(self, event, tag, action):
        if action == 'click': self.status(tag, 'focus')
        elif action == 'move': self.status(tag, 'hover')
        if isinstance(tag.widget, tkinter.Tk):
            widget = tag
        else:
            widget = tag.widget
            widget.event = event
            script = widget.getAttr('on' + action.title())
        default = getdef(widget.on, action)
        user = widget.on[action]
        if default: default(widget)
        if user: user(widget)
        self.event = None

    def position(self, event, action, _items=None):
        if isinstance(_items, list):
            items = _items
            tags = []
        else:
            main = self.window
            items = main.tag.items
            tags = [main]
        if len(items) > 0:
            for tag in items:
                try:
                    x = event.x >= tag.x and tag.x + tag.w >= event.x
                    y = event.y >= tag.y and tag.y + tag.h >= event.y
                    scroll = tag.style['scroll'] in ['on', 'x', 'y'] if action == 'scroll' else True
                    if tag.show and x and y and scroll:
                        tags.append(tag)
                        if len(tag.items) > 0: tags += call.position(self, event, action, tag.items)
                except:
                    pass

        if isinstance(_items, list): return tags
        else: return tags[-1]

    def click(self, event): self.command(event, self.position(event, 'click'), 'click')

    def move(self, event): self.command(event, self.position(event, 'move'), 'move')

    def scroll(self, event, up):
        try:
            widget = self.position(event, 'scroll')
            data = widget.__mtk_data__
            scroll = widget.style('scroll')
            x = widget.style('scroll-x')
            y = widget.style('scroll-y')
            scrollX = x if type(x) is int else 0
            scrollY = y if type(y) is int else 0

            if not data.is_scroll and scroll and scroll in ['on', 'x', 'y']:
                data.is_scroll = True

                if scroll == 'x':
                    left = data.position[4]
                    size = data.size[2]

                    if up and scrollX < 0:
                        more = 50 if scrollX + 50 <= 0 else data.scroll[1]
                        widget.style('scroll-x', scrollY + more)

                    elif not up and left - size > 0:
                        less = 50 if left - size > 50 else left - size

                        if left - size > 50:
                            data.scroll[1] = less

                        widget.style('scroll-x', scrollX + -less)

                else:
                    top = data.top
                    size = data.size[3]

                    if up and scrollY < 0:
                        post = scrollY + 50 if scrollY + 50 <= 0 else 0
                        widget.style('scroll-y', post)

                    elif not up and scrollY > -(top - size):
                        post = scrollY + -50 if (top - size) + scrollY > 50 else -(top - size)
                        widget.style('scroll-y', post)

            try:
                self.window.event = event
                data.callback['scroll']()
                self.window.event = None

            except:
                pass

        except Exception as error:
            self.__mtk_error__('scroll', error, widget)

        self.move(event)

    def scrollUp(self, event):
        self.scroll(event, True)

    def scrollDown(self, event):
        self.scroll(event, False)

    def __init__(self, window):
        self.window = window
        self.hovered = None
        self.focused = None
        self.window.canvas.bind('<Button-1>', self.click)
        self.window.canvas.bind('<Motion>', self.move)
        self.window.canvas.bind('<Button-4>', self.scrollUp)
        self.window.canvas.bind('<Button-5>', self.scrollDown)
