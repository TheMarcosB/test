###################################################################
## Module  : Image             ## Author   : Marcos Bento        ##
## --------------------------- ## ------------------------------ ##
## Github  : TheMarcosBC       ## Twitter  : TheMarcosBC         ##
## --------------------------- ## ------------------------------ ##
## Facebook: TheMarcosBC       ## Instagram: TheMarcosBC         ##
###################################################################

# import default modules
import math, os
from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps, ImageTk

# import local modules
from .Main import *
from . import Error, Unique

# fixed variables
__cache__ = {}
Transparent = 127, 127, 127, 0

###################################################################
## ------------ here starts the module definitions ------------- ##
## start ##########################################################
def _reversed(self, old_colors, new_colors):
    new_image = self.copy()
    new_data = []
    for color in self.getdata():
        try: new_data.append(new_colors[old_colors.index(color)])
        except:
            try: new_data.append(old_colors[new_colors.index(color)])
            except: new_data.append(color)
    new_image.putdata(new_data)
    return new_image

# corners
def getcorners(values):
    corners = []
    for i in range(4):
        if isinstance(values, (float, int)):
            corners.append(round(values))
        else:
            try:
                try: corner = round(values[i])
                except: corner = round(values[1 if i == 3 else 0])
                corners.append(corner)
            except:
                if corners:
                    corners.append(corners[0])
                else:
                    corners = [0, 0, 0, 0]
                    break
    return tuple(corners)

def _corner(size, length, position):
    width, height = size
    rw, rh = length
    bw, bh = rw * 2, rh * 2
    new_image = Image.new('L', size, 255)
    draw = ImageDraw.Draw(new_image)
    draw.polygon([(0, 0), (rw, 0), (0, rh)], 0)
    draw.ellipse((0, 0, bw, bh), 255)
    if position == 'right': new_image = ImageOps.mirror(new_image)
    elif position == 'bottom': new_image = new_image.rotate(180)
    elif position == 'left': new_image = ImageOps.mirror(new_image.rotate(180))
    return new_image

def _calcorners(size, values):
    w, h = size
    dw, dh = w / 2, h / 2
    pw, ph = (w * 2) / math.pi, (h * 2) / math.pi
    t, r, b, l = values
    # top
    if t >= w or r >= w or (t >= dw and r >= dw): tw = round(pw * math.atan(t / max(r, 0.1)))
    else: tw = round(t)
    if t >= h or l >= h or (t >= dh and l >= dh): th = round(ph * math.atan(t / max(l, 0.1)))
    else: th = round(t)
    # right
    if r >= w or t >= w or (r >= dw and t >= dw): rw = round(pw * math.atan(r / max(t, 0.1)))
    else: rw = round(r)
    if r >= h or b >= h or (r >= dh and b >= dh): rh = round(ph * math.atan(r / max(b, 0.1)))
    else: rh = round(r)
    # bottom
    if b >= w or l >= w or (b >= dw and l >= dw): bw = round(pw * math.atan(b / max(l, 0.1)))
    else: bw = round(b)
    if b >= h or r >= h or (b >= dh and r >= dh): bh = round(ph * math.atan(b / max(r, 0.1)))
    else: bh = round(b)
    # left
    if l >= w or b >= w or (l >= dw and b >= dw): lw = round(pw * math.atan(l / max(b, 0.1)))
    else: lw = round(l)
    if l >= h or t >= h or (l >= dh and t >= dh): lh = round(ph * math.atan(l / max(t, 0.1)))
    else: lh = round(l)
    # devolve
    return (tw, th), (rw, rh), (bw, bh), (lw, lh)

def _cornersmask(size, corners, isrealcorners):
    # big size
    bigsize = round(size[0] * 4), round(size[1] * 4)
    # big corners
    if isrealcorners:
        ts, rs, bs, ls = corners
    else:
        bigcorners = corners[0] * 4, corners[1] * 4, corners[2] * 4, corners[3] * 4
        ts, rs, bs, ls = _calcorners(bigsize, bigcorners)
    # mask
    mask = Image.new('L', bigsize, 255)
    if ts[0] > 0 and ts[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, ts, 'top'))
    if rs[0] > 0 and rs[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, rs, 'right'))
    if bs[0] > 0 and bs[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, bs, 'bottom'))
    if ls[0] > 0 and ls[1] > 0: mask = ImageChops.difference(mask, _corner(bigsize, ls, 'left'))
    # devolve
    return (mask.resize(size, Image.ANTIALIAS), (ts, rs, bs, ls)) + size

