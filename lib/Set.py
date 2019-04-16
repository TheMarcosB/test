########################################################
## Module  : Settings      ## Author   : Marcos Bento ##
## ----------------------- ## ----------------------- ##
## Github  : TheMarcosBC   ## Twitter  : TheMarcosBC  ##
## ----------------------- ## ----------------------- ##
## Facebook: TheMarcosBC   ## Instagram: TheMarcosBC  ##
########################################################

# import default modules
import re

# import local modules
from . import Array, Main, String

########################################################
## ------- here starts the module definitions ------- ##
########################################################
class new(Array.new):
    data = {}

    def value(self, get):
        new = String.space(get)
        if get.isnumeric(): new = float(get)
        elif get == 'false': new = False
        elif get == 'none': new = None
        elif get == 'true': new = True
        return new

    def find(self, val=None, key=None):
        devolve = None

        if self.data:
            for k, v in self.data.items():
                if key and type(k) is str and str(k).find(str(key)) != -1:
                    Return = k, v
                elif not key and val and type(v) is str and str(val) in str(v).lower().split(' '):
                    Return = k, v

        return Return

    def __init__(self, string=None):
        if string:
            data = {}
            index = 0
            lines = string.split('\n')
            name = None

            if len(lines) > 0:
                for line in lines:
                    _line = line.replace(' ', '')

                    if _line != '' and _line[0 : 1] not in ['!', '#']:
                        if re.search('\[(.*?)\]', line):
                            index = 0
                            name = re.findall('\[(.*?)\]', line)[0]
                            data[name] = {}

                        elif line.find('=') != -1:
                            k, v = line.split('=')
                            key = Main.space(k)
                            val = self.value(v)

                            if name:
                                data[name][key] = val
                            else:
                                data[key] = val

                        else:
                            val = self.value(line)

                            if name:
                                data[name][index] = val
                            else:
                                data[index] = val

                            index += 1

                self.data = data

def open(path):
    if path:
        string = Path.read(path)
        return get(string)
