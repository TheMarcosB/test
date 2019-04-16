########################################################
## Module  : Json          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import local modules
from .Main import *
from . import Array, Class, Error, Open

# fixed variables
_swap_decode = '\\',    '\n',  '\r',  '\t',   '"',   "'"
_swap_encode = '\\\\', '\\n', '\\r', '\\t', '\\"', "\\'"

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def _realdecode(string, isreal):
    if isreal:
        return realStr(string)

    else:
        return swapStr(string, _swap_encode, _swap_decode)

def _realencode(value):
    if value == None:
        return 'null'

    elif isinstance(value, (bool, float, int)):
        return str(value).lower()

    else:
        return '"%s"' % (swapStr(str(value), _swap_decode, _swap_encode))

def encode(self, isspace=True, space=''):
    try:
        iscount = Array.iscount(self)
        devolve = '[' if iscount else '{'
        count = 1
        items = Array.items(self)
        length = len(items)

        if not iscount and isspace and length > 1:
            devolve += '\n'

        for k, v in items:
            if not iscount and isspace and length > 1:
                devolve += space + (' ' * 4)

            if not iscount:
                devolve += _realencode(k) + ': '

            count += 1

            if Array.isarray(v):
                devolve += encode(v, isspace, space + (' ' * 4))

            else:
                devolve += _realencode(v)

            if length >= count:
                if not iscount and isspace:
                    devolve += ',\n'

                else:
                    devolve += ', '

        if not iscount and isspace and length > 1:
            devolve += '\n' + space

        return devolve + (']' if iscount else '}')

    except:
        return '{}'

def decode(string):
    devolve = Array.new()
    # check
    count = 0
    error = None
    status = 0
    # path
    path = []
    pathcount = 0
    prev = None
    # number
    ispoint = False
    isstart = False
    # real
    realkey = False
    realval = False
    # string
    key = None
    value = None
    # split
    opened = []
    closed = string.rfind('}')
    openst = None

    for i in string:
        # main
        if i == '{' and len(opened) == 0: # open
            opened.append(i)

        elif i == '}' and count == closed and key == value == None: # close
            try:
                del opened[0]

            except:
                error = Error('json', error='No close')
                break

        # array open
        elif (i in ['{', '['] and status == 5) or (i == '[' and pathcount == 0 and status == 0):
            if opened[-1] == '[' or status == 0:
                _array = Array.path(devolve, path)
                _index = len(_array)
                _array += Array.new()
                path.append(_index)

            else:
                path.append(_realdecode(key, realkey))
                Array.path(devolve, path, new=Array.new())

            key = None
            value = None
            opened.append(i)
            pathcount += 1
            realkey = False

            if i == '[':
                status = 5

            else:
                status = 0

        # key
        elif i in ['"', "'"] and status == 0 and opened[-1] == '{' and not isstart: # string open
            key = ''
            openst = i
            status = 1

        elif i == openst and status == 1 and key[-1 : ] != '\\': # string close
            status = 2

        elif i.isalpha() and status == 0 and opened[-1] == '{' and not isstart: # alpha
            key = i
            realkey = True
            status = 3

        elif i.isdigit() and status == 0 and opened[-1] == '{': # number
            key = ''

            if isstart:
                key += isstart
                isstart = False

            key += i
            realkey = True
            status = 4

        # split
        elif i == ':' and status in [2, 3, 4]:
            ispoint = False
            status = 5

        # less
        elif i in ['-', '+'] and status in [0, 5]:
            isstart = i

        # value
        elif i in ['"', "'"] and status == 5 and not isstart: # string open
            value = ''
            openst = i
            status = 6

        elif i == openst and status == 6 and value[-1 : ] != '\\': # string close
            status = 7

        elif i.isalpha() and status == 5 and not isstart: # alpha
            value = i
            realval = True
            status = 8

        elif i.isdigit() and status == 5: # number
            value = ''

            if isstart:
                value += isstart
                isstart = False

            value += i
            realval = True
            status = 9

        # key append
        elif status == 1: # string
            key += i

        elif i.isalpha() and status == 3: # alpha
            key += i

        elif (i.isdigit() or (i == '.' and not ispoint)) and status == 4: # number
            key += i

            if i == '.':
                ispoint = True

        # value append
        elif status == 6: # string
            value += i

        elif i.isalpha() and status == 8: # alpha
            value += i

        elif (i.isdigit() or (i == '.' and not ispoint)) and status == 9: # number
            value += i

            if i == '.':
                ispoint = True

        # item close
        elif status in [0, 5, 7, 8, 9] and i in [',', ']', '}']:
            if status > 0:
                if opened[-1] == '[' and value != None:
                    Array.path(devolve, path, add=_realdecode(value, realval))
                    status =  5

                elif not opened[-1] == '[' and key != None and value != None:
                    Array.path(devolve, path + [_realdecode(key, realkey)], new=_realdecode(value, realval))
                    status = 0

                elif (i, prev) == (',', ','):
                    error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
                    break

                elif i == ',':
                    status = 5 if opened[-1] == '[' else 0

            elif (((i == '}' and len(path) == 0) or i == ',') and key == '') or ((i, prev) == (',', ',')):
                error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
                break

            elif i == ',':
                status = 5 if opened[-1] == '[' else 0

            if i in [']', '}']:
                try:
                    if count != closed:
                        del path[-1]

                    del opened[-1]

                except:
                    error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
                    break

            prev = i
            key = None
            value = None
            ispoint = False
            realkey = False
            realval = False

        # array close
        elif i in [']', '}'] and len(path) > 0:
            try:
                del path[-1]
                del opened[-1]
                status = 5 if opened[-1] == '[' else 0

            except:
                error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
                break

        elif not i in ['\n', ' ']:
            error = Error('json', line=string[0 : count].count('\n') + 1, count=count, string=i)
            break

        count += 1

    if not error and not (len(path) == len(opened) == 0):
        error = Error('json', error='no close')

    if error:
        Array.clean(devolve)

    return devolve

def open(path):
    return decode(Open.read(path))

def write(path, array):
    Open.write(path, encode(array))
