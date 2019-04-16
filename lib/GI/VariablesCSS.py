##########################################################
## Module  : GI.VariablesCSS ## Author   : Marcos Bento ##
## ------------------------- ## ----------------------- ##
## Github  : TheMarcosBC     ## Twitter  : TheMarcosBC  ##
## ------------------------- ## ----------------------- ##
## Facebook: TheMarcosBC     ## Instagram: TheMarcosBC  ##
##########################################################
import math, re
# import local modules
from .. import Number, Image

##########################################################
## -------- here starts the module definitions -------- ##
##########################################################
def calc(value):
    return Number.inchcalc(value, 'px', False)

def rgba(*values):
    return Image.Color(values)

def rgb(*values):
    return Image.Color(values)

def alpha(color, value):
    if not isinstance(color, Image.Color): color = Image.Color(color)
    color.alpha(value)
    return color

def light(color, value):
    if not isinstance(color, Image.Color): color = Image.Color(color)
    color.light(value)
    return color

def mix(color, value):
    if not isinstance(color, Image.Color): color = Image.Color(color)
    color.mix(value)
    return color

class linear_gradient(tuple):
    def __new__(cls, value=None, *values):
        position = 'bottom'
        if value.replace('to ', '').strip() in ['top', 'right', 'bottom', 'left']: position = value.replace('to ', '').strip()
        else: values = (value, ) + values
        self = tuple.__new__(cls, values)
        self.position = position
        return self

class transition:
    def _calc(self, current, before, percenter):
        if percenter:
            if percenter[1]: percenter[0] -= 16.6
            else: percenter[0] += 16.6
            if isinstance(current, Number.inchcalc):
                string = current.value
                for val, token in re.findall('(\d+)([^\d]+)', string):
                    number = math.floor(float(val))
                    number = math.floor(min((number / 100) * percenter[0], number))
                    string = string.replace(val + token, str(number) + token)
                return calc(string)
            elif isinstance(current, (float, int)):
                if isinstance(before, Number.inchcalc):
                    string = before.value
                    for val, token in re.findall('(\d+)([^\d]+)', string):
                        number = math.floor(float(val))
                        number = math.floor(min((number / 100) * percenter[0], number))
                        string = string.replace(val + token, str(number) + token)
                    if percenter[0] <= 0 if percenter[1] else percenter[0] >= 100: return current
                    else: return calc(string)
                else:
                    if percenter[1]: return max(min(current + (((before - current) / 100) * percenter[0]), before), current)
                    else: return (max(min(before + (((current - before) / 100) * percenter[0]), current), before))
        else:
            return current

    def _current(self, current, before, percenter):
        if isinstance(current, tuple):
            items = []
            for c, b, p in zip(current, before, percenter):
                if isinstance(c, tuple):
                    item = []
                    for ic, ib, ip  in zip(c, b, p):

                        item.append(self._calc(ic, ib, ip))
                elif c != b:
                    item = self._calc(c, b, p)
                else:
                    item = c
                items.append(item)
            return items
        else:
            return self._calc(current, before, percenter)

    def __call__(self, event):
            if self.percenter >= 116.6: event.stop()
            else: self.percenter += 16.6
            if self.percenter <= 116.6:
                for key, items in self.style:
                    self.widget.style[key] = current = self._current(*items)

    def _inchcalc(self, value):
        devolve = 0
        for number, token in re.findall('(\d+)([^\d]+)', value.value): devolve += float(number)
        return devolve

    def _percenter(self, current, before):
        if isinstance(current, (Number.inchcalc, float, int)) or isinstance(before, (Number.inchcalc, float, int)):
            if isinstance(current, str): current = 0
            elif isinstance(current, Number.inchcalc): current = self._inchcalc(current)
            if isinstance(before, str): before = 0
            elif isinstance(before, Number.inchcalc): before = self._inchcalc(before)
            if current == before: return None
            elif current > before: return [0, 0]
            else: return [100, 1]
        else:
            return None

    def _values(self, current, before, percenter=None):
        if isinstance(current, tuple):
            if percenter == None: percenter = []
            for c, b in zip(current, before):
                if isinstance(c, tuple):
                    item = []
                    for ic, ib in zip(c, b): item.append(self._percenter(ic, ib))
                    percenter.append(item)
                else:
                    percenter.append(self._percenter(c, b))
        else:
            percenter = self._percenter(current, before)
        return current, before, percenter

    def _items(self, style):
        for key, transition in style.items():
            if key[ : 12] == '-transition-':
                current = self.widget.style.get(key[12 : ])
                before = style.get(key[12 : ])
                self.style.append([key[12 : ], self._values(transition, before)])

    def _update(self, up, style):
        devolve = {}
        for key, value in style.items():
            if key[ : 12] == '-transition-':
                up[key[12 : ]] = up[key]
                devolve[key] = value
        return devolve

    def __init__(self, widget, timer=1):
        if widget.style.transition == 'on':
            style = widget.style
            style.modified()
            self.widget = widget
            self.style = []
            if style.status['transition'] == None:
                style.status['transition'] = style.style.copy()
                self._items(style.status['transition'])
            else:
                up = style.status['transition']
                up.update(self._update(up, style.style))
                self._items(up)
                style.status['transition'] = None
            self.percenter = 0
            window = widget.parents[0].window
            window.setInterval(self, timer)
        else:
            del self
