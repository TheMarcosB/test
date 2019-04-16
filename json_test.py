import json
from lib import Array, Json, Open

string="""
{
    5 : '10',
    8 : true,
    6.0 : 30,
    +123.30 : -123.30,
    '07' : abcçúü,
    ftp : 21,
    'dict' : {    },
    'list2' : [    ],
    "list" : ['a', 13, "c"],
    "http" : 80,
    "https" : "{443}",
    "test" : {
        "carros": 123,
        "marcos": 21,
        "fla": {
           "test": 1,
           'array': [1, 2, 3, [0, 1, 'a'], {
               'a': 1,
               'b': 2,
               'c': 3,
               'd': [0, 2, 3],
               'f': {
                   'a': 1,
                   2:3,
                   'g': 100
                }
              }
           ]
        }
    }
}

"""
if 1:
    print(Json.encode(Json.decode(string)))

else:
    a = Json.decode(Open.etcr('url_status.json'))
    a['0']['a']=2
    a[45]='marcos11'
    a[{46}]='marcos10'
    a[True]=1
    a[False]=2
    a[None]=3
    a['a']=4
    path='${ETC}/carros.json'
    if 0:
        Json.write(path, a)
    print(Array.string(Json.open(path)))
