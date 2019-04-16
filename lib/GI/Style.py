########################################################
## Module  : GI.Style      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, os, re
from PIL import ImageFont

# import local modules
from . import ParametersCSS, VariablesCSS
from .. import Array, Class, Image, Number
from ..Main import *

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def _token(string):
    try:
        value, *args = re.split('([^\d.]+)', string)
        token = args[0] if len(args) > 0 else None
        float(value)
        if token in ['%', 'w', 'h', 'l']: return 'percent', token
        elif token in Number._inchtypes.keys(): return 'inch', token
        elif not token: return 'string', ''
        else: return 'other', ''
    except:
        return 'other', ''

def _realcomplete(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 2: return tuple(value * 2)
        elif len(value) == 3: return tuple(value) + (value[1], )
        else: return value
    else: return (value, ) * 4

def _realkey(key):
    devolve = ''
    for char in key:
        if char.isupper(): devolve += '-' + char.lower()
        else: devolve += char
    return devolve

def _realvalue(default, value):
    isauto = type(default) in [ParametersCSS.auto, ParametersCSS.inch, ParametersCSS.number]
    try:
        # complete
        if type(default) is ParametersCSS.complete:
            new_value, value = [], _realcomplete(value)
            for v, d in zip(value, default):
                v = _realvalue(d, v)
                if v != None: new_value.append(v)
                else: raise ValueError
            return tuple(new_value)
        elif type(default) is ParametersCSS.color and isinstance(value, (str, tuple)):
            if isinstance(value, Image.Color): return value.rgba
            else: return Image.getrgba(value)
        elif type(default) is ParametersCSS.image and isinstance(value, VariablesCSS.linear_gradient):
            return value
        elif isinstance(default, (ParametersCSS.image, ParametersCSS.path)) and isinstance(value, str) and default.exists(value):
            return os.path.realpath(value)
        # number
        elif type(default) is float and isinstance(value, (float, int)):
            return getOne(value)
        elif isauto and isinstance(value, (Number.inchcalc, Number.percent)):
            return value
        elif (type(default) is int or isauto) and isinstance(value, (float, int)):
            return math.floor(value)
        elif (type(default) is int or isauto) and isinstance(value, str):
            if isinstance(default, (ParametersCSS.auto, ParametersCSS.number)) and value in default.allowed:
                return value
            else:
                _type, token = _token(value)
                if _type == 'percent' and isauto: return Number.percent(value, token)
                elif _type == 'inch': return math.floor(Number.inch(value, 'px'))
                elif _type == 'string': return math.floor(float(value))
        # string
        elif isinstance(default, ParametersCSS.allow) and isinstance(value, str) and value in default.allowed:
            return value
        elif type(default) is str and isinstance(value, str):
            return value
    except:
        pass

def _realitem(default, value):
    try:
        if type(default) is ParametersCSS.items and isinstance(value, (list, tuple)):
            new_value = []
            for items in value:
                new_item = []
                for i, d in zip(items, default.default):
                    i = _realvalue(d, i)
                    if i != None: new_item.append(i)
                    else:
                        new_value = _realitem(default.default, value)
                        if new_value != None: return (new_value, )
                        else: raise ValueError
                new_value.append(tuple(new_item))
            return tuple(new_value)
        elif type(default) is tuple and isinstance(value, (list, tuple)):
            if len(default) == len(value):
                new_value = []
                for v, d in zip(value, default):
                    v = _realvalue(d, v)
                    if v != None: new_value.append(v)
                    else: raise ValueError
                return tuple(new_value)
            else:
                raise ValueError
        else:
            return _realvalue(default, value)
    except:
        pass

def _copy(self):
    devolve, keys = {}, self.keys()
    for key, value in self.items():
        if not ('-on-' + key in keys or '-off-' + key in keys):  devolve[key] = value
    return devolve

def _clear(self):
    delete, keys = [], self.keys()
    for key in keys:
        if not ('-on-' + key in keys or '-off-' + key in keys): delete.append(key)
    for key in delete: del self[key]

# create new style
class new(Class.simple, dict):
    # itmes
    def __getitem__(self, key, isattr=False):
        try:
            return Object.dict(self)['style'][key]
        except:
            try:
                if key[ : 4] == '-on-': default = ParametersCSS.args[key[4 : ]]
                elif key[ : 5] == '-off-': default = ParametersCSS.args[key[5 : ]]
                elif key[ : 12] == '-transition-':
                    if key[12 : ] != 'background-canvas':
                        default = self.style.get(key[12 : ], ParametersCSS.args[key[12 : ]])
                    else:
                        default = ParametersCSS.args[key[12 : ]]
                else: default = ParametersCSS.args[key]
                if not isattr and (key[ : 4] == '-on-' or key[ : 5] == '-off-' or key[ : 12] == '-transition-') and not type(default) is ParametersCSS.link:
                    raise KeyError
                if isinstance(default, (ParametersCSS.complete, ParametersCSS.items)): return tuple(default)
                elif type(default) is ParametersCSS.link:
                    if key[ : 4] == '-on-': key = '-on-' + default
                    elif key[ : 5] == '-off-': key = '-off-' + default
                    elif key[ : 12] == '-transition-': key = '-transition-' + default
                    else: key = default
                    return getItem(self.__getitem__(key), default.keys)
                elif isinstance(default, (ParametersCSS.path, ParametersCSS.string)): return str(default)
                else: return default
            except:
                pass

    def __getattr__(self, key):
        return self.__getitem__(_realkey(key))

    def __setitem__(self, key, value):
        try:
            if value == None:
                raise ValueError
            else:
                if key[ : 4] == '-on-': default = ParametersCSS.args[key[4 : ]]
                elif key[ : 5] == '-off-': default = ParametersCSS.args[key[5 : ]]
                elif key[ : 12] == '-transition-': default = ParametersCSS.args[key[12 : ]]
                else: default = ParametersCSS.args[key]
                if type(default) is ParametersCSS.font:
                    if not value + '.ttf' in os.listdir(self['font-path']): raise ValueError
                elif type(default) is ParametersCSS.link:
                    if key[ : 4] == '-on-': key = '-on-' + default
                    elif key[ : 5] == '-off-': key = '-off-' + default
                    elif key[ : 12] == '-transition-': key = '-transition-' + default
                    else: key = default
                    default, keyItem = self.__getitem__(key, True), default
                    defaultItem = getItem(default, keyItem.keys)
                    item = _realitem(defaultItem, value)
                    if item == None: item = defaultItem
                    value = setItem(default, keyItem.keys, item)
                else: value = _realitem(default, value)
                if value != None: Object.dict(self)['style'][key] = value
                else: raise ValueError
        except:
            try: del Object.dict(self)['style'][key]
            except: pass

    def __setattr__(self, key, value):
        self.__setitem__(_realkey(key), value)

    # status
    def focus(self, *argsv, **argsk):
        try:
            Object.dict(self)['status']['focus'].update(argsk)
            if len(argsv) > 0: Object.dict(self)['status']['focus'].update(argsv[0])
        except:
            pass

    def hover(self, *argsv, **argsk):
        try:
            Object.dict(self)['status']['hover'].update(argsk)
            if len(argsv) > 0: Object.dict(self)['status']['hover'].update(argsv[0])
        except:
            pass

    # update
    def modified(self):
        devolve = Object.dict(self)['style'] != Object.dict(self)['before']
        if devolve: Object.dict(self)['before'] = dict.copy(Object.dict(self)['style'])
        return devolve

    def update(self, mode='normal'):
        try:
            status = self.status[mode]
            if status != None and mode == 'normal':
                _clear(self.style)
                self.style.update(status)
                self.status['normal'] = None
            elif status and len(status) > 0:
                if self.status['normal'] == None: self.status['normal'] = _copy(self.style)
                _clear(self.style)
                self.style.update(self.status['normal'])
                self(status)
        except:
            pass

    # main
    def __call__(self, value):
        if Array.iskeys(value):
            for k, v in Array.items(value):
                self.__setitem__(k, v)

    def __init__(self):
        Object.dict(self)['before'] = None
        Object.dict(self)['style'] = {}
        Object.dict(self)['status'] = {
            'focus': {},
            'hover': {},
            'normal': None,
            'transition': None
        }