def _newcorners(self, size):
    new_size = size[0] + size[1]
    old_size = self._corners[2] + self._corners[3]
    corners = []
    for width, height in self._corners[1]:
        if old_size > new_size:
            less = old_size - new_size
            width -= less
            height -= less
        else:
            more = new_size - old_size
            width += more
            height += more
        corners.append((max(width, 0), max(height, 0)))
    return _cornersmask(size, tuple(corners), True)

def _upcorners(self, size):
    if self._corners:
        self._corners = _newcorners(self, size)
        new_image = Image.new('RGBA', size)
        new_image.paste(self._image, (0, 0), self._corners[0])
        self._image = new_image

def _uppadding(self, *values):
    self._padding[0] += values[0]
    self._padding[1] += values[1]
    self._padding[2] += values[2]
    self._padding[3] += values[3]

def _upsize(self, size):
    self._size = size
    self._padding = [0, 0, 0, 0]
    self._position = [0, 0]

# color
def getrgba(value):
    if isinstance(value, (list, tuple)):
        new_color = []
        for i in range(4):
            try:
                val = value[i]
                if i == 3: new_color.append(getNum(math.floor(255 * val) if isinstance(val, float) else val, 0, 255))
                else: new_color.append(getNum(round(value[i]), 0, 255))
            except IndexError as error:
                if i == 3: new_color.append(255)
                else: raise ValueError
        return tuple(new_color)
    else:
        if value == 'transparent':
            return Transparent
        elif value[0] == '#':
            if len(value) == 4: return ImageColor.getrgb('#' + (value[1 : ] * 2)) + (255, )
            elif len(value) == 7: return ImageColor.getrgb(value) + (255, )
            else: return ImageColor.getrgb(value[ : 7]) + (getNum(int(value[8 : ], 16), 0, 255), )
        else:
            return ImageColor.getrgb(value) + (255, )

class Color(tuple):
    # formats
    @property
    def hexa(self): return '#%02x%02x%02x%02x' % self.rgba

    @property
    def hex(self): return self.hexa[0 : 7]

    @property
    def rgb(self): return tuple(list(self.rgba)[0 : 3])

    # update
    def clear(self):
        self.rgba = tuple(self)

    def light(self, value):
        r, g, b, a = self
        if value < 0:
            r, g, b = round(r - (abs(value) * r)), round(g - (abs(value) * g)), round(b - (abs(value) * b))
        else:
            r, g, b = round(r + (value * (255 - r))), round(g + (value * (255 - g))), round(b + (value * (255 - b)))
        self.rgba = getNum(r, 0, 255), getNum(g, 0, 255), getNum(b, 0, 255), a
        return self

    def mix(self, color, value=0.5):
        color, rgb, value = Color.__color__(color), (), getOne(value)
        for i in range(3): rgb += round(color[i] + (self[i] - color[i]) * value),
        self.rgba = rgb + (self[3], )
        return self

    def alpha(self, value):
        value = round(getOne(value) * 255)
        self.rgba = tuple(list(self)[0 : 3] + [value])
        return self

    # main
    def __color__(value):
        if isinstance(value, Color):
            return value.rgba
        else:
            try: return getrgba(value)
            except: return Transparent

    def __new__(cls, value):
        color = Color.__color__(value)
        self = tuple.__new__(cls, color)
        self.rgba = color
        return self

def getcolor(value):
    return Color.__color__(value)

