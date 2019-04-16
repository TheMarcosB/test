########################################################
## Module  : Open          ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os

# import default modules
from . import Array, Sys

# fixed variables
_open = open
_etc = Sys.etc + '/'

########################################################
## ------- here starts the module definitions ------- ##
########################################################
def realpath(path):
    for k, v in Array.items(Sys.paths):
        path = path.replace('${%s}' % (k.upper()), v)

    return path

def open(path, mode='r'):
    return _open(realpath(path), mode)

def read(path):
    return open(path).read()

def write(path, content, mode='w'):
    obj = open(path, mode)
    obj.write(content)
    obj.close()

def etc(path, mode='r'):
    return _open(_etc + path, mode)

def etcr(path):
    return _open(_etc + path).read()

def etcw(path, content, mode='w'):
    obj = _open(_etc + path, mode)
    obj.write(content)
    obj.close()
