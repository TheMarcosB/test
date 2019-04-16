########################################################
## Module  : System        ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import os, sys
from atexit import register as addexit

# import local modules
from .Main import *
from . import Error

# variables fixed
lib = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(lib)
etc = path + '/etc'
home = os.getenv('HOME')
data = home + '/.TheMarcosData'
paths = {'data': data, 'etc': etc, 'home': home, 'lib': lib, 'sys': path}

########################################################
## ------- here starts the module definitions ------- ##
########################################################
password = Cache(etc + '/password', '123456')
allowApp = Cache(etc + '/allowapp')

# create data folder
if not os.path.isdir(paths['data']):
    os.mkdir(paths['data'])

#  allow application
def allowAppCheck(id):
    if id in allowApp.lines():
        return True

    if input('require password for application: ') == password.read():
        allowApp.newline(id)
        addexit(lambda: allowApp.delline(id))
        return True

    else:
        Error('allow', 'permission denied, password required!', type='application')
        sys.exit()