# create
class _Image:
    # background
    def append(self, image, x=0, y=0):
        bg = self._image.crop((x, y, image.size[0] + x, image.size[1] + y))
        self._image.paste(Image.alpha_composite(bg, image._image), (x, y))
        return self

    def canvas(self, items):
        if len(items) > 0:
            width, height = self.size
            canvas = Image.new('RGBA', (math.floor(width * 4), math.floor(height * 4)), Transparent)
            draw = ImageDraw.Draw(canvas)
            for name, x, y, w, h, color, text in items:
                x, y, w, h = math.floor(x * 4), math.floor(y * 4), math.floor(w * 4), math.floor(h * 4)
                if name =='rectangle': draw.rectangle((x, y, x + w, y + h), color)
                elif name == 'ellipse': draw.ellipse((x, y, x + w, y + h), color)
            self._image = Image.alpha_composite(self._image, canvas.resize((width, height), Image.ANTIALIAS))

    def expand(self, *values):
        corners = getcorners(values)
        if corners != (0, 0, 0, 0):
            (w, h), (t, r, b, l) = self.size, corners
            new_size = math.floor(w + r + l), math.floor(h + t + b)
            new_image = Image.new('RGBA', new_size, self._color.rgba)
            new_image.paste(self._image, (t, l))
            self._image = new_image
            _uppadding(self, t, r, b, l)
            _upcorners(self, new_size)
        return self

    def fill(self, color):
        self._color = Color(color)
        new_image = Image.new('RGBA', self.size, self._color.rgba)
        self._image = Image.alpha_composite(new_image, self._image)
        return self

    def repeat(self, size, mode='normal', x=0, y=0):
        old_image, old_size = self._image, self._image.size
        if mode in ['loop-round', 'loop-stretch']:
            w2, h2 = math.floor(old_size[0] / 3), math.floor(old_size[1] / 3)
            w0, h0 = w2 * 3, h2 * 3
            xl, yl = math.floor(size[0] / w2), math.floor(size[1] / h2)
            w1, h1 = w2 * xl, h2 * yl
            # get image
            old_image = old_image.resize((w0, h0), Image.ANTIALIAS)
            new_image = Image.new('RGBA', (w1, h1))
            # get sides
            top = old_image.crop((w2, 0, w0 - w2, h2))
            right = old_image.crop((w0 - w2, h2, w0, h0 - h2))
            bottom = old_image.crop((w2, h0 - h2, w0 - w2, h0))
            left = old_image.crop((0, h2, w2, h0 - h2))
            # add sides
            if mode == 'loop-round':
                for x in range(xl - 2):
                    new_image.paste(top, (w2 * (x + 1), 0))
                    new_image.paste(bottom, (w2 * (x + 1), h1 - h2))
                for y in range(yl - 2):
                    new_image.paste(left , (0, h2 * (y + 1)))
                    new_image.paste(right, (w1 - w2, h2 * (y + 1)))
            else:
                new_image.paste(top.resize((w1 - (w2 * 2), h2), Image.ANTIALIAS), (w2, 0))
                new_image.paste(bottom.resize((w1 - (w2 * 2), h2), Image.ANTIALIAS), (w2, h1 - h2))
                new_image.paste(right.resize((w2, h1 - (h2 * 2)), Image.ANTIALIAS), (w1 - w2, h2))
                new_image.paste(left.resize((w2, h1 - (h2 * 2)), Image.ANTIALIAS), (0, h2))
            # corners
            new_image.paste(old_image.crop((0, 0, w2, h2)))
            new_image.paste(old_image.crop((w0 - w2, 0, w0, h2)), (w1 - w2, 0))
            new_image.paste(old_image.crop((w0 - w2, h0 - h2, w0, h0)), (w1 - w2, h1 - h2))
            new_image.paste(old_image.crop((0, h0 - h2, w2, h0)), (0, h1 - h2))
            copy = new_image.copy()
            w3, h3 = w1 - (w2 * 2), h1 - (h2 * 2)
            pw, ph = math.floor(w3 *(100 / w1)), math.floor(h3 *(100 / h1))
            while w3 > w0 and h3 > h0:
                new_image.paste(copy.resize((w3, h3), Image.ANTIALIAS), (math.floor((w1 - w3) / 2), math.floor((h1 - h3) / 2)))
                w3, h3 = math.floor((w3 / 100) * pw), math.floor((h3 / 100) * ph)
            new_image.paste(old_image.resize((w3, h3), Image.ANTIALIAS), (math.floor((w1 - w3) / 2), math.floor((h1 - h3) / 2)))
            self._image = new_image.resize(size, Image.ANTIALIAS)
            _upsize(self, size)
        else:
            w0, h0, w1, h1 = old_size + size
            if mode in ['repeat', 'repeat-x', 'repeat-y', 'round', 'round-x', 'round-y']:
                if mode in ['round', 'round-x', 'round-y']:
                    w0, h0 = math.floor(w1 / 2 if w1 / 1.5 >= w0 else w0), math.floor(h1 / 2 if h1 / 1.5 >= h0 else h0)
                    xl, yl = math.floor(w1 / w0), math.floor(h1 / h0)
                    w0, h0 = min(w0 + round((w1 - (w0 * xl)) / xl), w1), min(h0 + round((h1 - (h0 * yl)) / yl), h1)
                    old_image = old_image.resize((w0, h0), Image.ANTIALIAS)
                    new_image = Image.new('RGBA', (w0 * xl, h0 * yl))
                else:
                    xl, yl = round(w1 / w0) + 1, round(h1 / h0) + 1
                    new_image = Image.new('RGBA', size)
                for x in range(xl):
                    if mode in ['repeat-x', 'round-x']:
                        new_image.paste(old_image, (round(w0 * x), 0))
                    else:
                        for y in range(yl): new_image.paste(old_image, (round(w0 * x), round(h0 * y)))
                        if mode in ['repeat-y', 'round-y']: break
                if mode in ['round', 'round-x', 'round-y']: self._image = new_image.resize(size, Image.ANTIALIAS)
                else: self._image = new_image
                _upsize(self, size)
            elif size + (x, y) != old_size + (0, 0):
                new_image = Image.new('RGBA', size)
                new_image.paste(old_image, (x, y))
                self._image = new_image
                _upsize(self, size)
        return self

    def linear_gradient(self, values, position='bottom'):
        if isinstance(values, tuple) and len(values) >= 2:
            old_image, new_image = self._image.copy(), Image.new('RGBA', self.size)
            colors, newdata, positions = [], [], ['bottom', 'top', 'left', 'right']
            (width, height), isx, count = old_image.size, position in positions[2 : 4], len(values)
            length, items = width if isx else height, count - 1
            for i in range(count):
                try:
                    color, percentage = values[i]
                    if isx:
                        w = round((width / 100) * min(max(percentage, 1), 100))
                        more = round((width - w) / count)
                        value = (w + more, height), more, color
                        width -= w + more
                        length -= w + more
                    else:
                        h = round((height / 100) * min(max(percentage, 1), 100))
                        more = round((height - h) / count)
                        value = (width, h + more), more, color
                        height -= h + more
                        length -= h + more
                    items -= 1
                except:
                    color = values[i]
                    if i >= count - 2:
                        if isx: w, h, percentage = length, height, length
                        else: w, h, percentage = width, length, length
                    else:
                        if isx:
                            w, h = round(width / items), height
                            length -= w
                            percentage = w
                        else:
                            w, h = width, round(height / items)
                            length -= h
                            percentage = h
                    value = (w, h), percentage, color
                colors.append(value)
            for i in range(len(colors) - 1):
                ((w, h), percentage, color), mix = colors[i : i + 2]
                color, less, mix, value = Color(color), 100 / percentage, mix[2], 100
                if isx:
                    for x in range(w):
                        newdata.append(color.mix(mix, value / 100).rgba)
                        if x >= w - percentage: value -= less
                else:
                    for y in range(h):
                        newdata += [color.mix(mix, value / 100).rgba] * w
                        if y >= h - percentage: value -= less
            if isx: newdata = newdata * old_image.size[1]
            if position in positions[1 : 3]: newdata = list(reversed(newdata))
            new_image.putdata(newdata)
            new_image = Image.alpha_composite(old_image, new_image)
            try: self._image.paste(new_image, (0, 0), self._corners[0])
            except: self._image = new_image
        return self

    def shadow_inside(self, x, y, blur, solid, color, *argsv):
        if x > 0 or y > 0 or blur > 0:
            (w, h), color = self._image.size, Color(color)
            weight = round(blur + solid)
            shadow = Image.new('RGBA', (w + (weight * 2), h + (weight * 2)), color)
            rectsize = round((w - (solid * 2))), round((h - (solid * 2)))
            rectx = x + ((shadow.size[0] - rectsize[0]) / 2)
            recty = y + ((shadow.size[1] - rectsize[1]) / 2)
            rect = Image.new('RGBA', rectsize, color.alpha(0).rgba)
            if self._corners: shadow.paste(rect, (round(rectx), round(recty)), _newcorners(self, rectsize)[0])
            else: shadow.paste(rect, (round(rectx), round(recty)))
            if blur > 0:
                blur = round((255 if blur > 255 else blur) / 3.5)
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
            new_image = Image.new('RGBA', (w, h))
            new_image.paste(shadow, (-weight, -weight))
            new_image = Image.alpha_composite(self._image, new_image)
            if self._corners:
                corners = Image.new('RGBA', (w, h))
                corners.paste(new_image, (0, 0), self._corners[0])
                new_image = corners
            self._image = new_image
        return self

    # border
    def border(self, values, color='transparent', style='solid', image=None):
        corners = getcorners(values)
        if corners != (0, 0, 0, 0):
            old_image, old_size = self._image, self._image.size
            (w0, h0), (t, r, b, l) = old_size, corners
            new_size = old_size[0] + r + l, old_size[1] + t + b
            (w1, h1), color = new_size, Color(color)
            # by style
            if style in ['inbutton', 'outbutton', 'inset', 'outset']:
                big_size = math.floor(w1 * 3), math.floor(h1 * 3)
                (w1, h1), t1, r1, b1, l1 = big_size, math.floor(t * 3), math.floor(r * 3), math.floor(b * 3), math.floor(l * 3)
                new_border = Image.new('RGBA', big_size, color.rgba)
                draw = ImageDraw.Draw(new_border)
                color = 'white' if style in ['inbutton', 'outbutton'] else color.light(0.5).rgba
                if style in ['inbutton', 'inset']: draw.polygon([(0, 0), (w1 - 1, 0), (w1 - r1, t1), (l1, h1 - b1), (0, h1 - 1)], color)
                elif style in ['outbutton', 'outset']: draw.polygon([(w1, h1), (w1 - 1, 0), (w1 - r1, t1), (l1, h1 - b1), (0, h1 - 1)], color)
                new_image = new_border.resize(new_size, Image.ANTIALIAS)
            else:
                new_image = Image.new('RGBA', new_size, color.rgba)
                # by image
                if image:
                    image = image._image.convert('RGBA').resize(new_size, Image.ANTIALIAS)
                    new_image = Image.alpha_composite(new_image, image)
            # new image
            new_image.paste(self._image, (l, t), self._image)
            self._image = new_image
            self._position[0] += l
            self._position[1] += t
            _upcorners(self, new_size)
            # devolve
        return self

    def corners(self, *values):
        corners = getcorners(values)
        if corners == (0, 0, 0, 0):
            self._corners = None
        else:
            old_size = self._image.size
            self._corners = _cornersmask(old_size, corners, False)
            new_image = Image.new('RGBA', old_size)
            new_image.paste(self._image, (0, 0), self._corners[0])
            self._image = new_image
        return self

    def shadow_outside(self, x, y, blur, solid, color, inset=False):
        if x > 0 or y > 0 or blur > 0:
            (w, h), color = self._image.size, Color(color)
            weight = round((blur / 2) + solid)
            width, height, = w + (weight * 2), h + (weight * 2)
            morex = abs(x) - weight if abs(x) >= weight else 0
            morey = abs(y) - weight if abs(y) >= weight else 0
            shadow = Image.new('RGBA', (round(width + morex), round(height + morey)), color.alpha(0).rgba)
            rectsize = round(width - blur), round(height - blur)
            rectx = shadow.size[0] - (rectsize[0] + (blur / 2)) if x > -1 else (blur / 2)
            recty = shadow.size[1] - (rectsize[1] + (blur / 2)) if y > -1 else (blur / 2)
            rect = Image.new('RGBA', rectsize, color)
            if self._corners: shadow.paste(rect, (round(rectx), round(recty)), _newcorners(self, rectsize)[0])
            else: shadow.paste(rect, (round(rectx), round(recty)))
            if blur > 0:
                blur = round((255 if blur > 255 else blur) / 3.5)
                shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
            centerx = round((shadow.size[0] - w) / 2)
            centery = round((shadow.size[1] - h) / 2)
            if -centerx >= x: x = centery * 2
            else: x = 0 if x >= centerx else centerx
            if -centery >= y: y = centery * 2
            else: y = 0 if y >= centery else centery
            new_image = shadow
            if self._corners:
                new_image.paste(self._image, (x, y), self._corners[0])
                self._corners = _newcorners(self, shadow.size)
            else:
                new_image.paste(self._image, (x, y))
            if x < 0:
                x = abs(x)
                self.x -= x
                self._position[0] += x
            if y < 0:
                y = abs(y)
                self.y -= y
                self._position[1] += y
            self._image = new_image
        return self

    # filter
    def blur(self, value):
        self._image = self._image.filter(ImageFilter.GaussianBlur(round(getOne(value) * 100)))
        return self

    def brightness(self, value):
        self._image = ImageEnhance.Brightness(self._image).enhance(round(getOne(value) * 100))
        return self

    def opacity(self, value):
        newdata = []
        for item in self._image.getdata():
            r, g, b, a = item
            alpha = max(math.floor(getOne(value) * a), 0)
            newdata.append((r, g, b, alpha))
        self._image.putdata(newdata)
        return self

    # resize
    def crop(self, w, h, x=0, y=0):
        if not self.size == (w, h) and self.size[0] >= w and self.size[1] >= h:
            self._image = self._image.crop((x, y, x + w, y + h))
            _upsize(self, self._image.size)
        return self

    def resize(self, *argsv, **argsk):
        image = self._image
        mode = argsk.get('mode', getItem(argsv, 1, 'fill'))
        width, height = image.size
        # get size
        new_width = getItem(argsk.get('size'), 0, argsk.get('width', getItem(argsv, (0, 0))))
        new_height = getItem(argsk.get('size'), 1, argsk.get('height', getItem(argsv, (0, 1))))
        # resize
        if new_width != None or new_height != None:
            # from fill
            if mode == 'fill' and new_width != None and new_height != None:
                size = math.floor(new_width), math.floor(new_height)
                if (width, height) != size:
                    self._image = image.resize(size, Image.ANTIALIAS)
                    _upsize(self, self._image.size)
            else:
                # real size
                real_width = new_height if new_width == None else new_width
                real_height = new_width if new_height == None else new_height
                # from height
                if (real_width > real_height) if mode == 'contain' else ((width > height and new_height != None) or new_width == None):
                    h = real_height if mode == 'contain' else new_height
                    w = width * (h / height)
                    if mode != 'contain' and new_width == None:
                        new_width = w
                    elif mode != 'contain' and new_width > w:
                        w = new_width;
                        h = height * (w / width)
                # from width
                else:
                    w = real_width if mode == 'contain' else new_width
                    h = height * (w / width)
                    if mode != 'contain' and new_height == None:
                        new_height = h
                    elif mode != 'contain' and new_height > h:
                        h = new_height
                        w = width * (h / height)
                # new image
                if mode in ['contain', 'cover']:
                    # position
                    x = round(-((w - real_width) / 2) if w > real_width else (real_width - w) / 2)
                    y = round(-((h - real_height) / 2) if h > real_height else (real_height - h) / 2)
                    # create
                    self._image = Image.new('RGBA', (round(real_width), round(real_height)))
                    self._image.paste(image.resize((round(w), round(h)), Image.ANTIALIAS), (round(x), round(y)))
                else:
                    # create
                    self._image = image.resize((round(w), round(h)), Image.ANTIALIAS)
                _upsize(self, self._image.size)
        return self

    def rotate(self, rotate):
        try:
            self._image = self._image.rotate(rotate)
            _upsize(self, self._image.size)
        except:
            pass
        return self

    # main
    def tkinter(self):
        return ImageTk.PhotoImage(self._image)

    def copy(self):
        image = _Image(self._image.copy(), self._color.rgba)
        image._size = self._size
        image._padding, image._position = self._padding, self._position
        image.x, image.y = self.x, self.y
        return image

    def save(self, *argsv, **argsk):
        self._image.save(*argsv, **argsk)

    def show(self):
         self._image.show()

    @property
    def size(self):
        return self._image.size

    def __init__(self, image, color):
        self._image, self._size = image,  image.size
        self._corners, self._color = None, Color(color)
        self._padding, self._position = [0, 0, 0, 0], [0, 0]
        self.x, self.y = 0, 0

