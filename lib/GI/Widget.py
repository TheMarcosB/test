########################################################
## Module  : GI.Widget     ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules

# import local modules
from . import DefaultCSS, Event, Style
from .. import Class, Unique
from ..Main import *

# fixed variables
_lock = [
    # main
    '__id__', 'on', 'parent', 'tagName',
    # style
    'focus', 'hover', 'style',
    # attributes
    'delAttr', 'getAttr', 'setAttr',
    # items
    'getByClass', 'getById', 'getByName', 'getByTag', 'getItems', 'index', 'items'
]

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# bases
class _attribute(Class.simple):
    def append(self, name, value):
        Object.dict(self)[name] = value

    def delete(self, name):
        try: del Object.dict(self)[name]
        except: return False
        return True

    def __call__(self, key, default=None):
        return Object.dict(self).get(key, default)

class _base(Class.simple):
    @property
    def className(self): return self.getAttr('class')
    @property
    def className(self, value): self.setAttr('class', value)
    @property
    def id(self): return self.getAttr('id')
    @property
    def id(self, value): self.setAttr('id', value)
    @property
    def name(self): return self.getAttr('name')
    @property
    def name(self, value): self.setAttr('name', value)

    @property
    def parents(self):
        devolve = []
        while True:
            devolve.append(self)
            try: self = self.parent
            except: break
        return list(reversed(devolve))

    # attributes
    def __getattr__(self, key, default=None):
        try: return object.__getattr__(self, key)
        except: return default

    def __setattr__(self, key, value):
        if key in _lock:
            if self.__getattr__(key, _base) == _base:
                object.__setattr__(self, key, value)
        else:
            object.__setattr__(self, key, value)

    # string
    def __repr__(self):
        return '<Element%s>' % self.tagName.capitalize()

    def __str__(self):
        return self.__repr__()

    # main
    def delete(self):
        return self.parent.item.delete(self)

    def __init__(self, name):
        self.tagName = lockStr(name.lower())
        self.__id__ = lockStr(Unique.id())
        self.getAttr = _attribute()
        self.delAttr = self.getAttr.delete
        self.setAttr = self.getAttr.append
        self.on = Event.new()
        self.style = Style.new()
        self.focus = self.style.focus
        self.hover = self.style.hover

class _items:
    # items
    def __find__(self, key, tag):
        if type in ['id', 'name']: devolve = None
        else: devolve = _items()
        for item in reversed(self.__items__):
            try:
                if tag == 'tag' and key == item.tagName: devolve.__items__.append(item)
                elif tag == 'id' and key == item.getAttr('id'): devolve = item
                elif tag == 'class':
                    names, count = item.getAttr('name'), 0
                    for name in names:
                        if name + ' ' in key + ' ': count += 1
                    if count == len(names): devolve.__items__.append(item)
                elif tag == 'name' and key == item.getAttr('name'): devolve = item
                elif tag == 'type' and key == item.getAttr('type'): devolve.__items__.append(item)
            except:
                pass
            if isinstance(item.items, _items) and item.items.length > 0:
                if tag in ['id', 'name']: devolve = item.items.__find__(key, tag)
                else: devolve.__items__ += item.items.__find__(key, tag).__items__
        return devolve

    def getItems(self):
        devolve = _items()
        for item in self.__items__:
            devolve.append(item)
            if isinstance(item.items, _items) and item.items.length > 0:
                devolve.__items__ += item.getItems().__items__
        return devolve

    def getByClass(self, key):
        return self.__find__(key, 'class')

    def getById(self, key):
        return self.__find__(key, 'id')

    def getByName(self, key):
        return self.__find__(key, 'name')

    def getByTag(self, key):
        return self.__find__(key, 'tag')

    # index
    def index(self, widget):
        if isinstance(widget, _base):
            index = 0
            for item in self.__items__:
                if widget.__id__ == item.__id__:
                    return index
                index += 1
        return -1

    def __getitem__(self, index):
        try: return self.__items__[index]
        except: pass

    # iterator
    def __iter__(self):
        return self.__items__.__iter__()

    def __len__(self):
        return self.__items__.__len__()

    def __next__(self):
        return self.__items__.__next__()

    # widget
    def append(self, widget):
        if isinstance(widget, _base):
            self.__items__.append(widget)

    def delete(self, widget):
        if isinstance(widget, _base):
            try:
                index = 0
                for item in self.__items__:
                    if widget.__id__ == item.__id__:
                        del self.__items__[index]
                        return True
                    else:
                        if widget.items.length > 0:
                            if widget.items.delete(widget):
                                return True
                    index += 1
            except:
                return False

    # string
    def __repr__(self):
        return self.__items__.__repr__()

    def __str__(self):
        return self.__items__.__str__()

    # main
    @property
    def length(self):
        return len(self.__items__)

    def __init__(self, widget=None):
        self.__items__ = []
        if widget:
            widget.items = self
            widget.getItems = self.getItems
            widget.getByClass = self.getByClass
            widget.getById = self.getById
            widget.getByName = self.getByName
            widget.getByTag = self.getByTag
            widget.index = self.index

# widgets
class canvas(_base):
    def tagItems(self):
        devolve = []
        for item in self.items: devolve.append(item[ : -1])
        return devolve

    def createTag(self, tag, w, h, x, y, color, id=None, text=''):
        self.items.append([tag, w, h, x, y, color, text, id])
        self.style.backgroundCanvas = self.tagItems()

    def clearTags(self):
        self.items.clear()
        self.style.backgroundCanvas = None

    def deleteTag(self, key):
        try:
            if isinstance(key, int):
                del self.items[key]
            else:
                index = 0
                for item in self.items:
                    if key == item[-1]: del self.items[index]
                    index += 1
        except:
            pass

    def tagEdit(self, key, **argsk):
        index = 0
        for item in self.items:
            if key == index if isinstance(key, int) else key == item[-1]:
                count = 1
                for k in ['w', 'h', 'x', 'y', 'color']:
                    try: self.items[index][count] = argsk[k]
                    except: pass
                    count += 1
                break
            index += 1

    def tagSize(self, key, w, h):
        self.tagEdit(key, w=w, h=h)

    def tagPosition(self, key, x, y):
        self.tagEdit(key, x=x, y=y)

    def tagColor(self, key, color):
        self.tagEdit(key, color=color)

    def __init__(self, name):
        _base.__init__(self, name)
        self.items = []

class label(_base):
    @property
    def value(self): return self.getAttr('value', '')
    @value.setter
    def value(self, value): self.setAttr('value', value)
    @property
    def length(self): return len(self.value)

class text(label):
    pass

class entry(text):
    pass

class image(_base):
    @property
    def src(self): return self.getAttr('src', '')
    @src.setter
    def src(self, value): self.setAttr('src', value)

# create
class frame(_base):
    def createTag(self, name):
        name = name.lower()
        if name in ['canvas', 'check', 'radio', 'slider']:  widget = canvas(name)
        elif name in ['button', 'label', 'title', 'tag']: widget = label(name)
        elif name == 'entry': widget = entry(name)
        elif name == 'text': widget = text(name)
        elif name in 'image': widget = image(name)
        elif name == 'video': widget = video(name)
        else: widget = frame(name)
        widget.parent = self
        DefaultCSS.up(widget)
        self.items.append(widget)
        return widget

    @property
    def length(self): return self.items.length

    def __init__(self, name):
        _base.__init__(self, name)
        _items(self)
