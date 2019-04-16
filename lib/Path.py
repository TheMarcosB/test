########################################################
## Module  : Path          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import math, os, re, sys

# import local modules
from . import Number

# fixed variables
_bytes = bytes
_list = list
_type = type

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def split(path):
    dirpath = os.path.dirname(path)
    dirname = os.path.basename(dirpath)
    filename = os.path.basename(path)

    if os.path.isdir(path):
        name = filename
        extension = 'x-directory'

    else:
        name, _extension = os.path.splitext(filename)

        if _extension != '':
            extension = _extension[1 : ].lower()

        else:
            extension = 'x-unknown'

    return name, extension, filename, dirname, dirpath

def bytes(path):
    devolve = b''

    if path and os.path.isfile(path):
        try:
            devolve = open(path, 'rb')

        except:
            pass

    return devolve

def read(path):
    return bytes(path).read()

def length(path):
    devolve = 0

    if os.path.isfile(path):
        try:
            devolve = os.path.getsize(path)

        except:
            pass

    return devolve

def size(path):
    return Number.bytes(length(path))

def mime(path):
    _extension = split(path)[1] if path else 'x-unknown'
    _mime = Conf.sys('mimes').find(extension)
    return _mime[0] if _mime else 'application/octet-stream'

def type(path):
    _extension = split(path)[1] if path else 'x-unknown'
    _type = Conf.sys('types').find(extension)
    return _type[0] if _type else 'other'

def order(_type=None):
    _type = _type if _type else 'x-unknown'

    if _type and os.path.exists(_type) and _type not in Conf.sys('types').data.keys():
        _type = type(_type)

    _order = Conf.sys('order').find(_type)
    return _order[0] if _order else 'x'

def about(path=None):
    name, extension, filename, dirname, dirpath = split(path)
    _type = type(path)
    data = {
        'name': name,
        'extension': extension,
        'file': filename,
        'directory': dirname if path else '',
        'path': path,
        'mime': mime(path),
        'type': _type,
        'order': order(_type),
        'size': bytes(path)
    }
    return data

def list(path=None, _filter=False, hidden=True, ignore={}, local=''):
    ig = ignore if Type(ignore) is dict else {}
    keys = ig.keys()
    directory = sorted(os.listdir(path + '/' + local)) if path and os.path.isdir(path) else None;
    files = []

    if directory and len(directory) > 0:
        for i in directory:
            location = i if local == '' else local + '/' + i
            _path = path + '/' + location
            no_dir = i not in ig['directory'] if os.path.isdir(_path) and 'directory' in keys and Type(ig['directory']) in [List, tuple] else True
            no_file = i not in ig['file'] if os.path.isfile(_path) and 'file' in keys and Type(ig['file']) in [List, tuple] else True
            no_hide = hidden if i[0 : 1] == '.' else True
            no_type = split(_path)[1] not in ig['extension'] if 'extension' in keys and Type(ig['extension']) in [List, tuple] else True

            if  no_dir and no_file and no_hide and no_type:
                _about = about(_path)

                if _about:
                    if os.path.isfile(_path):
                        _about['tags'] = local.split('/')

                    files.append(_about)

                    if os.path.isdir(_path) and _filter:
                        files += list(path, True, hidden, ignore, location)

    return Search.new(files) if local == '' else files