class Text(dict):
    # sizes
    def charsize(self, char):
        if not self.font:
            fontfile = '/' + self['font-family']
            try:
                if self['font-style']: fontfile += '-' + self['font-style']
                if self['font-weight']: fontfile += '-' + self['font-weight']
                fontfile += '.ttf'
                if self['path']: self.font = ImageFont.truetype(os.path.realpath(self['path']) + fontfile, self['font-size'])
                else: self.font = ImageFont.truetype(Paths.etc + '/fonts' + fontfile, self['font-size'])
            except:
                 try: self.font = ImageFont.truetype(Paths.etc + '/fonts/arial.ttf', self['font-size'])
                 except: self.font = ImageFont.truetype(Paths.etc + '/fonts/arial.ttf', 13)
        size = self.font.getsize(char)
        return size[0] + self['letter-spacing'], size[1]

    def height(self):
        return self['line-height'] if isinstance(self['line-height'], int) else self['font-size']

    def textsize(self, text):
        lines = text.splitlines()
        if len(lines) > 1:
            width, height = 0, 0
            for line in lines:
                if line != '':
                    length = 0
                    for char in line: length += self.charsize(char)[0]
                    if length > width: width = length
                height += self.height()
            return width, height
        else:
            length = 0
            for char in text: length += self.charsize(char)[0]
            return length, self.height()

    @property
    def getsize(self):
        try:
            return self._textsize
        except:
            self._textsize = self.textsize(self.text)
            return self._textsize

    # lines
    def _realx(self, length):
        devolve = 0
        if self['text-align'] == 'right': devolve = math.floor(self.getsize[0] - length)
        elif self['text-align'] == 'center': devolve = math.floor((self.getsize[0] - length) / 2)
        return max(devolve, 0)

    def _length(self, line, length, y, isjump):
        string, status, start, end = line, 1, None, None
        delete = self.backspace != None or self.delete != None
        paste = self.backspace if self.backspace != None else self.delete
        ispaste = delete and isinstance(paste, str) and paste != ''
        if isinstance(self.bar, tuple):
            bx, by = max(self.bar[0], 0), max(self.bar[1], 0)
            if y + self.height() >= by:
                count, length, string, x = 0, 0, '', self._realx(length)
                if line == '':
                    start = end = x
                    self.barBack = self.barCurrent = self.barNext = x, y
                else:
                    for char in line:
                        add, charSize = True, self.charsize(char)[0]
                        if x + (charSize / 2) >= bx and start == None:
                            start = end = x
                            if delete:
                                try:
                                    if self.backspace != None:
                                        endSize = self.charsize(string[-1])[0]
                                        length -= endSize
                                        start -= endSize
                                        end -= endSize
                                        string = string[0 : -1]
                                        try: self.barBack = max(start - self.charsize(string[-1])[0], 0), y
                                        except: pass
                                        self.barNext = start + charSize, y
                                    else:
                                        if ispaste:
                                            char = paste[0]
                                            charSize = self.charsize(char)[0]
                                            start += charSize
                                            end += charSize
                                            self.barBack = x, y
                                            try: self.barNext = x + charSize + self.charsize(line[count + 1])[0], y
                                            except: pass
                                        else:
                                            add = False
                                            try: self.barBack = max(start - self.charsize(string[-1])[0], 0), y
                                            except: pass
                                            self.barNext = start + charSize, y
                                    barCurrent = start, y
                                except:
                                    pass
                                self.backspace, self.delete = None, None
                        if add:
                            length += charSize
                            string += char
                        x += charSize
                        count += 1
                self.bar = True
        elif isinstance(self.select, tuple):
            height = self.height()
            (x1, y1, x2, y2), x = self.select, self._realx(length)
            istop, isbottom = y >= y1 and y < y1 + height, y2 > y1 + height and y + height >= y2
            if istop or isbottom:
                string, length = '', 0
                if line != '':
                    for char in line:
                        charSize = self.charsize(char)[0]
                        if (istop and x >= x1) or (isbottom and x <= x2):
                            self.selectText += char
                            if start == None:
                                if istop and ispaste: string += paste
                                start = x
                            if not delete:
                                string += char
                                length += charSize
                        else:
                            if isbottom and x > x2 and end == None: end = x
                            string += char
                            length += charSize
                        x += charSize
                elif istop and ispaste: string += paste
                if length == 0:
                    if delete: status = 0
                    else: start, end = x, x + self.charsize('  ')[0]
                elif istop: end = x
                if isbottom:
                    self.select = True
                    if isinstance(self.first, str):
                        status = 0
                        self._text(self.first + string)
                    if line == '': self.realText += '\n'
                elif istop and ispaste:
                    status = 0
                    if y2 > y1 + height:
                        self.first = string
                    else:
                        self.select = True
                        self._text(string)
            elif y > y1:
                string, start, end = line, x, x + length
                if line == '': end += self.charsize('  ')[0]
                if delete: status = 0
        if status == 1:
            x = self._realx(length)
            self.lines.append((string, (x, self.y), (start, end)))
            self.y += self.height()
            if self.select or self.bar:
                self.realText += string
                if isjump:
                    if end and end >= x + length:
                        self.selectText += '\n'
                        if not delete: self.realText += '\n'
                    else: self.realText += '\n'

    def _text(self, text):
        (width, height), y, h = self.getsize, 0, self.height()
        for line in text.splitlines():
            if self['word-break'] in ['break-all', 'keep-all']:
                countSpace, length, spaces, string = 1, 0, line.split(' '), ''
                for space in spaces:
                    if countSpace != len(spaces): space += ' '
                    if self['word-break'] == 'break-all':
                        charLength, charString= 0, ''
                        for char in space:
                            charSize = self.charsize(char)[0]
                            if charSize + charLength > width:
                                self._length(charString, charLength, y, False)
                                charString, charLength = char, charSize
                                y += h
                            else:
                                charString += char
                                charLength += charSize
                    else:
                        string, length = space, self.textsize(space)[0]
                    if length + charLength > width:
                        self._length(string, length, y, False)
                        string, length = charString, charLength
                        y += h
                    else:
                        string += charString
                        length += charLength
                    countSpace += 1
                self._length(string, length, y, True)
                y += h
            else:
                self._length(line, self.textsize(line)[0], y, True)
                y += h

    def _image(self, x=0, y=0):
        self.first, self.lines, self.selectText, self.y = None, [], '', 0
        if self.bar: self.select = None
        delete = self.backspace != None or self.delete != None
        self._text(self.text)
        if (self.select or self.bar) and delete: self.text, self.realText = self.realText, ''
        else: self.realText = ''
        if self.select and delete: self.select = None
        blur, color, h = 0, getcolor(self['color']), self['font-size']
        top = math.floor(((self['line-height'] - h) / 2) - 1) if isinstance(self['line-height'], int) else 0
        # size
        pt, pr, pb, pl = getcorners(self['padding'])
        try: width = self.size[0] + pr + pl
        except: width = self.getsize[0] + pr + pl
        try: height = self.size[1] + pt + pb
        except: height = self.getsize[1] + pt + pb
        size = width, height
        # background and bar
        bg, shadowBg = Image.new('RGBA', size, Transparent), None
        barColor, draw = getcolor(self['bar-color']), ImageDraw.Draw(bg)
        # select
        if self.select:
            selectColor, selectFgColor = getcolor(self['select-background']), Color(self['select-color'])
            selectBg = Image.new('RGBA', size, Transparent)
            selectText = Image.new('RGBA', size, selectFgColor.alpha(0).rgba)
            selectDraw, selectTextDraw = ImageDraw.Draw(selectBg), ImageDraw.Draw(selectText)
        # shadow
        try:
            sx, sy, blur, shadowColor = self['text-shadow']
            sx, sy, blur, shadowColor = int(sx), int(sy), max(int(blur), 0), Color(shadowColor)
            if sx > 0 or sy > 0 or blur > 0:
                shadowBg = Image.new('RGBA', size, shadowColor.alpha(0).rgba)
                shadowDraw = ImageDraw.Draw(shadowBg)
        except:
             pass
        # lines
        for line, (lx, ly), (start, end) in self.lines:
            lx += pl + x; ly += pt + y
            if ly >= 0 and ly <= height:
                selected = start != None and end != None
                if selected: start += pl + x; end += pl + x
                if self.select and selected:
                    selectDraw.rectangle((start, ly, end, ly + h + self['line-height']), selectColor)
                if line.strip() != '':
                    for char in line:
                        charSize = self.font.getsize(char)[0] + self['letter-spacing']
                        if lx + charSize >= 0 and lx <= width:
                            if self.bar and selected and lx >= start and lx <= end:
                                draw.rectangle((lx - 1, ly + top, lx - 1, ly + top + h + 2), barColor)
                            if shadowBg: shadowDraw.text((lx + sx, ly + sy + top), char, shadowColor, font=self.font)
                            if self.select and selected and lx >= start and lx <= end:
                                selectTextDraw.text((lx, ly + top), char, selectFgColor, font=self.font)
                            else:
                                draw.text((lx, ly + top), char, color, font=self.font)
                        lx += charSize
                elif self.bar and selected:
                    draw.rectangle((lx, ly + top, lx, ly + top + h + 2), barColor)
        # merge
        if shadowBg and blur > 0: shadowBg = shadowBg.filter(ImageFilter.GaussianBlur(blur / 3))
        if self.select:
            if shadowBg: selectBg = Image.alpha_composite(selectBg, shadowBg)
            new_image = Image.alpha_composite(selectBg, selectText)
            new_image = Image.alpha_composite(new_image, bg)
        else:
            if shadowBg: new_image = Image.alpha_composite(shadowBg, bg)
            else: new_image = bg
        # clear
        self.backspace, self.delete = None, None
        self.bar, self.select = None, None
        self['width'], self['height'], self.font = None, None, None
        del self.first
        del self.lines
        del self.y
        del self._textsize
        # devolve
        return new_image

    # main
    def __getitem__(self, key):
        try:
            value = self.attr[key]
            if value != None: return value
            else: return self.get(key)
        except:
            return self.get(key)

    def show(self, scroll=(0, 0)):
        self._image(*scroll).show()

    def image(self, scroll=(0, 0)):
        return _Image(self._image(*scroll), 'transparent')

    def background(self, image, scroll=(0, 0)):
        self['padding'] = image._padding
        self._textsize = self.size = image._size
        bg = Image.new('RGBA', image.size)
        bg.paste(self._image(*scroll), tuple(image._position))
        image._image =  Image.alpha_composite(image._image, bg)
        return image

    def __init__(self, text='', style={}):
        self.font, self.realText = None, ''
        self.backspace, self.delete = None, None
        self.bar, self.select, self.selectText = None, None, ''
        self.style, self.attr, self.text = self.update, style, text
        self.barCurrent, self.barBack, self.barNext = (0, 0), (0, 0), (0, 0)
        self.update({
            # main
            'bar-color': 'black',
            'line-height': 0,
            'padding': 0,
            'select-background': 'blue',
            'select-color': 'white',
            # font
            'color': 'black',
            'font-family': 'arial',
            'font-path': None,
            'font-size': 15,
            'font-style': '',
            'font-weight': '',
            # text
            'text-align': 'left',
            'text-shadow': None,
            # word
            'letter-spacing': 0,
            'word-break': 'normal',
            'word-spacing': 0,
        })

def draw(image):
    return ImageDraw.Draw(image._image)

def new(size, color='transparent'):
    return _Image(Image.new('RGBA', size, Color(color).rgba), color)

# open file
def open(path):
    return _Image(Image.open(path).convert('RGBA'), 'transparent')
