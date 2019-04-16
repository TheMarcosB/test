########################################################
## Module  : Class         ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from .Main import *
from . import Blocker, Error, Unique

# fixed variables
_hides = ['__blocker__', '__id__', '__list__', '__self__', '__text__']

########################################################
## ------- here starts the module definitions ------- ##
########################################################
# errors
def _blockererror(self, attr, key='__blocker__'):
    Error('blocker', "attribute '%s' blocked in call of '%s' in object '%s'" % (key, attr, clsName(self)))

def _isattrerror(self, key):
    Error('attribute', "attribute '%s' of '%s' object is not writable" % (key, clsName(self)))

def _noattrerror(self, key):
    Error('attribute', "'%s' object has no attribute '%s'" % (clsName(self), key))

# callbacks
def _getattribute(self, key):
    attrs = Object.dict(self)
    if key == '__dict__': return attrs['__dict__']
    elif key in attrs.keys(): return attrs[key]
    else: return Object.get(self, key)

def _hide(items, type='key'):
    devolve = []
    for item in items:
        if isinstance(item, tuple): key, value = item
        else: key = item
        if not key in _hides:
            if type == 'key' and not key in devolve: devolve.append(key)
            elif type == 'item': devolve.append(item)
            elif type == 'value': devolve.append(value)
    return devolve

def _dir(self):
    return _hide(Object.dir(self) + list(Object.dict(self).keys()))

# important
class name:
    def new(name, value=None):
        if value: return '<TheMarcosLib.%s.%s>' % (name.capitalize(), value.capitalize())
        else: return '<TheMarcosLib.%s>' % (name.capitalize())

    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __call__(self, *vals, **keys):
        return name.new(self.name, self.value)

class _dict:
    __repr__ = name('class', 'dict')
    __str__ = __repr__

    def iskey(self, key):
        try: Object.dict(self)[key]
        except: return False
        return True

    def keys(self):
        try: return _hide(Object.dict(self), 'key')
        except: return []

    def values(self):
        try: return _hide(Object.dict(self), 'value')
        except: return []

    def items(self):
        try: return _hide(Object.dict(self), 'item')
        except: return []

    def __delitem__(self, key):
        try:
            attrs = Object.dict(self)
            cls = attrs['__self__']
            if not Blocker.check(cls):
                if key in Object.attrs(cls):
                    _isattrerror(cls, key)
                else:
                    try:
                        del attrs[key]
                        return True
                    except:
                        _noattrerror(cls, key)
            else:
                _blockererror(cls, '__delattr__', key)
        except:
            pass
        return False

    def __getitem__(self, key):
        try:
            attrs = Object.dict(self)
            cls = attrs['__self__']
            try: return attrs[key]
            except: _noattrerror(cls, key)
        except:
            pass

    def __setitem__(self, key, value):
        attrs = Object.dict(self)
        try:
            cls = attrs['__self__']
            if not Blocker.check(cls):
                if key in Object.attrs(cls):
                    _isattrerror(cls, key)
                else:
                    attrs[key] = value
            else:
                _blockererror(cls, '__setattr__', key)
        except KeyError:
            attrs['__self__'] = value

    def __getattribute__(self, key):
        if not key in ['__delattr__', '__getattr__', '__setattr__']:
            if key == '__dict__': return {}
            else: return Object.get(self, key)

    def  __init__(self, cls):
        self['__self__'] = cls

# classes
class new:
    __repr__ = name('class')
    __str__ = __repr__

    def __delattr__(self, key):
        del self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __new__(cls, *vals, **keys):
        # set attributes
        cls.__blocker__ = Blocker.current
        cls.__dir__ = _dir
        cls.__getattribute__ = _getattribute
        # create instance
        self = object.__new__(cls, *vals, **keys)
        # new attributes
        attrs = Object.dict(self)
        attrs['__dict__'] = _dict(self)
        attrs['__id__'] = lockStr(Unique.id())
        attrs['__list__'] = []
        attrs['__name__'] = name.new('class')
        # return instance
        return self

class simple:
    __dir__ = _dir

    def __getattribute__(self, key):
        if key == '__dict__': return {}
        else: return object.__getattribute__(self, key)

# attributes
def isattr(self, key):
    if isinstance(self, new): return self.__dict__.iskey(key)
    else: return Object.exists(self, key)

def delattr(self, key):
    if isinstance(self, new): return new.__delattr__(self, key)
    else: return Object.delete(self, key)

def getattr(self, key):
    if isinstance(self, new): return new.__getattr__(self, key)
    else: return Object.get(self, key)

def setattr(self, key, value):
    if isinstance(self, new): return new.__setattr__(self, key, value)
    else: return Object.set(self, key, value)
